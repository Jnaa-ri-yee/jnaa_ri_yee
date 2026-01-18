# ======================================================                     *
#  Project      : scripts                                                    *
#  File         : auto_setup.py                                              *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:36                                           *
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
Script principal para configurar automáticamente todo el sistema.
"""

import argparse
from pathlib import Path
import sys
import yaml

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.dataset_discovery import DatasetDiscovery
from core.auto_config_generator import AutoConfigGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Configuración automática del sistema de entrenamiento'
    )
    parser.add_argument(
        '--dataset-path',
        type=str,
        required=True,
        help='Ruta al dataset (ej: /path/to/datasets/)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='config/generated',
        help='Directorio donde guardar las configuraciones generadas'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SISTEMA AUTÓNOMO DE DETECCIÓN Y CONFIGURACIÓN")
    print("=" * 60)
    print()
    
    # 1. Descubrir dataset
    print("Paso 1/3: Descubriendo estructura del dataset...")
    discovery = DatasetDiscovery(args.dataset_path)
    report = discovery.discover()
    
    print()
    print("Resumen del Dataset:")
    print(f"  • Tipo: {report['dataset_type']}")
    print(f"  • Total de clases: {report['total_classes']}")
    print(f"  • Total de archivos: {report['distribution']['total_files']}")
    print(f"  • Promedio por clase: {report['distribution']['avg_samples']:.1f}")
    print(f"  • Desbalance: {report['distribution']['imbalance_ratio']:.2f}x")
    print()
    
    # Mostrar algunas clases
    print("Clases detectadas (primeras 10):")
    for i, cls in enumerate(report['classes'][:10], 1):
        count = report['distribution']['files_per_class'].get(cls, 0)
        print(f"  {i:2d}. {cls:20s} ({count} muestras)")
    if len(report['classes']) > 10:
        print(f"  ... y {len(report['classes']) - 10} clases más")
    print()
    
    # 2. Generar configuración automática
    print("Paso 2/3: Generando configuración automática...")
    config_gen = AutoConfigGenerator(report)
    config = config_gen.generate()
    
    print("Configuración generada:")
    print(f"  • Modelo: {config['model']['architecture']}")
    print(f"  • Backbone: {config['model']['backbone']}")
    print(f"  • Batch size: {config['dataset']['batch_size']}")
    print(f"  • Epochs: {config['training']['epochs']}")
    print(f"  • Learning rate: {config['training']['learning_rate']}")
    print()
    
    # 3. Guardar todo
    print("Paso 3/3: Guardando configuraciones...")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    discovery.save_report(output_dir)
    config_gen.save(output_dir)
    
    # Guardar también config de data loaders
    loader_config = discovery.get_data_loaders_config()
    loader_config_path = output_dir / 'data_loaders_config.yaml'
    with open(loader_config_path, 'w', encoding='utf-8') as f:
        yaml.dump(loader_config, f, default_flow_style=False, allow_unicode=True)
    print(f"Data loaders config guardado en: {loader_config_path}")
    
    print()
    print("=" * 60)
    print("SISTEMA CONFIGURADO EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Próximos pasos:")
    print("1. Revisa las configuraciones en:", output_dir)
    print("2. Ejecuta: python main.py train")
    print()


if __name__ == '__main__':
    main()
