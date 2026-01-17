/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : import-dataset.ts                                         *
 *  Team         : Equipo Jña'a Ri Y'ë'ë                                     *
 *  Developer    : Axel Eduardo Urbina Secundino                             *
 *  Created      : 2026-01-17                                                *
 *  Last Updated : 2026-01-17 03:05                                          *
 * ======================================================                    *
 *                                                                           *
 *  License:                                                                 *
 * © 2026 Equipo Jña'a Ri Y'ë'ë                                              *
 *                                                                           *
 * Este software y su código fuente son propiedad exclusiva                  *
 * del equipo Jña'a Ri Y'ë'ë.                                                *
 *                                                                           *
 * Uso permitido únicamente para:                                            *
 * - Evaluación académica                                                    *
 * - Revisión técnica                                                        *
 * - Convocatorias, hackatones o concursos                                   *
 *                                                                           *
 * Queda prohibida la copia, modificación, redistribución                    *
 * o uso sin autorización expresa del equipo.                                *
 *                                                                           *
 * El software se proporciona "tal cual", sin garantías.                     *
 */

import { PrismaClient } from '../generated/prisma/client.js';
import { PrismaPg } from '@prisma/adapter-pg';
import pg from 'pg'; 
import * as fs from 'fs';
import * as path from 'path';
import { AuthService } from './services/auth.service.js';
import { DriveService } from './services/drive.service.js';
import { DBService } from './services/db.service.js';
import { ImageService } from './services/image.service.js';
import { logger, logError } from './utils/logger.js';
import { crearCola } from './utils/queue.js';
import { env } from './config/env.js';
import { ESTRUCTURA_DATASET, type CategoriaConfig } from './config/dataset-structure.js';
import type { ProcessResult, DownloadTask } from './types/index.js';

class DatasetImporter {
  private prisma: PrismaClient;
  private pool: pg.Pool;
  private authService: AuthService;
  private driveService!: DriveService;
  private dbService: DBService;
  private imageService: ImageService;
  private cola = crearCola();

  constructor() {
    this.pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
    const adapter = new PrismaPg(this.pool);

    this.prisma = new PrismaClient({ adapter });
    this.authService = new AuthService();
    this.dbService = new DBService(this.prisma);
    this.imageService = new ImageService();
  }

  async inicializar() {
    const drive = await this.authService.autenticar();
    this.driveService = new DriveService(drive);
  }

  crearEstructuraCarpetas(
    estructura: CategoriaConfig[], 
    basePath: string = env.BASE_OUTPUT_DIR
  ) {
    if (!fs.existsSync(basePath)) {
      fs.mkdirSync(basePath, { recursive: true });
    }

    estructura.forEach(categoria => {
      const categoriaPath = path.join(basePath, categoria.codigo);
      fs.mkdirSync(categoriaPath, { recursive: true });

      if (categoria.subcategorias) {
        categoria.subcategorias.forEach(sub => {
          const subPath = path.join(categoriaPath, sub.codigo);
          fs.mkdirSync(subPath, { recursive: true });

          if (sub.senas) {
            sub.senas.forEach(sena => {
              const senaPath = path.join(subPath, sena.toLowerCase());
              fs.mkdirSync(senaPath, { recursive: true });
            });
          }
        });
      }

      if (categoria.senas) {
        categoria.senas.forEach(sena => {
          const senaPath = path.join(categoriaPath, sena.toLowerCase());
          fs.mkdirSync(senaPath, { recursive: true });
        });
      }
    });
  }

  async procesarImagenesSena(
    carpetaDriveId: string,
    senaId: number,
    rutaLocal: string,
    loteId: string
  ): Promise<ProcessResult> {
    const archivos = await this.driveService.listarArchivos(carpetaDriveId);
    const imagenes = this.driveService.filtrarImagenes(archivos);

    if (imagenes.length === 0) {
      logger.warn(`No se encontraron imágenes en carpeta Drive ${carpetaDriveId}`);
      return { procesadas: 0, errores: 0 };
    }

    logger.info(`Procesando ${imagenes.length} imágenes...`);

   // Asegurarse de que la carpeta exista
if (!fs.existsSync(rutaLocal)) {
  fs.mkdirSync(rutaLocal, { recursive: true });
}

const tareas: DownloadTask[] = imagenes.map(img => {
  const safeFileName = img.name?.replace(/[^\w.-]/g, '_'); // normaliza nombre
  return {
    fileId: img.id!,
    fileName: img.name!,
    destino: path.join(rutaLocal, `${Date.now()}_${safeFileName}`),
    senaId,
    loteId
  };
});


    let procesadas = 0;
    let errores = 0;

    await Promise.all(
      tareas.map(tarea => 
        this.cola.add(async () => {
          try {
            // Descargar imagen
            await this.driveService.descargarArchivo(tarea.fileId, tarea.destino);

            // Validar imagen
            const esValida = await this.imageService.validarImagen(tarea.destino);
            if (!esValida) {
              logger.warn(`Imagen inválida: ${tarea.fileName}`);
              fs.unlinkSync(tarea.destino);
              errores++;
              return;
            }

            // Obtener información del archivo
            const stats = fs.statSync(tarea.destino);

            await this.dbService.crearMuestra({
              rutaArchivo: tarea.destino,
              nombreOriginal: tarea.fileName,
              tamanoArchivo: stats.size,
              formato: path.extname(tarea.fileName).substring(1).toLowerCase(),
              senaId: tarea.senaId,
              loteId: tarea.loteId
            });

            procesadas++;
            logger.debug(`${tarea.fileName}`);
          } catch (error) {
            errores++;
            logError(`Error procesando ${tarea.fileName}`, error);
          }
        })
      )
    );

    return { procesadas, errores };
  }

