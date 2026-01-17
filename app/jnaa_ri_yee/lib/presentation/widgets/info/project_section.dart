/*
 * ======================================================                    *
 *  Project      : info                                                      *
 *  File         : project_section.dart                                      *
 *  Team         : Equipo Jña'a Ri Y'ë'ë                                     *
 *  Developer    : Axel Eduardo Urbina Secundino                             *
 *  Created      : 2025-10-30                                                *
 *  Last Updated : 2026-01-16 22:01                                          *
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

import 'package:flutter/material.dart';

class ProjectSection extends StatelessWidget {
  const ProjectSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(children: const [
      Text("Jña'a Ri Y'ë'ë",
          style: TextStyle(
              color: Colors.white,
              fontSize: 38,
              fontWeight: FontWeight.bold)),
      SizedBox(height: 16),
      Text(
        "Interpretación de señas con visión por computadora para inclusión social.",
        textAlign: TextAlign.center,
        style: TextStyle(color: Colors.white70, fontSize: 18),
      ),
    ]);
  }
}
