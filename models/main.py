# ======================================================                     *
#  Project      : models                                                     *
#  File         : main.py                                                    *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:58                                           *
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

# main.py
"""
Script principal TODO-EN-UNO para el sistema de entrenamiento automático.

Uso:
    python main.py setup --dataset /ruta/dataset
    python main.py train
    python main.py evaluate
    python main.py dashboard
"""

import argparse
import sys
from pathlib import Path

# Agregar src al path ANTES de cualquier import
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def setup_dataset(args):
    """Paso 1: Configurar dataset automáticamente."""
    from src.core.dataset_discovery import DatasetDiscovery
    from src.core.auto_config_generator import AutoConfigGenerator
    import yaml
    
    print("\n" + "="*70)
    print("PASO 1: CONFIGURACIÓN AUTOMÁTICA DEL DATASET")
    print("="*70 + "\n")
    
    # Validar que existe el dataset
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"Error: El dataset no existe en '{args.dataset}'")
        return False
    
    # Descubrir dataset
    print("Analizando estructura del dataset...")
    discovery = DatasetDiscovery(str(dataset_path))
    report = discovery.discover()
    
    # Mostrar resumen
    print("\nResumen del Dataset:")
    print(f"  • Tipo: {report['dataset_type']}")
    print(f"  • Total de clases: {report['total_classes']}")
    print(f"  • Total de archivos: {report['distribution']['total_files']}")
    print(f"  • Promedio por clase: {report['distribution']['avg_samples']:.1f}")
    
    # Mostrar algunas clases
    print("\nPrimeras 10 clases detectadas:")
    for i, cls in enumerate(report['classes'][:10], 1):
        count = report['distribution']['files_per_class'].get(cls, 0)
        print(f"  {i:2d}. {cls:30s} ({count:3d} muestras)")
    
    if len(report['classes']) > 10:
        print(f"  ... y {len(report['classes']) - 10} clases más")
    
    # Generar configuración
    print("\nGenerando configuración automática...")
    config_gen = AutoConfigGenerator(report)
    config = config_gen.generate()
    
    print(f"Modelo: {config['model']['architecture']}")
    print(f"Backbone: {config['model']['backbone']}")
    print(f"Batch size: {config['dataset']['batch_size']}")
    print(f"Epochs: {config['training']['epochs']}")
    
    # Guardar configuraciones
    output_dir = Path('config/generated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    discovery.save_report(output_dir)
    config_gen.save(output_dir)
    
    # Guardar config de data loaders
    loader_config = discovery.get_data_loaders_config()
    loader_config_path = output_dir / 'data_loaders_config.yaml'
    with open(loader_config_path, 'w', encoding='utf-8') as f:
        yaml.dump(loader_config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"\nConfiguración guardada en: {output_dir}")
    print("\nPróximo paso:")
    print("    python main.py train")
    print("\n" + "="*70 + "\n")
    
    return True


def train_model(args):
    """Paso 2: Entrenar modelo con versionado automático."""
    import torch
    import yaml
    import json
    import numpy as np
    from src.data.loaders.universal_loader import create_data_loaders
    from src.algorithms.deep.simple_hybrid_model import SimpleHybridModel
    from src.training.deep.hybrid_trainer import HybridTrainer
    from src.core.version_manager import VersionManager
    from src.core.experiment_logger import ExperimentLogger
    from src.metrics.analysis.error_analyzer import ErrorAnalyzer
    
    print("\n" + "="*70)
    print("PASO 2: ENTRENAMIENTO CON VERSIONADO AUTOMÁTICO")
    print("="*70 + "\n")
    
    # Verificar configuración
    config_path = Path('config/generated/auto_generated_config.yaml')
    if not config_path.exists():
        print("Error: No se encontró configuración.")
        print("   Ejecuta primero: python main.py setup --dataset /ruta/dataset")
        return False
    
    # Cargar configuración
    print("Cargando configuración...")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print("Configuración cargada")
    
    # Iniciar logging de experimento
    experiment_logger = ExperimentLogger()
    run_id = experiment_logger.start_run(config)
    print(f"Run ID: {run_id}")
    
    try:
        # Crear data loaders
        print("\nPreparando datos...")
        loaders = create_data_loaders(
            config_path='config/generated/data_loaders_config.yaml',
            batch_size=config['dataset']['batch_size'],
            num_workers=config['dataset']['num_workers'],
            extract_landmarks=config['features']['landmarks']['enabled']
        )
        
        print(f"Train: {len(loaders['train'].dataset)} muestras")
        print(f"Val: {len(loaders['val'].dataset)} muestras")
        print(f"Test: {len(loaders['test'].dataset)} muestras")
        
        # Crear modelo
        print("\nConstruyendo modelo...")
        model = SimpleHybridModel(
            num_classes=config['dataset']['num_classes'],
            backbone=config['model']['backbone'],
            use_landmarks=config['model']['use_landmarks'],
            pretrained=config['model']['pretrained']
        )
        
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"Arquitectura: {config['model']['architecture']}")
        print(f"Parámetros: {total_params:,}")
        print(f"Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")
        
        # Entrenar
        print("\n" + "="*70)
        print("ENTRENANDO...")
        print("="*70)
        
        trainer = HybridTrainer(
            model=model,
            train_loader=loaders['train'],
            val_loader=loaders['val'],
            test_loader=loaders['test'],
            config=config
        )
        
        results = trainer.train()
        
        # Análisis de errores
        print("\nAnalizando errores...")
        error_analyzer = ErrorAnalyzer(
            predictions=results['test_metrics']['predictions'],
            labels=results['test_metrics']['labels'],
            class_names=config['dataset']['class_names']
        )
        
        error_analysis = error_analyzer.analyze()
        recommendations = error_analyzer.get_recommendations()
        
        print("\nRecomendaciones:")
        for rec in recommendations:
            print(f"  {rec}")
        
        # Gestionar versión
        print("\n" + "="*70)
        print("GESTIONANDO VERSIONES...")
        print("="*70)
        
        version_manager = VersionManager()
        
        version_name = version_manager.create_new_version(
            model_info={
                'architecture': config['model']['architecture'],
                'backbone': config['model']['backbone'],
                'total_params': total_params,
                'trainable_params': trainable_params
            },
            metrics=results['test_metrics'],
            config=config,
            force=args.force_version if hasattr(args, 'force_version') else False
        )
        
        if version_name:
            # Guardar todo
            version_dir = Path('models') / version_name
            eval_dir = Path('evaluation') / version_name
            
            # Modelo
            trainer.save_model(version_dir / 'final' / 'model.pth')
            
            # Config
            with open(version_dir / 'config' / 'training_config.yaml', 'w') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            # Métricas
            metrics_dir = eval_dir / 'metrics'
            metrics_dir.mkdir(parents=True, exist_ok=True)
            
            # Guardar solo métricas serializables
            metrics_to_save = {
                k: v for k, v in results['test_metrics'].items()
                if k not in ['predictions', 'labels', 'probabilities']
            }
            
            with open(metrics_dir / 'test_metrics.json', 'w') as f:
                json.dump(metrics_to_save, f, indent=2)
            
            # Análisis de errores
            analysis_dir = eval_dir / 'analysis'
            analysis_dir.mkdir(parents=True, exist_ok=True)
            
            with open(analysis_dir / 'error_analysis.json', 'w') as f:
                json.dump(error_analysis, f, indent=2, ensure_ascii=False)
            
            # Visualizaciones
            trainer.plot_training_history(analysis_dir)
            trainer.plot_confusion_matrix(
                cm=np.array(results['test_metrics']['confusion_matrix']),
                class_names=config['dataset']['class_names'],
                save_dir=analysis_dir
            )
            
            # Registrar experimento exitoso
            experiment_logger.end_run(
                run_id=run_id,
                results=results['test_metrics'],
                version=version_name,
                success=True
            )
            
            # Resumen final
            print("\n" + "="*70)
            print("ENTRENAMIENTO COMPLETADO")
            print("="*70)
            print(f"\nVersión: {version_name}")
            print(f"Modelo: models/{version_name}/final/model.pth")
            print(f"Evaluación: evaluation/{version_name}/")
            print(f"\nMétricas:")
            print(f"  • Test Accuracy: {results['test_metrics']['test_accuracy']:.4f}")
            print(f"  • Test F1-Score: {results['test_metrics']['test_f1']:.4f}")
            print(f"  • Test Precision: {results['test_metrics']['test_precision']:.4f}")
            
            best_version = version_manager.get_best_version()
            print(f"\nMejor versión: {best_version}")
            
            print("\nPróximos pasos:")
            print("    python main.py dashboard    # Ver resumen")
            print("    python main.py evaluate      # Evaluación detallada")
            print("\n" + "="*70 + "\n")
            
            return True
        else:
            print("\nNo se creó nueva versión (no hubo mejora suficiente)")
            experiment_logger.end_run(
                run_id=run_id,
                results=results['test_metrics'],
                version=None,
                success=False
            )
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()
        
        experiment_logger.end_run(
            run_id=run_id,
            results={},
            version=None,
            success=False
        )
        return False


