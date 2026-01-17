/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : retry.ts                                                  *
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

import { logger } from './logger.js';
import { env } from '../config/env.js';

export async function conReintento<T>(
  fn: () => Promise<T>,
  nombre: string,
  intentos: number = env.RETRY_ATTEMPTS
): Promise<T> {
  let ultimoError: Error | null = null;

  for (let i = 0; i < intentos; i++) {
    try {
      return await fn();
    } catch (error) {
      ultimoError = error as Error;
      if (i < intentos - 1) {
        const delay = env.RETRY_DELAY_MS * Math.pow(2, i);
        logger.warn(`Reintento ${i + 1}/${intentos} para ${nombre} en ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw new Error(`Falló después de ${intentos} intentos: ${nombre} - ${ultimoError?.message}`);
}