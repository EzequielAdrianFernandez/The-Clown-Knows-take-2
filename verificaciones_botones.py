import pygame
import sys

def verificar_evento_salida(eventos):
    """
    Verifica si hay eventos de salida del juego
    """
    for i in range(len(eventos)):
        evento = eventos[i]
        if evento.type == pygame.QUIT:
            return True
    return False

def obtener_botones_presionados(diccionario_botones):
    """
    Obtiene lista de IDs de botones que han sido presionados
    """
    botones_presionados = []
    claves_botones = list(diccionario_botones.keys())
    
    for i in range(len(claves_botones)):
        boton_id = claves_botones[i]
        boton_data = diccionario_botones[boton_id]
        
        if 'presionado' in boton_data and boton_data['presionado']:
            botones_presionados.append(boton_id)
    
    return botones_presionados

def procesar_todas_acciones(botones_presionados, estado_actual, diccionario_actual):
    """
    Procesa todas las acciones de botones presionados
    """
    nuevo_estado = estado_actual
    nuevo_diccionario = diccionario_actual
    
    for i in range(len(botones_presionados)):
        boton_id = botones_presionados[i]
        nuevo_estado, nuevo_diccionario = ejecutar_accion_boton(
            boton_id, nuevo_estado, nuevo_diccionario
        )
    
    return nuevo_estado, nuevo_diccionario

