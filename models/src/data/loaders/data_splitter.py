# ======================================================                     *
#  Project      : loaders                                                    *
#  File         : data_splitter.py                                           *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 16:30                                           *
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
Split automático de datos en train/val/test.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import random
import yaml


class AutoDataSplitter:
    """Split automático de datos manteniendo distribución de clases."""
    
    def __init__(
        self,
        data_config: Dict,
        split_ratios: Dict = None,
        seed: int = 42
    ):
        if split_ratios is None:
            split_ratios = {'train': 0.7, 'val': 0.15, 'test': 0.15}
        
        self.data_config = data_config
        self.split_ratios = split_ratios
        self.seed = seed
        random.seed(seed)
        
        # Validar ratios
        total = sum(split_ratios.values())
        assert abs(total - 1.0) < 0.01, f"Split ratios must sum to 1.0, got {total}"
    
    def split(self) -> Dict[str, List]:
        """Realiza el split estratificado de datos."""
        splits = {'train': [], 'val': [], 'test': []}
        
        # Agrupar por clase
        files_by_class = {}
        for class_data in self.data_config['data_paths']:
            class_idx = class_data['class_idx']
            class_path = Path(class_data['path'])
            
            files = []
            for file_name in class_data['files']:
                file_path = class_path / file_name
                if file_path.exists():
                    files.append((str(file_path), class_idx))
            
            if files:
                files_by_class[class_idx] = files
        
        # Split por clase
        for class_idx, files in files_by_class.items():
            random.shuffle(files)
            
            n_files = len(files)
            n_train = int(n_files * self.split_ratios['train'])
            n_val = int(n_files * self.split_ratios['val'])
            
            if n_files >= 3:
                n_train = max(1, n_train)
                n_val = max(1, n_val)
                n_test = max(1, n_files - n_train - n_val)
            elif n_files == 2:
                n_train = 1
                n_val = 0
                n_test = 1
            else:
                n_train = 1
                n_val = 0
                n_test = 0
            
            splits['train'].extend(files[:n_train])
            splits['val'].extend(files[n_train:n_train + n_val])
            splits['test'].extend(files[n_train + n_val:])
        
        # Shuffle final
        for split_data in splits.values():
            random.shuffle(split_data)
        
        return splits
    
    def get_split_info(self, splits: Dict) -> Dict:
        """Información sobre el split."""
        total = sum(len(v) for v in splits.values())
        
        info = {
            'total_samples': total,
            'splits': {}
        }
        
        for split_name, split_data in splits.items():
            info['splits'][split_name] = {
                'num_samples': len(split_data),
                'percentage': len(split_data) / total * 100 if total > 0 else 0
            }
        
        return info