def evaluate_models(args):
    """Paso 3: Evaluación detallada de modelos."""
    from src.core.version_manager import VersionManager
    import json
    
    print("\n" + "="*70)
    print("EVALUACIÓN DETALLADA DE MODELOS")
    print("="*70 + "\n")
    
    vm = VersionManager()
    
    if not vm.registry['versions']:
        print("No hay modelos entrenados aún.")
        print("   Ejecuta: python main.py train")
        return False
    
    print(f"Total de versiones: {len(vm.registry['versions'])}\n")
    
    # Tabla comparativa
    print("Comparación de Versiones:")
    print("-" * 70)
    print(f"{'Versión':<10} {'Accuracy':<12} {'F1-Score':<12} {'Creado':<20}")
    print("-" * 70)
    
    for version_data in vm.registry['versions']:
        version = version_data['version']
        metrics = version_data['metrics']
        created = version_data['created_at'][:19]
        
        is_best = version == vm.get_best_version()
        marker = "🏆" if is_best else "  "
        
        print(f"{marker} {version:<10} "
              f"{metrics.get('test_accuracy', 0):<12.4f} "
              f"{metrics.get('test_f1', 0):<12.4f} "
              f"{created:<20}")
    
    print("-" * 70)
    
    # Mejor modelo
    best_version = vm.get_best_version()
    best_info = vm.get_version_info(best_version)
    
    print(f"\nMejor Modelo: {best_version}")
    print(f"  • Accuracy: {best_info['metrics']['test_accuracy']:.4f}")
    print(f"  • Precision: {best_info['metrics']['test_precision']:.4f}")
    print(f"  • Recall: {best_info['metrics']['test_recall']:.4f}")
    print(f"  • F1-Score: {best_info['metrics']['test_f1']:.4f}")
    print(f"  • Arquitectura: {best_info['model_info']['architecture']}")
    print(f"  • Parámetros: {best_info['model_info']['total_params']:,}")
    
    # Análisis de errores
    error_analysis_path = Path(f'evaluation/{best_version}/analysis/error_analysis.json')
    if error_analysis_path.exists():
        with open(error_analysis_path) as f:
            error_analysis = json.load(f)
        
        print(f"\nAnálisis de Errores:")
        print(f"  • Total de errores: {error_analysis['summary']['total_errors']}")
        print(f"  • Tasa de error: {error_analysis['summary']['error_rate']:.2%}")
        
        print(f"\nClases más difíciles:")
        for cls_data in error_analysis['hardest_classes'][:3]:
            print(f"  • {cls_data['class_name']}: {cls_data['accuracy']:.2%}")
        
        print(f"\nClases más fáciles:")
        for cls_data in error_analysis['easiest_classes'][:3]:
            print(f"  • {cls_data['class_name']}: {cls_data['accuracy']:.2%}")
    
    print("\n" + "="*70 + "\n")
    return True


