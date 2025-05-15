#!/usr/bin/env python3
import os
import sys
from views.main_view import MainView
from controllers.network_controller import NetworkController
# sudo "/home/arthur/Documents/proyectos/monitoreo de red/.venv/bin/python" "/home/arthur/Documents/proyectos/monitoreo de red/monitor_red.py"
def check_permissions():
    """Verifica los permisos necesarios para la captura de paquetes."""
    if sys.platform != "win32":
        try:
            if os.geteuid() != 0:
                print("\n" + "="*60)
                print(" ADVERTENCIA DE PERMISOS ".center(60, "="))
                print(" Este script necesita privilegios de superusuario (root) para")
                print(" capturar paquetes de red en modo promiscuo.")
                print(" Por favor, ejecútalo usando 'sudo':")
                print(f"   sudo {sys.executable} {os.path.abspath(__file__)}")
                print(" Es posible que funcione sin sudo, pero podría no capturar")
                print(" todo el tráfico o fallar al iniciar la captura.")
                print("="*60 + "\n")
        except AttributeError:
            print("Advertencia: No se pudo verificar el ID de usuario.")
            print("Asegúrate de ejecutar con permisos adecuados si la captura falla.")

def main():
    """Punto de entrada principal de la aplicación."""
    # Verificar permisos al inicio
    check_permissions()

    try:
        # Crear la vista principal
        view = MainView()
        
        # Crear el controlador
        controller = NetworkController(view)
        
        # Iniciar la aplicación
        view.mainloop()
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
    except Exception as e:
        import traceback
        print(f"\nERROR inesperado: {type(e).__name__}: {e}")
        traceback.print_exc()
    finally:
        print("\nAplicación finalizada.")

if __name__ == "__main__":
    main()