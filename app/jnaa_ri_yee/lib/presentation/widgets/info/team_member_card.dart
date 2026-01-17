/*
 * ======================================================                    *
 *  Project      : info                                                      *
 *  File         : team_member_card.dart                                     *
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
import 'package:url_launcher/url_launcher.dart';

class TeamMemberCard extends StatelessWidget {
  final String name, github, linkedin;
  const TeamMemberCard(
      {super.key,
      required this.name,
      required this.github,
      required this.linkedin});

  Future<void> open(String url) async {
    await launchUrl(Uri.parse(url),
        mode: LaunchMode.externalApplication);
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white.withOpacity(0.1),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: ListTile(
        leading: const Icon(Icons.person, color: Colors.white),
        title: Text(name,
            style: const TextStyle(color: Colors.white, fontSize: 18)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            GestureDetector(
                onTap: () => open(linkedin),
                child: const Text("LinkedIn",
                    style: TextStyle(color: Colors.cyanAccent))),
            GestureDetector(
                onTap: () => open(github),
                child: const Text("GitHub",
                    style: TextStyle(color: Colors.purpleAccent))),
          ],
        ),
      ),
    );
  }
}