def show_dashboard(args):
    """Mostrar dashboard del sistema."""
    from src.tools.visualization.dashboard import SimpleDashboard
    
    dashboard = SimpleDashboard()
    dashboard.show_overview()
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Sistema Autónomo de Entrenamiento de Modelos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # 1. Configurar dataset (solo la primera vez)
  python main.py setup --dataset /ruta/a/tu/dataset

  # 2. Entrenar modelo
  python main.py train

  # 3. Ver resultados
  python main.py dashboard
  python main.py evaluate

  # 4. Mejorar modelo (edita config y vuelve a entrenar)
  python main.py train

  # 5. Forzar nueva versión aunque no haya mejora
  python main.py train --force-version
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Setup
    setup_parser = subparsers.add_parser('setup', help='Configurar dataset automáticamente')
    setup_parser.add_argument(
        '--dataset',
        type=str,
        required=True,
        help='Ruta al dataset'
    )
    
    # Train
    train_parser = subparsers.add_parser('train', help='Entrenar modelo')
    train_parser.add_argument(
        '--force-version',
        action='store_true',
        help='Forzar creación de nueva versión'
    )
    
    # Evaluate
    subparsers.add_parser('evaluate', help='Evaluar modelos')
    
    # Dashboard
    subparsers.add_parser('dashboard', help='Ver dashboard del sistema')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Ejecutar comando
    commands = {
        'setup': setup_dataset,
        'train': train_model,
        'evaluate': evaluate_models,
        'dashboard': show_dashboard
    }
    
    success = commands[args.command](args)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()