/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : env.ts                                                    *
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

import { config } from 'dotenv';
import { z } from 'zod';

config({ path: '.env.local' });

const envSchema = z.object({
  GOOGLE_CREDENTIALS_PATH: z.string().default('./credentials.json'),
  GOOGLE_TOKEN_PATH: z.string().default('./token.json'),
  DRIVE_FOLDER_ID: z.string().min(1, 'DRIVE_FOLDER_ID es requerido'),
  BASE_OUTPUT_DIR: z.string().default('./datasets'),
  MAX_CONCURRENT_DOWNLOADS: z.coerce.number().int().positive().default(5),
  RETRY_ATTEMPTS: z.coerce.number().int().positive().default(3),
  RETRY_DELAY_MS: z.coerce.number().int().positive().default(1000),
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
});

type Env = z.infer<typeof envSchema>;

function validateEnv(): Env {
  try {
    return envSchema.parse(process.env);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const issues = error.issues.map((i) => `  - ${i.path.join('.')}: ${i.message}`);
      throw new Error(`Error en variables de entorno:\n${issues.join('\n')}`);
    }
    throw error;
  }
}

export const env = validateEnv();

export const SCOPES = ['https://www.googleapis.com/auth/drive.readonly'] as const;