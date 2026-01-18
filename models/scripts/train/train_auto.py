# ======================================================                     *
#  Project      : train                                                      *
#  File         : train_auto.py                                              *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:51                                           *
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
Script de entrenamiento automático con versionado.
Este es el script legacy, usa mejor: python main.py train
"""

import sys
import yaml
from pathlib import Path
import argparse
import torch
import json
import numpy as np

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from data.loaders.universal_loader import create_data_loaders
from algorithms.deep.simple_hybrid_model import SimpleHybridModel
from training.deep.hybrid_trainer import HybridTrainer
from core.version_manager import VersionManager
from core.experiment_logger import ExperimentLogger
from metrics.analysis.error_analyzer import ErrorAnalyzer


def main():
    parser = argparse.ArgumentParser(description='Entrenamiento automático con versionado')
    parser.add_argument(
        '--config',
        type=str,
        default='config/generated/auto_generated_config.yaml',
        help='Ruta a la configuración generada'
    )
    parser.add_argument(
        '--data-config',
        type=str,
        default='config/generated/data_loaders_config.yaml',
        help='Ruta a la configuración de data loaders'
    )
    parser.add_argument(
        '--force-version',
        action='store_true',
        help='Forzar creación de nueva versión aunque no haya mejora'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("SISTEMA DE ENTRENAMIENTO AUTOMÁTICO")
    print("="*70)
    
    # 1. Cargar configuración
    print("\nCargando configuración...")
    
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: No se encontró {config_path}")
        print("   Ejecuta primero: python main.py setup --dataset /ruta/dataset")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"Configuración cargada")
    
    # 2. Iniciar logging de experimento
    experiment_logger = ExperimentLogger()
    run_id = experiment_logger.start_run(config)
    print(f"Run ID: {run_id}")
    
    try:
        # 3. Crear data loaders
        print("\nPreparando datos...")
        loaders = create_data_loaders(
            config_path=args.data_config,
            batch_size=config['dataset']['batch_size'],
            num_workers=config['dataset']['num_workers'],
            extract_landmarks=config['features']['landmarks']['enabled']
        )
        
        print(f"  ✓ Train: {len(loaders['train'].dataset)} muestras")
        print(f"  ✓ Val: {len(loaders['val'].dataset)} muestras")
        print(f"  ✓ Test: {len(loaders['test'].dataset)} muestras")
        
        # 4. Crear modelo
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
        
        # 5. Entrenar
        print("\n" + "="*70)
        trainer = HybridTrainer(
            model=model,
            train_loader=loaders['train'],
            val_loader=loaders['val'],
            test_loader=loaders['test'],
            config=config
        )
        
        results = trainer.train()
        
        # 6. Análisis de errores
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
        
        # 7. Gestionar versión
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
            force=args.force_version
        )
        
        if version_name:
            # Guardar modelo y artefactos
            version_dir = Path('models') / version_name
            eval_dir = Path('evaluation') / version_name
            
            trainer.save_model(version_dir / 'final' / 'model.pth')
            
            # Config
            with open(version_dir / 'config' / 'training_config.yaml', 'w') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            # Métricas
            metrics_dir = eval_dir / 'metrics'
            metrics_dir.mkdir(parents=True, exist_ok=True)
            
            metrics_to_save = {
                k: v for k, v in results['test_metrics'].items()
                if k not in ['predictions', 'labels', 'probabilities']
            }
            
            with open(metrics_dir / 'test_metrics.json', 'w') as f:
                json.dump(metrics_to_save, f, indent=2)
            
            # Análisis
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
            
            # Resumen
            print("\n" + "="*70)
            print("ENTRENAMIENTO COMPLETADO")
            print("="*70)
            print(f"\nVersión: {version_name}")
            print(f"Modelo: models/{version_name}/final/model.pth")
            print(f"Evaluación: evaluation/{version_name}/")
            print(f"\nMétricas:")
            print(f"  • Test Accuracy: {results['test_metrics']['test_accuracy']:.4f}")
            print(f"  • Test F1-Score: {results['test_metrics']['test_f1']:.4f}")
            
            best_version = version_manager.get_best_version()
            print(f"\nMejor versión: {best_version}")
            
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
        print(f"\nError durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()
        
        experiment_logger.end_run(
            run_id=run_id,
            results={},
            version=None,
            success=False
        )
        return False


if __name__ == '__main__':
    import numpy as np
    success = main()
    sys.exit(0 if success else 1)
