/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : drive.service.ts                                          *
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

import type { drive_v3 } from 'googleapis';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream';
import { promisify } from 'util';
import { logger } from '../utils/logger.js';
import { conReintento } from '../utils/retry.js';
import type { DriveFile } from '../types/index.js';

const streamPipeline = promisify(pipeline);

export class DriveService {
  constructor(private drive: drive_v3.Drive) {}

  async listarArchivos(folderId: string): Promise<DriveFile[]> {
    return conReintento(async () => {
      const response = await this.drive.files.list({
        q: `'${folderId}' in parents and trashed=false`,
        fields: 'files(id, name, mimeType, size)',
        pageSize: 1000
      });
      return response.data.files || [];
    }, `listar archivos de carpeta ${folderId}`);
  }

  async descargarArchivo(fileId: string, destino: string): Promise<void> {
    return conReintento(async () => {
      const dest = createWriteStream(destino);
      const response = await this.drive.files.get(
        { fileId, alt: 'media' },
        { responseType: 'stream' }
      );
      await streamPipeline(response.data as any, dest);
      logger.debug(`Descargado: ${destino}`);
    }, `descargar archivo ${fileId}`);
  }

  async buscarCarpeta(parentId: string, nombreCarpeta: string): Promise<DriveFile | null> {
    const archivos = await this.listarArchivos(parentId);
    return archivos.find(f => 
      f.mimeType === 'application/vnd.google-apps.folder' &&
      f.name?.toLowerCase() === nombreCarpeta.toLowerCase()
    ) || null;
  }

  filtrarImagenes(archivos: DriveFile[]): DriveFile[] {
    return archivos.filter(f => 
      f.mimeType?.startsWith('image/') && 
      /\.(jpe?g|png|webp)$/i.test(f.name || '')
    );
  }
}