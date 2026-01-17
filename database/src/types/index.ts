/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : index.ts                                                  *
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

import type { drive_v3 } from 'googleapis';

export type DriveFile = drive_v3.Schema$File;

export interface ImageDimensions {
  ancho: number;
  alto: number;
}

export interface ProcessResult {
  procesadas: number;
  errores: number;
}

export interface DownloadTask {
  fileId: string;
  fileName: string;
  destino: string;
  senaId: number;
  loteId: string;
}