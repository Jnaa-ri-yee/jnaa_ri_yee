# ======================================================                     *
#  Project      : core                                                       *
#  File         : experiment_logger.py                                       *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 20:51                                           *
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
Logger automático de experimentos.
Registra todos los entrenamientos y sus resultados.
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class NumpyEncoder(json.JSONEncoder):
    """Encoder personalizado para manejar tipos de NumPy."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        return super(NumpyEncoder, self).default(obj)


class ExperimentLogger:
    """Registra automáticamente todos los experimentos."""
    
    def __init__(self, log_dir: str = 'history/experiments'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.all_runs_path = self.log_dir / 'all_runs.json'
        self.runs = self._load_runs()
    
    def _convert_numpy_types(self, obj):
        """
        Convierte recursivamente tipos NumPy a tipos nativos de Python.
        
        Args:
            obj: Objeto a convertir (puede ser dict, list, numpy type, etc.)
        
        Returns:
            Objeto con tipos nativos de Python
        """
        if isinstance(obj, dict):
            return {k: self._convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_numpy_types(item) for item in obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        else:
            return obj
    
    def _load_runs(self) -> List[Dict]:
        """Carga el historial de runs."""
        if self.all_runs_path.exists():
            with open(self.all_runs_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_runs(self):
        """Guarda el historial de runs."""
        # CAMBIO CRÍTICO: Convertir tipos NumPy antes de guardar
        runs_converted = self._convert_numpy_types(self.runs)
        
        with open(self.all_runs_path, 'w', encoding='utf-8') as f:
            # CAMBIO CRÍTICO: Usa NumpyEncoder para serializar
            json.dump(runs_converted, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    
    def start_run(self, config: Dict) -> str:
        """
        Inicia un nuevo experimento.
        
        Args:
            config: Configuración del experimento
            
        Returns:
            run_id: ID único del experimento
        """
        run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # CAMBIO CRÍTICO: Convertir config antes de guardar
        config_converted = self._convert_numpy_types(config)
        
        run_info = {
            'run_id': run_id,
            'started_at': datetime.now().isoformat(),
            'config': config_converted,
            'status': 'running'
        }
        
        self.runs.append(run_info)
        self._save_runs()
        
        print(f"Experimento iniciado: {run_id}")
        
        return run_id
    
    def end_run(
        self,
        run_id: str,
        results: Dict,
        version: Optional[str] = None,
        success: bool = True
    ):
        """
        Finaliza un experimento.
        
        Args:
            run_id: ID del experimento
            results: Resultados del experimento
            version: Versión creada (si aplica)
            success: Si el experimento fue exitoso
        """
        # CAMBIO CRÍTICO: Convertir results antes de guardar
        results_converted = self._convert_numpy_types(results)
        
        for run in self.runs:
            if run['run_id'] == run_id:
                run['ended_at'] = datetime.now().isoformat()
                run['results'] = results_converted
                run['version'] = version
                run['status'] = 'completed' if success else 'failed'
                run['success'] = success
                
                # Calcular duración
                start_time = datetime.fromisoformat(run['started_at'])
                end_time = datetime.fromisoformat(run['ended_at'])
                duration = (end_time - start_time).total_seconds()
                run['duration_seconds'] = float(duration)
                run['duration_minutes'] = float(duration / 60)
                
                break
        
        self._save_runs()
        
        status_emoji = "✅" if success else "❌"
        print(f"{status_emoji} Experimento finalizado: {run_id}")
        if success and version:
            print(f"Versión: {version}")
    
    def get_best_runs(self, metric: str = 'test_accuracy', top_k: int = 5) -> List[Dict]:
        """
        Obtiene los mejores K experimentos.
        
        Args:
            metric: Métrica para ordenar
            top_k: Número de experimentos a retornar
            
        Returns:
            Lista de los mejores experimentos
        """
        completed_runs = [r for r in self.runs if r.get('success', False)]
        
        if not completed_runs:
            return []
        
        # Función para extraer el valor de la métrica de forma segura
        def get_metric_value(run):
            results = run.get('results', {})
            value = results.get(metric, 0)
            # Convertir a float si es necesario
            try:
                return float(value) if value is not None else 0.0
            except (TypeError, ValueError):
                return 0.0
        
        sorted_runs = sorted(
            completed_runs,
            key=get_metric_value,
            reverse=True
        )
        
        return sorted_runs[:top_k]
    
    def get_run_summary(self) -> Dict:
        """
        Resumen de todos los experimentos.
        
        Returns:
            Dict con estadísticas de experimentos
        """
        total = len(self.runs)
        completed = len([r for r in self.runs if r.get('status') == 'completed'])
        failed = len([r for r in self.runs if r.get('status') == 'failed'])
        running = len([r for r in self.runs if r.get('status') == 'running'])
        
        best_run = None
        if completed > 0:
            completed_runs = [r for r in self.runs if r.get('success', False)]
            if completed_runs:
                best_run = max(
                    completed_runs,
                    key=lambda r: float(r.get('results', {}).get('test_accuracy', 0))
                )
        
        return {
            'total_runs': total,
            'completed': completed,
            'failed': failed,
            'running': running,
            'success_rate': float((completed / total * 100) if total > 0 else 0),
            'best_run_id': best_run['run_id'] if best_run else None,
            'best_accuracy': float(best_run.get('results', {}).get('test_accuracy', 0)) if best_run else 0.0
        }
    
    def get_run_by_id(self, run_id: str) -> Optional[Dict]:
        """
        Obtiene información de un run específico.
        
        Args:
            run_id: ID del experimento
            
        Returns:
            Información del run o None si no existe
        """
        for run in self.runs:
            if run['run_id'] == run_id:
                return run
        return None
    
    def compare_runs(self, run_ids: List[str]) -> Dict:
        """
        Compara múltiples experimentos.
        
        Args:
            run_ids: Lista de IDs de runs a comparar
            
        Returns:
            Diccionario con la comparación
        """
        runs = [self.get_run_by_id(rid) for rid in run_ids]
        runs = [r for r in runs if r is not None]
        
        if not runs:
            return {'error': 'No se encontraron runs válidos'}
        
        comparison = {
            'runs': run_ids,
            'metrics': {},
            'configs': {}
        }
        
        # Extraer todas las métricas únicas
        all_metrics = set()
        for run in runs:
            if 'results' in run:
                all_metrics.update(run['results'].keys())
        
        # Comparar métricas
        for metric in all_metrics:
            comparison['metrics'][metric] = {}
            for run in runs:
                run_id = run['run_id']
                value = run.get('results', {}).get(metric, None)
                if value is not None:
                    comparison['metrics'][metric][run_id] = float(value)
        
        # Comparar configuraciones clave
        config_keys = ['architecture', 'learning_rate', 'batch_size', 'epochs']
        for key in config_keys:
            comparison['configs'][key] = {}
            for run in runs:
                run_id = run['run_id']
                value = run.get('config', {}).get(key, None)
                if value is not None:
                    comparison['configs'][key][run_id] = value
        
        return comparison
    
    def export_to_csv(self, output_path: str = 'experiments_summary.csv'):
        """
        Exporta el historial de experimentos a CSV.
        
        Args:
            output_path: Ruta del archivo CSV de salida
        """
        import csv
        
        if not self.runs:
            print("No hay experimentos para exportar")
            return
        
        # Preparar datos
        fieldnames = [
            'run_id', 'status', 'success', 'started_at', 'ended_at',
            'duration_minutes', 'version', 'test_accuracy', 'test_f1',
            'train_accuracy', 'val_accuracy'
        ]
        
        output_file = self.log_dir / output_path
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for run in self.runs:
                row = {
                    'run_id': run['run_id'],
                    'status': run.get('status', 'unknown'),
                    'success': run.get('success', False),
                    'started_at': run.get('started_at', ''),
                    'ended_at': run.get('ended_at', ''),
                    'duration_minutes': run.get('duration_minutes', 0),
                    'version': run.get('version', ''),
                }
                
                # Agregar métricas si existen
                results = run.get('results', {})
                row['test_accuracy'] = results.get('test_accuracy', '')
                row['test_f1'] = results.get('test_f1', '')
                row['train_accuracy'] = results.get('train_accuracy', '')
                row['val_accuracy'] = results.get('val_accuracy', '')
                
                writer.writerow(row)
        
        print(f"Experimentos exportados a: {output_file}")
    
    def clean_failed_runs(self):
        """Elimina runs fallidos del historial."""
        initial_count = len(self.runs)
        self.runs = [r for r in self.runs if r.get('status') != 'failed']
        removed = initial_count - len(self.runs)
        
        if removed > 0:
            self._save_runs()
            print(f"Eliminados {removed} experimentos fallidos")
        else:
            print("No hay experimentos fallidos para eliminar")
    
    def print_summary(self):
        """Imprime un resumen bonito de los experimentos."""
        summary = self.get_run_summary()
        
        print("\n" + "="*60)
        print("RESUMEN DE EXPERIMENTOS")
        print("="*60)
        print(f"Total de experimentos:    {summary['total_runs']}")
        print(f"Completados:         {summary['completed']}")
        print(f"Fallidos:            {summary['failed']}")
        print(f"En ejecución:        {summary['running']}")
        print(f"Tasa de éxito:       {summary['success_rate']:.1f}%")
        
        if summary['best_run_id']:
            print(f"\nMejor experimento:      {summary['best_run_id']}")
            print(f"   Accuracy:               {summary['best_accuracy']:.4f}")
        
        print("="*60 + "\n")