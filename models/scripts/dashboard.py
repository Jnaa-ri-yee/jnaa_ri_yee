# ======================================================                     *
#  Project      : scripts                                                    *
#  File         : dashboard.py                                               *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:13                                           *
# ======================================================                     *
#                                                                            *
#  License:                                                                  *
# © 2026 Equipo Jña'a Ri Y'ë'ë                                               *
#                                                                            *
# Este software y su código fuente son propiedad exclusiva                   *
# del equipo Jña'a Ri Y'ë'ë.                                                 *
#                                                                            *
# Uso permitido únicamente para:                                             *
# - Evaluación académica                                                     *
# - Revisión técnica                                                         *
# - Convocatorias, hackatones o concursos                                    *
#                                                                            *
# Queda prohibida la copia, modificación, redistribución                     *
# o uso sin autorización expresa del equipo.                                 *
#                                                                            *
# El software se proporciona "tal cual", sin garantías.                      *

"""
Script para ver dashboard del sistema.

Uso:
    python scripts/dashboard.py
    python scripts/dashboard.py --classes
    python scripts/dashboard.py --confusion
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools.visualization.dashboard import SimpleDashboard


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Dashboard del sistema')
    parser.add_argument(
        '--version',
        type=str,
        help='Ver detalles de una versión específica'
    )
    parser.add_argument(
        '--classes',
        action='store_true',
        help='Mostrar rendimiento por clase'
    )
    parser.add_argument(
        '--confusion',
        action='store_true',
        help='Mostrar confusiones principales'
    )
    
    args = parser.parse_args()
    
    dashboard = SimpleDashboard()
    
    if args.classes:
        dashboard.show_class_performance(args.version)
    elif args.confusion:
        dashboard.show_confusion_pairs(args.version)
    else:
        dashboard.show_overview()


if __name__ == '__main__':
    main()

