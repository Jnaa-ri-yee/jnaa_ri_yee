# ======================================================                     *
#  Project      : visualization                                              *
#  File         : dashboard.py                                               *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:11                                           *
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
Dashboard de consola para visualizar el progreso del sistema.
Muestra versiones, experimentos, y mejor modelo actual.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Agregar src al path si es necesario
if str(Path(__file__).parent.parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class SimpleDashboard:
    """Dashboard de consola simple para visualizar progreso del sistema."""
    
    def __init__(self):
        self.version_manager = None
        self.experiment_logger = None
    
    def show_overview(self):
        """
        Muestra un resumen general del sistema:
        - Versiones de modelos
        - Experimentos realizados
        - Mejor modelo actual
        - Estadísticas generales
        """
        print("\n" + "="*70)
        print("DASHBOARD - SISTEMA DE ENTRENAMIENTO AUTÓNOMO")
        print("="*70)
        
        # Verificar si hay datos
        if not self._check_system_initialized():
            print("\nSistema no inicializado aún.")
            print("\nPara comenzar:")
            print("   1. python main.py setup --dataset /tu/dataset")
            print("   2. python main.py train")
            print("\n" + "="*70 + "\n")
            return
        
        # Mostrar secciones
        self._show_versions()
        self._show_experiments()
        self._show_best_model()
        self._show_performance_trend()
        
        print("="*70 + "\n")
    
    def _check_system_initialized(self) -> bool:
        """Verifica si el sistema ha sido inicializado."""
        models_dir = Path('models')
        config_dir = Path('config/generated')
        
        return (
            models_dir.exists() and 
            config_dir.exists() and
            len(list(models_dir.glob('v*'))) > 0
        )
    
    def _show_versions(self):
        """Muestra todas las versiones de modelos."""
        from core.version_manager import VersionManager
        
        try:
            vm = VersionManager()
            
            print("\nVersiones de Modelos:")
            
            if not vm.registry['versions']:
                print("  (No hay versiones aún)")
                return
            
            print(f"  Total: {len(vm.registry['versions'])} versiones")
            print()
            
            # Tabla de versiones
            print(f"  {'Ver':<6} {'Accuracy':<12} {'F1-Score':<12} {'Creado':<20} {'Estado'}")
            print("  " + "-"*60)
            
            best_version = vm.get_best_version()
            
            for version_data in vm.registry['versions']:
                version = version_data['version']
                metrics = version_data['metrics']
                created = version_data['created_at'][:10]  # Solo fecha
                
                acc = metrics.get('test_accuracy', 0)
                f1 = metrics.get('test_f1', 0)
                
                # Marcar la mejor versión
                status = "MEJOR" if version == best_version else ""
                
                print(f"  {version:<6} {acc:<12.4f} {f1:<12.4f} {created:<20} {status}")
            
        except Exception as e:
            print(f"Error cargando versiones: {e}")
    
    def _show_experiments(self):
        """Muestra resumen de experimentos realizados."""
        from core.experiment_logger import ExperimentLogger
        
        try:
            logger = ExperimentLogger()
            summary = logger.get_run_summary()
            
            print(f"\nExperimentos:")
            print(f"  • Total ejecutados: {summary['total_runs']}")
            print(f"  • Exitosos: {summary['completed']}")
            print(f"  • Fallidos: {summary['failed']}")
            
            if summary['total_runs'] > 0:
                print(f"  • Tasa de éxito: {summary['success_rate']:.1f}%")
            
            # Mostrar últimos 3 experimentos
            if logger.runs:
                print(f"\n  Últimos 3 experimentos:")
                for run in logger.runs[-3:]:
                    run_id = run['run_id']
                    status_icon = "✅" if run.get('success') else "❌"
                    version = run.get('version', 'N/A')
                    
                    print(f"    {status_icon} {run_id} → {version}")
        
        except Exception as e:
            print(f"Error cargando experimentos: {e}")
    
    def _show_best_model(self):
        """Muestra información del mejor modelo actual."""
        from core.version_manager import VersionManager
        
        try:
            vm = VersionManager()
            
            best_version = vm.get_best_version()
            
            if not best_version:
                print("\nMejor Modelo:")
                print("  (No hay modelos aún)")
                return
            
            version_info = vm.get_version_info(best_version)
            metrics = version_info['metrics']
            model_info = version_info['model_info']
            
            print(f"\nMejor Modelo: {best_version}")
            print(f"\n  Métricas:")
            print(f"    • Accuracy:  {metrics['test_accuracy']:.4f} ({metrics['test_accuracy']*100:.2f}%)")
            print(f"    • Precision: {metrics['test_precision']:.4f}")
            print(f"    • Recall:    {metrics['test_recall']:.4f}")
            print(f"    • F1-Score:  {metrics['test_f1']:.4f}")
            
            print(f"\n  Arquitectura:")
            print(f"    • Tipo: {model_info['architecture']}")
            print(f"    • Backbone: {model_info['backbone']}")
            print(f"    • Parámetros: {model_info['total_params']:,}")
            
            print(f"\n  Ubicación:")
            print(f"    • Modelo: models/{best_version}/final/model.pth")
            print(f"    • Evaluación: evaluation/{best_version}/")
        
        except Exception as e:
            print(f"Error cargando mejor modelo: {e}")
    
    def _show_performance_trend(self):
        """Muestra tendencia de rendimiento a través de las versiones."""
        from core.version_manager import VersionManager
        
        try:
            vm = VersionManager()
            
            if len(vm.registry['versions']) < 2:
                return  # No hay suficientes versiones para mostrar tendencia
            
            print(f"\nTendencia de Rendimiento:")
            
            versions = vm.registry['versions']
            
            # Calcular mejora desde v1 hasta última versión
            v1_acc = versions[0]['metrics']['test_accuracy']
            latest_acc = versions[-1]['metrics']['test_accuracy']
            improvement = latest_acc - v1_acc
            improvement_pct = (improvement / v1_acc * 100) if v1_acc > 0 else 0
            
            if improvement > 0:
                print(f"Mejora desde v1: +{improvement:.4f} (+{improvement_pct:.2f}%)")
            elif improvement < 0:
                print(f"Regresión desde v1: {improvement:.4f} ({improvement_pct:.2f}%)")
            else:
                print(f"Sin cambio desde v1")
            
            # Gráfico ASCII simple de últimas 5 versiones
            last_5 = versions[-5:]
            if len(last_5) > 1:
                print(f"\n  Últimas {len(last_5)} versiones:")
                
                accs = [v['metrics']['test_accuracy'] for v in last_5]
                min_acc = min(accs)
                max_acc = max(accs)
                range_acc = max_acc - min_acc if max_acc > min_acc else 0.01
                
                for v in last_5:
                    version = v['version']
                    acc = v['metrics']['test_accuracy']
                    
                    # Normalizar para gráfico ASCII
                    normalized = int(((acc - min_acc) / range_acc) * 30)
                    bar = "█" * normalized
                    
                    print(f"    {version}: {bar} {acc:.4f}")
        
        except Exception as e:
            print(f"Error calculando tendencia: {e}")
    
    def show_class_performance(self, version: Optional[str] = None):
        """
        Muestra rendimiento por clase para una versión específica.
        
        Args:
            version: Versión a analizar (None = mejor versión)
        """
        from core.version_manager import VersionManager
        
        try:
            vm = VersionManager()
            
            if version is None:
                version = vm.get_best_version()
            
            if not version:
                print("No hay versiones disponibles")
                return
            
            # Cargar análisis de errores
            error_analysis_path = Path(f'evaluation/{version}/analysis/error_analysis.json')
            
            if not error_analysis_path.exists():
                print(f"No se encontró análisis para {version}")
                return
            
            with open(error_analysis_path) as f:
                analysis = json.load(f)
            
            print("\n" + "="*70)
            print(f"RENDIMIENTO POR CLASE - {version}")
            print("="*70)
            
            errors_per_class = analysis['errors_per_class']
            
            # Ordenar por accuracy (de menor a mayor)
            sorted_classes = sorted(
                errors_per_class.items(),
                key=lambda x: x[1]['accuracy']
            )
            
            print(f"\n{'Clase':<30} {'Accuracy':<12} {'Muestras':<10} {'Errores'}")
            print("-"*70)
            
            for class_name, data in sorted_classes:
                acc = data['accuracy']
                samples = data['total_samples']
                errors = data['errors']
                
                # Barra visual de accuracy
                bar_length = int(acc * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                
                print(f"{class_name:<30} {bar} {acc:.2%}  ({errors}/{samples})")
            
            # Resumen
            print("\n" + "-"*70)
            print(f"Resumen:")
            
            all_accs = [data['accuracy'] for data in errors_per_class.values()]
            print(f"  • Accuracy promedio: {sum(all_accs)/len(all_accs):.2%}")
            print(f"  • Accuracy mínima: {min(all_accs):.2%}")
            print(f"  • Accuracy máxima: {max(all_accs):.2%}")
            
            print("\n" + "="*70 + "\n")
        
        except Exception as e:
            print(f"Error: {e}")
    
    def show_confusion_pairs(self, version: Optional[str] = None, top_k: int = 5):
        """
        Muestra los pares de clases que más se confunden.
        
        Args:
            version: Versión a analizar
            top_k: Número de pares a mostrar
        """
        from core.version_manager import VersionManager
        
        try:
            vm = VersionManager()
            
            if version is None:
                version = vm.get_best_version()
            
            error_analysis_path = Path(f'evaluation/{version}/analysis/error_analysis.json')
            
            if not error_analysis_path.exists():
                print(f"No se encontró análisis para {version}")
                return
            
            with open(error_analysis_path) as f:
                analysis = json.load(f)
            
            confusion_pairs = analysis['confusion_pairs'][:top_k]
            
            print("\n" + "="*70)
            print(f"TOP {top_k} CONFUSIONES - {version}")
            print("="*70)
            
            if not confusion_pairs:
                print("\nNo hay confusiones significativas!")
                print("\n" + "="*70 + "\n")
                return
            
            print(f"\n{'#':<4} {'Verdadera':<20} {'→':<3} {'Predicha':<20} {'Veces':<8} {'%'}")
            print("-"*70)
            
            for i, pair in enumerate(confusion_pairs, 1):
                true_class = pair['true_class']
                pred_class = pair['predicted_class']
                count = pair['count']
                pct = pair['percentage']
                
                print(f"{i:<4} {true_class:<20} → {pred_class:<20} {count:<8} {pct:.1f}%")
            
            print("\n" + "="*70 + "\n")
        
        except Exception as e:
            print(f"Error: {e}")