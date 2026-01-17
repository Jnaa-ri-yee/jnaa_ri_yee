/*
 * ======================================================                    *
 *  Project      : info                                                      *
 *  File         : team_section.dart                                         *
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
import 'team_member_card.dart';

class TeamSection extends StatelessWidget {
  const TeamSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(children: const [
      Text("Integrantes",
          style: TextStyle(
              color: Colors.white,
              fontSize: 26,
              fontWeight: FontWeight.bold)),
      SizedBox(height: 20),
      TeamMemberCard(
        name: "Anahi Figueroa González",
        github: "https://github.com/Ann8ix",
        linkedin:
            "https://www.linkedin.com/in/anahi-figueroa-gonzalez-2a4a3438b",
      ),
      TeamMemberCard(
        name: "Axel Eduardo Urbina Secundino",
        github: "https://github.com/AEUS-06",
        linkedin: "https://www.linkedin.com/in/axel-eduardo-u-8124a837b",
      ),
    ]);
  }
}