def inicializar_pygame(ancho, alto, titulo):
    """
    Inicializa pygame y retorna la pantalla y el reloj
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(titulo)
    reloj = pygame.time.Clock()
    return pantalla, reloj

def cargar_fondo(ruta_imagen, ancho, alto):
    """
    Carga y escala la imagen de fondo
    """
    try:
        fondo = pygame.image.load(ruta_imagen)
        return pygame.transform.scale(fondo, (ancho, alto))
    except pygame.error:
        print(f"No se pudo cargar la imagen: {ruta_imagen}")
        # Crear un fondo por defecto
        fondo = pygame.Surface((ancho, alto))
        fondo.fill((25, 25, 50))
        return fondo

def ejecutar_accion_boton(boton_id, estado_actual, diccionario_actual):
    """
    Maneja todas las acciones de botones - versión simplificada
    """
    from menu_definiciones import (MENU_LEADERBOARD,MENU_PRINCIPAL, MENU_OPCIONES, MENU_JUEGO_PREGUNTA, MENU_SELECCION_USUARIO, MENU_JUEGO_PREGUNTA_VoF, MENU_SELECCION_DIFICULTAD_LABERINTO,MENU_LABERINTO_JUEGO, MENU_TIENDA)
    
    match boton_id:
        # === BOTONES DE NAVEGACIÓN PRINCIPAL ===
        case 'boton_salir':  # Solo el botón del menú principal
            pygame.quit()
            sys.exit()

        case 'boton_volver_menu':  # Nuevo ID para volver al menú
            print("Volviendo al menú principal...")
            return "menu_principal", MENU_PRINCIPAL
        # === BOTONES DE CONFIGURACIÓN ===
        case 'boton_sonido' | 'boton_dificultad':
            print(f"Configurando {boton_id}...")
            return estado_actual, diccionario_actual

        # === BOTONES DE NAVEGACIÓN PRINCIPAL ===
        case 'boton_jugar' if estado_actual == "menu_principal":
            print("Iniciando juego Multiple Choice...")
            return "juego_pregunta", MENU_JUEGO_PREGUNTA

        case 'boton_jugar_VoF' if estado_actual == "menu_principal":
            print("Iniciando juego Verdadero o Falso...")
            return "juego_pregunta_VoF", MENU_JUEGO_PREGUNTA_VoF

        case 'boton_seleccion_usuario' if estado_actual == "menu_principal":
            print("Seleccionando usuario...")
            return "seleccion_usuario", MENU_SELECCION_USUARIO
        # === MENU DE OPCIONES === #
        case 'boton_opciones' if estado_actual == "menu_principal":
            print("Abriendo opciones...")
            return "opciones", MENU_OPCIONES

        case 'boton_sonido' if estado_actual == "opciones":
            # Este botón ahora manejará el mute/unmute
            # La lógica se manejará en manejador_estados.py
            return estado_actual, diccionario_actual

        # === BOTONES DE SELECCIÓN DE USUARIO ===
        case 'boton_volver' if estado_actual == "seleccion_usuario":
            print("Volviendo al menú principal...")
            return "menu_principal", MENU_PRINCIPAL

        # === BOTONES DE USUARIOS EXISTENTES ===
        case 'boton_usuario_1' | 'boton_usuario_2' | 'boton_usuario_3' | 'boton_usuario_4' |'boton_usuario_5' | 'boton_usuario_6' | 'boton_usuario_7' | 'boton_usuario_8' |'boton_usuario_9' | 'boton_usuario_10':
            # Estos se manejan en manejador_estados.py
            return estado_actual, diccionario_actual

        # === BOTONES DE CREACIÓN DE USUARIO ===
        case 'boton_confirmar' if estado_actual == "crear_usuario":
            # La lógica de creación se maneja en manejador_estados
            return estado_actual, diccionario_actual

        case 'boton_volver' if estado_actual == "crear_usuario":
            print("Volviendo a selección de usuario...")
            return "seleccion_usuario", MENU_SELECCION_USUARIO
        # === BOTONES DE VOLVER ===
        case 'boton_volver' if estado_actual == "opciones":
            print("Volviendo al menú principal desde opciones...")
            return "menu_principal", MENU_PRINCIPAL
        
        # === BOTONES DE RESPUESTA (manejados en manejador_estados) ===
        case 'boton_opcion_1' | 'boton_opcion_2' | 'boton_opcion_3' | 'boton_opcion_4':
            # Estos se manejan en manejador_estados.py
            return estado_actual, diccionario_actual
        
        # === BOTONES DE CONTINUACIÓN (manejados en manejador_estados) ===
        case 'boton_continuar' | 'boton_menu_principal':
            # Estos se manejan en manejador_estados.py
            return estado_actual, diccionario_actual
        
        # === BOTÓN NUEVO LABERINTO EN MENÚ PRINCIPAL ===
        case 'boton_laberinto' if estado_actual == "menu_principal":
            print("Iniciando selección de dificultad laberinto...")
            return "seleccion_dificultad_laberinto", MENU_SELECCION_DIFICULTAD_LABERINTO
        
        # === BOTONES DE DIFICULTAD LABERINTO ===
        case 'boton_facil' if estado_actual == "seleccion_dificultad_laberinto":
            print("Iniciando laberinto fácil (10x15)...")
            return "laberinto_juego", MENU_LABERINTO_JUEGO
        
        case 'boton_medio' if estado_actual == "seleccion_dificultad_laberinto":
            print("Iniciando laberinto medio (10x18)...")
            return "laberinto_juego", MENU_LABERINTO_JUEGO
        
        case 'boton_dificil' if estado_actual == "seleccion_dificultad_laberinto":
            print("Iniciando laberinto difícil (12x18)...")
            return "laberinto_juego", MENU_LABERINTO_JUEGO
        
        case 'boton_deathrow' if estado_actual == "seleccion_dificultad_laberinto":
            print("Iniciando laberinto deathrow (12x22)...")
            return "laberinto_juego", MENU_LABERINTO_JUEGO
        
        case 'boton_volver' if estado_actual == "seleccion_dificultad_laberinto":
            print("Volviendo al menú principal...")
            return "menu_principal", MENU_PRINCIPAL

        # === BOTONES DE COMPRA DE MEDALLAS === #
        case 'boton_tienda' if estado_actual == "menu_principal":
            print("Abriendo tienda de medallas...")
            return "tienda", MENU_TIENDA

        case 'boton_volver' if estado_actual == "tienda":
            print("Volviendo al menú principal desde tienda...")
            return "menu_principal", MENU_PRINCIPAL

        case boton_id if boton_id.startswith('boton_medalla_'):
            return estado_actual, diccionario_actual

        # === BOTONES DE LEADERBOARD ===
        case 'boton_leaderboard' if estado_actual == "menu_principal":
            print("Abriendo leaderboard...")
            return "leaderboard", MENU_LEADERBOARD

        case 'boton_volver' if estado_actual == "leaderboard":
            print("Volviendo al menú principal desde leaderboard...")
            return "menu_principal", MENU_PRINCIPAL

        # === CASO POR DEFECTO ===
        case _:
            print(f"Botón {boton_id} no manejado en estado {estado_actual}")
            return estado_actual, diccionario_actual
