/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : db.service.ts                                             *
 *  Team         : Equipo Jña'a Ri Y'ë'ë                                     *
 *  Developer    : Axel Eduardo Urbina Secundino                             *
 *  Created      : 2026-01-17                                                *
 *  Last Updated : 2026-01-17 03:04                                          *
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

import { PrismaClient, type Categoria, type Sena, type LoteSubida } from '../../generated/prisma/client.js';
import { logger } from '../utils/logger.js';
import { ImageService } from './image.service.js';

export class DBService {
  private imageService = new ImageService();

  constructor(private prisma: PrismaClient) {}

  async obtenerOCrearCategoria(
    nombre: string,
    codigo: string,
    padreId?: number,
    orden: number = 0
  ): Promise<Categoria> {
    let categoria = await this.prisma.categoria.findUnique({ where: { codigo } });
    
    if (!categoria) {
      categoria = await this.prisma.categoria.create({
        data: { nombre, codigo, padreId, orden }
      });
      logger.info(`Categoría creada: ${nombre}`);
    }
    
    return categoria;
  }

  async obtenerOCrearSena(
    nombre: string,
    codigo: string,
    categoriaId: number,
    dificultad: 'BASICO' | 'INTERMEDIO' | 'AVANZADO' = 'BASICO'
  ): Promise<Sena> {
    let sena = await this.prisma.sena.findUnique({ where: { codigo } });
    
    if (!sena) {
      sena = await this.prisma.sena.create({
        data: { nombre, codigo, categoriaId, dificultad }
      });
      logger.info(`Seña creada: ${nombre}`);
    }
    
    return sena;
  }

  async crearLote(nombre: string, descripcion?: string): Promise<LoteSubida> {
    return this.prisma.loteSubida.create({
      data: {
        nombre,
        descripcion,
        estado: 'PROCESANDO',
        iniciadoEn: new Date()
      }
    });
  }

  async actualizarLote(
    id: string,
    datos: {
      totalArchivos: number;
      procesados: number;
      exitosos: number;
      fallidos: number;
      estado: 'COMPLETADO' | 'FALLIDO';
      errores?: string;
    }
  ) {
    return this.prisma.loteSubida.update({
      where: { id },
      data: {
        ...datos,
        completadoEn: new Date()
      }
    });
  }

  async crearMuestra(datos: {
    rutaArchivo: string;
    nombreOriginal: string;
    tamanoArchivo: number;
    formato: string;
    senaId: number;
    loteId: string;
  }) {
    const { ancho, alto } = await this.imageService.obtenerDimensiones(datos.rutaArchivo);
    
    return this.prisma.muestra.create({
      data: {
        tipo: 'IMAGEN',
        rutaArchivo: datos.rutaArchivo,
        nombreOriginal: datos.nombreOriginal,
        tamanoArchivo: datos.tamanoArchivo,
        ancho,
        alto,
        formato: datos.formato,
        calidad: 'PENDIENTE',
        fuente: 'LOTE',
        loteSubidaId: datos.loteId,
        senaId: datos.senaId
      }
    });
  }
}