  async procesarEstructura(
    estructura: CategoriaConfig[],
    carpetaRaizDriveId: string,
    loteId: string,
    padreId?: number
  ): Promise<ProcessResult> {
    let totalProcesadas = 0;
    let totalErrores = 0;

    for (const [index, config] of estructura.entries()) {
      try {
        // Crear categoría en BD
        const categoria = await this.dbService.obtenerOCrearCategoria(
          config.nombre,
          config.codigo,
          padreId,
          config.orden ?? index
        );

        // Buscar carpeta en Drive
        const carpetaDrive = await this.driveService.buscarCarpeta(
          carpetaRaizDriveId,
          config.nombre
        );

        if (!carpetaDrive) {
          logger.warn(`Carpeta no encontrada en Drive: ${config.nombre}`);
          continue;
        }

        // Procesar subcategorías recursivamente
        if (config.subcategorias) {
          const { procesadas, errores } = await this.procesarEstructura(
            config.subcategorias,
            carpetaDrive.id!,
            loteId,
            categoria.id
          );
          totalProcesadas += procesadas;
          totalErrores += errores;
        }

        // Procesar señas de esta categoría
        if (config.senas) {
  for (const senaCodigo of config.senas) {
    const senaNombre = senaCodigo.toUpperCase();
    const sena = await this.dbService.obtenerOCrearSena(
      senaNombre,
      senaCodigo.toLowerCase(),
      categoria.id,
      config.dificultad
    );

    // Buscar carpeta de la seña en Drive
    const carpetaSena = await this.driveService.buscarCarpeta(
      carpetaDrive.id!,
      senaCodigo
    );

    if (carpetaSena) {
      // 🔹 Determinar la ruta de la categoría/subcategoría de forma segura
      let rutaCategoria = config.codigo; // Por defecto la categoría actual

      if (padreId) {
        // Si existe padre, obtener su código de la BD
        const categoriaPadre = await this.prisma.categoria.findUnique({
          where: { id: padreId }
        });
        if (categoriaPadre) {
          rutaCategoria = path.join(categoriaPadre.codigo, config.codigo);
        }
      }

      const rutaLocal = path.join(
        env.BASE_OUTPUT_DIR,
        rutaCategoria,
        senaCodigo.toLowerCase()
      );

      // Crear carpeta si no existe
      if (!fs.existsSync(rutaLocal)) {
        fs.mkdirSync(rutaLocal, { recursive: true });
      }

      const { procesadas, errores } = await this.procesarImagenesSena(
        carpetaSena.id!,
        sena.id,
        rutaLocal,
        loteId
      );

      totalProcesadas += procesadas;
      totalErrores += errores;
    } else {
      logger.warn(`Carpeta de seña no encontrada: ${senaCodigo}`);
    }
  }
}

      } catch (error) {
        logError(`Error procesando categoría ${config.nombre}`, error);
        totalErrores++;
      }
    }

    return { procesadas: totalProcesadas, errores: totalErrores };
  }

  async importar() {
    const lote = await this.dbService.crearLote(
      `Importación Dataset ${new Date().toISOString()}`,
      'Importación automática desde Google Drive'
    );

    try {
      logger.info('Iniciando importación del dataset...\n');

      const { procesadas, errores } = await this.procesarEstructura(
        ESTRUCTURA_DATASET,
        env.DRIVE_FOLDER_ID,
        lote.id
      );

      await this.dbService.actualizarLote(lote.id, {
        totalArchivos: procesadas + errores,
        procesados: procesadas + errores,
        exitosos: procesadas,
        fallidos: errores,
        estado: errores > 0 ? 'COMPLETADO' : 'COMPLETADO'
      });

      logger.info('\nImportación completada!');
      logger.info(`   Imágenes procesadas: ${procesadas}`);
      logger.info(`   Errores: ${errores}`);

      return { procesadas, errores };
    } catch (error) {
      logError('Error crítico en importación', error);
      
      await this.dbService.actualizarLote(lote.id, {
        totalArchivos: 0,
        procesados: 0,
        exitosos: 0,
        fallidos: 1,
        estado: 'FALLIDO',
        errores: (error as Error).message
      });

      throw error;
    }
  }

  async desconectar() {
    await this.prisma.$disconnect();
  }
}

// Función principal
async function main() {
  const importer = new DatasetImporter();

  try {
    // Crear estructura de carpetas
    logger.info('Creando estructura de carpetas...');
    importer.crearEstructuraCarpetas(ESTRUCTURA_DATASET);
    logger.info('Carpetas creadas\n');

    // Inicializar servicios
    await importer.inicializar();

    // Ejecutar importación
    await importer.importar();
  } catch (error) {
    logError('Error fatal', error);
    process.exit(1);
  } finally {
    await importer.desconectar();
  }
}

// Ejecutar
main();

export { DatasetImporter };