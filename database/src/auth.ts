/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : auth.ts                                                   *
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

import { AuthService } from './services/auth.service.js';
import { logger, logError } from './utils/logger.js';

async function main() {
  const authService = new AuthService();
  
  try {
    logger.info('Iniciando proceso de autenticación...');
    logger.info('Se abrirá un navegador para autorizar el acceso a Google Drive');
    
    await authService.generarToken();
    
    logger.info('Autenticación completada exitosamente');
    logger.info('Ahora puedes ejecutar: npm run import');
  } catch (error) {
    logError('Error en autenticación', error);
    process.exit(1);
  }
}

main();