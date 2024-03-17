"""
Script: clean_django_modules.py

Descripción:

Este script se utiliza EN WINDOWS para limpiar todos los módulos de nuestro proyecto 
antes de ejecutar 'makemigrations' y 'migrate', eliminando archivos residuales 
que pueden interferir con los procesos de migración. 

Concretamente:

1. Elimina la carpeta __pycache__ de cada módulo.
2. Limpia todos los archivos dentro de la carpeta 'migrations' de cada módulo, excepto __init__.py.

Uso:
python clean_django_modules.py
"""
import os
import shutil

def remove_pycache_and_clean_migrations(root_path, modules):
    for module in modules:
        # Ruta del módulo
        module_path = os.path.join(root_path, module)
        print(f"Revisando módulo: {module}")
        pycache_found = False
        migrations_cleaned = False

        # Eliminar cualquier __pycache__ en el módulo y dentro de las subcarpetas
        for root, dirs, files in os.walk(module_path):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                shutil.rmtree(pycache_path)
                print(f"Eliminado: {pycache_path}")
                pycache_found = True

            # Limpiar todos los archivos en migrations excepto __init__.py
            if 'migrations' in root:
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        print(f"Eliminado: {file_path}")
                        migrations_cleaned = True

        # Mensajes de resumen por módulo
        if not pycache_found:
            print(f"No se encontró __pycache__ para eliminar en el módulo {module}.")
        if not migrations_cleaned:
            print(f"No se encontraron archivos en 'migrations' para eliminar en el módulo {module}.")

# Ruta de la carpeta actual donde se encuentra el script
root_path = '.'

# Lista de módulos a limpiar
modules = ['catering_employees', 'catering_owners', 'catering_particular', 'core']

remove_pycache_and_clean_migrations(root_path, modules)
