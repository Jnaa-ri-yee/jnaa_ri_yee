/*
 * ======================================================                    *
 *  Project      : database                                                  *
 *  File         : dataset-structure.ts                                      *
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

export interface CategoriaConfig {
  nombre: string;
  codigo: string;
  orden?: number;
  dificultad?: 'BASICO' | 'INTERMEDIO' | 'AVANZADO';
  subcategorias?: CategoriaConfig[];
  senas?: string[];
}

export const ESTRUCTURA_DATASET: CategoriaConfig[] = [
  {
    nombre: 'Alfabeto',
    codigo: 'alfabeto',
    orden: 1,
    subcategorias: [
      {
        nombre: 'Vocales',
        codigo: 'vocales',
        orden: 1,
        dificultad: 'BASICO',
        senas: ['a', 'e', 'i', 'o', 'u']
      },
      {
        nombre: 'Consonantes',
        codigo: 'consonantes',
        orden: 2,
        dificultad: 'BASICO',
        senas: ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
      }
    ]
  },
  {
    nombre: 'Palabras',
    codigo: 'palabras',
    orden: 2,
    subcategorias: [
      {
        nombre: 'Saludos',
        codigo: 'saludos',
        dificultad: 'INTERMEDIO',
        senas: ['hola', 'adios', 'buenos-dias', 'buenas-tardes', 'buenas-noches']
      },
      {
        nombre: 'Cortesía',
        codigo: 'cortesia',
        dificultad: 'INTERMEDIO',
        senas: ['gracias', 'por-favor', 'perdon', 'disculpa']
      }
    ]
  },
  {
    nombre: 'Frases',
    codigo: 'frases',
    orden: 3,
    dificultad: 'AVANZADO',
    senas: ['como-estas', 'me-llamo', 'mucho-gusto', 'de-nada']
  }
];