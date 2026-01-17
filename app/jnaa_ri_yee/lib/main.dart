/*
 * ======================================================                    *
 *  Project      : Frontend                                                  *
 *  File         : main.dart                                                 *
 *  Team         : Equipo Jña'a Ri Y'ë'ë                                     *
 *  Developer    : Axel Eduardo Urbina Secundino                             *
 *  Created      : 2025-10-30                                                *
 *  Last Updated : 2026-01-16 19:05                                          *
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
import 'routes/app_routes.dart';
import 'core/theme/theme.dart';

void main() {
  runApp(const InterpreteLSM());
}

class InterpreteLSM extends StatelessWidget {
  const InterpreteLSM({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Jñaa Ri Yee - Traductor de Señas',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      initialRoute: AppRoutes.initialRoute,
      routes: AppRoutes.routes,
    );
  }
}
