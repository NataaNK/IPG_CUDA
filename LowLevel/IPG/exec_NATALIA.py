import argparse
import sys
import os
import yaml

# Agregar el directorio raíz al sistema de rutas
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from basicsr.models.ipg_model import IPGModel  # Importar el modelo
from basicsr.utils.registry import MODEL_REGISTRY

def update_yaml(input_dir, yaml_path):
    """Actualizar el archivo YAML con el directorio de entrada proporcionado."""
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    # Actualizar el campo 'dataroot_lq'
    if 'datasets' in config and 'test' in config['datasets']:
        config['datasets']['test']['dataroot_lq'] = input_dir

    # Guardar el archivo actualizado
    with open(yaml_path, 'w') as file:
        yaml.safe_dump(config, file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to run inference (test) using BasicSR.")
    parser.add_argument('--opt', type=str, required=True, help='Path to the YAML file for inference.')
    parser.add_argument('--input_dir', type=str, required=True, help='Path to the input directory for images.')
    args = parser.parse_args()

    # Verificar si el archivo YAML proporcionado existe
    if not os.path.isfile(args.opt):
        print(f"Error: No se encontró el archivo YAML: {args.opt}")
        exit(1)

    # Actualizar el archivo YAML con el directorio de entrada
    print(f"Actualizando {args.opt} con el directorio de entrada: {args.input_dir}")
    try:
        update_yaml(args.input_dir, args.opt)
    except Exception as e:
        print(f"Error al actualizar el archivo YAML: {e}")
        exit(1)

    # Verificar si el modelo está registrado
    print("Model registry keys:", MODEL_REGISTRY._obj_map.keys())
    if "IPGModel" not in MODEL_REGISTRY._obj_map:
        print("Error: El modelo 'IPGModel' no está registrado.")
        exit(1)

    # Comando para ejecutar el script de test
    eval_cmd = f'python -m basicsr.test --opt {args.opt}'

    print('=' * 50)
    print(f'Comando de inferencia:\n{eval_cmd}')
    print('=' * 50)

    # Ejecutar el comando de inferencia
    os.system(eval_cmd)

    print('=' * 50)
    print('Inferencia finalizada.')
    print('=' * 50)
