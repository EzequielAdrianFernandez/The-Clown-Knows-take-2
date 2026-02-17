import pygame
import sys

def salir_del_juego():
    """Acción para el botón salir - cierra el juego completamente"""
    print("Saliendo del juego...")
    pygame.quit()
    sys.exit()

def iniciar_juego():
    """Acción para el botón jugar - inicia el juego principal"""
    print("Iniciando juego...")
    # Aquí cambias al estado de juego principal
    return "jugando"

def mostrar_opciones():
    """Acción para el botón opciones - muestra el menú de opciones"""
    print("Mostrando opciones...")
    return "opciones"

def volver_menu_principal():
    """Acción para volver al menú principal"""
    print("Volviendo al menú principal...")
    return "menu_principal"