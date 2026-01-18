# fix_imports.py - Script para corregir todos los imports automáticamente
"""
Ejecuta este script para corregir todos los imports de typing en tu proyecto.

Uso:
    python fix_imports.py
"""

import os
import re
from pathlib import Path


def fix_file_imports(filepath):
    """Corrige los imports de typing en un archivo."""
    
    if not os.path.exists(filepath):
        print(f"{filepath} no existe, saltando...")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Detectar qué type hints se usan
    type_hints_needed = set()
    
    patterns = {
        'Dict': r'(:\s*Dict[\[\s]|->\s*Dict[\[\s])',
        'List': r'(:\s*List[\[\s]|->\s*List[\[\s])',
        'Optional': r'(:\s*Optional[\[\s]|->\s*Optional[\[\s])',
        'Tuple': r'(:\s*Tuple[\[\s]|->\s*Tuple[\[\s])',
        'Any': r'(:\s*Any[\[\s]|->\s*Any[\[\s])',
    }
    
    for type_name, pattern in patterns.items():
        if re.search(pattern, content):
            type_hints_needed.add(type_name)
    
    if not type_hints_needed:
        print(f"✓ {filepath} - No necesita type hints")
        return True
    
    # Verificar si ya tiene el import correcto
    import_match = re.search(r'from typing import ([^\n]+)', content)
    
    if import_match:
        # Ya tiene import, verificar si está completo
        current_imports = set(
            item.strip() 
            for item in import_match.group(1).split(',')
        )
        
        if type_hints_needed.issubset(current_imports):
            print(f"✓ {filepath} - Imports correctos")
            return True
        
        # Actualizar import existente
        all_imports = sorted(current_imports | type_hints_needed)
        new_import_line = f"from typing import {', '.join(all_imports)}"
        
        content = re.sub(
            r'from typing import [^\n]+',
            new_import_line,
            content
        )
        
    else:
        # No tiene import de typing, agregarlo después de los imports estándar
        sorted_imports = sorted(type_hints_needed)
        new_import_line = f"from typing import {', '.join(sorted_imports)}"
        
        # Buscar dónde insertar (después del último import)
        import_section_end = 0
        for match in re.finditer(r'^(import |from )', content, re.MULTILINE):
            import_section_end = content.find('\n', match.end())
        
        if import_section_end > 0:
            # Insertar después de los imports
            content = (
                content[:import_section_end + 1] +
                new_import_line + '\n' +
                content[import_section_end + 1:]
            )
        else:
            # No hay imports, agregar al inicio después del docstring
            docstring_end = 0
            if content.startswith('"""') or content.startswith("'''"):
                quote = '"""' if content.startswith('"""') else "'''"
                second_quote = content.find(quote, 3)
                if second_quote != -1:
                    docstring_end = second_quote + 3
            
            content = (
                content[:docstring_end] +
                '\n\n' + new_import_line + '\n' +
                content[docstring_end:]
            )
    
    # Guardar archivo corregido
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{filepath} - Corregido: {', '.join(sorted(type_hints_needed))}")
    return True


def main():
    """Corrige todos los archivos del proyecto."""
    
    files_to_fix = [
        'src/core/dataset_discovery.py',
        'src/core/auto_config_generator.py',
        'src/core/version_manager.py',
        'src/core/experiment_logger.py',
        'src/data/loaders/universal_loader.py',
        'src/data/loaders/data_splitter.py',
        'src/algorithms/deep/simple_hybrid_model.py',
        'src/training/deep/hybrid_trainer.py',
        'src/metrics/analysis/error_analyzer.py',
        'src/tools/visualization/dashboard.py',
        'src/tools/utils/file_utils.py',
    ]
    
    print("="*60)
    print("🔧 CORRECTOR AUTOMÁTICO DE IMPORTS")
    print("="*60)
    print()
    
    all_ok = True
    for filepath in files_to_fix:
        if not fix_file_imports(filepath):
            all_ok = False
    
    print()
    print("="*60)
    if all_ok:
        print("TODOS LOS ARCHIVOS CORREGIDOS")
        print()
        print("Prueba ahora:")
        print('  python -c "from src.core import DatasetDiscovery, VersionManager, ExperimentLogger; print(\'OK\')"')
    else:
        print("Algunos archivos no pudieron ser corregidos")
    print("="*60)


if __name__ == '__main__':
    main()