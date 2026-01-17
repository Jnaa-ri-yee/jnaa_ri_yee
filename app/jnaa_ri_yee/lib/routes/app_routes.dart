/*
 * ======================================================                    *
 *  Project      : routes                                                    *
 *  File         : app_routes.dart                                           *
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
import '../presentation/screens/home_screen.dart';
import '../presentation/screens/camera_screen.dart';
import '../presentation/screens/info_screen.dart';

class AppRoutes {
  static const String home = '/home';
  static const String camera = '/camera';
  static const String info = '/info';

  static const String initialRoute = home;

  static final Map<String, WidgetBuilder> routes = {
    home: (context) => const HomeScreen(),
    camera: (context) => const CameraScreen(),
    info: (context) => const InfoScreen(),
  };
}
