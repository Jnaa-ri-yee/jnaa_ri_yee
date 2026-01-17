/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : auth.service.ts                                           *
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

import { google } from 'googleapis';
import * as fs from 'fs';
import { env, SCOPES } from '../config/env.js';
import { logger, logError } from '../utils/logger.js';

export class AuthService {
  async autenticar() {
    try {
      const credentials = JSON.parse(fs.readFileSync(env.GOOGLE_CREDENTIALS_PATH, 'utf-8'));
      const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;
      const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

      if (!fs.existsSync(env.GOOGLE_TOKEN_PATH)) {
        throw new Error(
          `No se encontró ${env.GOOGLE_TOKEN_PATH}. ` +
          `Ejecuta primero el script de autenticación.`
        );
      }

      const token = JSON.parse(fs.readFileSync(env.GOOGLE_TOKEN_PATH, 'utf-8'));
      oAuth2Client.setCredentials(token);

      logger.info('Autenticación con Google Drive exitosa');
      return google.drive({ version: 'v3', auth: oAuth2Client });
    } catch (error) {
      logError('Error en autenticación', error);
      throw error;
    }
  }

  async generarToken() {
    const { authenticate } = await import('@google-cloud/local-auth');
    
    const auth = await authenticate({
      scopes: SCOPES as unknown as string[],
      keyfilePath: env.GOOGLE_CREDENTIALS_PATH,
    });
    
    fs.writeFileSync(env.GOOGLE_TOKEN_PATH, JSON.stringify(auth.credentials));
    logger.info(`Token guardado en ${env.GOOGLE_TOKEN_PATH}`);
  }
}