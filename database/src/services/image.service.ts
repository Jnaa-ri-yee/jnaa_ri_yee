/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : image.service.ts                                          *
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

import sharp from 'sharp';
import { logError } from '../utils/logger.js';
import type { ImageDimensions } from '../types/index.js';

export class ImageService {
  async obtenerDimensiones(rutaArchivo: string): Promise<ImageDimensions> {
    try {
      const metadata = await sharp(rutaArchivo).metadata();
      return { 
        ancho: metadata.width || 0, 
        alto: metadata.height || 0 
      };
    } catch (error) {
      logError(`Error obteniendo dimensiones de ${rutaArchivo}`, error);
      return { ancho: 0, alto: 0 };
    }
  }

  async validarImagen(rutaArchivo: string): Promise<boolean> {
    try {
      await sharp(rutaArchivo).metadata();
      return true;
    } catch {
      return false;
    }
  }
}