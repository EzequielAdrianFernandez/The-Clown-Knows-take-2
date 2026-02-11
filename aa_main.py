import pygame
import sys  
from verificaciones_botones import (
    inicializar_pygame, 
    cargar_fondo, 
    verificar_evento_salida
)
from manejador_estados import (
    crear_estado_inicial,
    actualizar_estado_completo,
    dibujar_estado_actual,
    cargar_fuentes,
    obtener_fondo_actual
)
from menu_definiciones import FONDOS  # Importar los fondos
from y_musica import musica_inicializar, dibujar_musica_pantalla , musica_actualizar_completo

def main():
    # Configuración
    ANCHO_PANTALLA, ALTO_PANTALLA = 1000, 700
    FPS = 60

    # Inicialización
    pantalla, reloj = inicializar_pygame(ANCHO_PANTALLA, ALTO_PANTALLA, "El payaso sabe")
    
    # Inicializar sistema de música
    musica_inicializar()
    
    # Cargar todas las imágenes de fondo
    fondos_cargados = {}
    for estado, ruta_fondo in FONDOS.items():
        try:
            fondo = cargar_fondo(ruta_fondo, ANCHO_PANTALLA, ALTO_PANTALLA)
            fondos_cargados[estado] = fondo
            print(f"Fondo cargado: {ruta_fondo}")
        except:
            # Si no se puede cargar, crear un fondo por defecto
            print(f"No se pudo cargar el fondo: {ruta_fondo}")
            fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
            fondo.fill((25, 25, 50))
            fondos_cargados[estado] = fondo
    
    # cargar la fuente que soporta emogis
    fuente = cargar_fuentes()
    
    # Estado del juego
    estado_juego = crear_estado_inicial()
    
    # Bucle principal
    ejecutando = True
    while ejecutando:
        # Procesar eventos
        eventos = pygame.event.get()
        ejecutando = not verificar_evento_salida(eventos)
        
        #Actualizar estado del juego
        estado_juego = actualizar_estado_completo(
            pantalla, fuente, eventos, estado_juego
        )
        # Obtener fondo actual basado en el estado ACTUALIZADO
        estado_actual = estado_juego['estado_actual']
        fondo_actual = obtener_fondo_actual(fondos_cargados, estado_actual)
        
        # Dibujar fondo correspondiente al estado actual
        pantalla.blit(fondo_actual, (0, 0))
        
        # Dibujar controles de música en pantalla
        dibujar_musica_pantalla(pantalla, fuente, estado_juego, ALTO_PANTALLA)

        # Actualizar estado completo del juego (NUEVAMENTE)
        estado_juego = actualizar_estado_completo(
            pantalla, fuente, eventos, estado_juego
        )
        
        # Dibujar estado actual
        dibujar_estado_actual(pantalla, fuente, estado_juego)
        
        # Actualizar pantalla y controlar FPS
        pygame.display.flip()
        reloj.tick(FPS)
    
    # SALIR correctamente
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()