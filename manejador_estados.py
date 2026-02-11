"""
🎮 MÓDULO: manejador_estados.py
===============================
CORAZÓN DEL SISTEMA DE ESTADOS DEL JUEGO.

¿QUÉ HACE ESTE MÓDULO?
----------------------------------------------------------------------------
1. 🎬 crear_estado_inicial()      → Construye el estado global del juego
2. 🔄 actualizar_estado_completo() → Bucle principal de actualización
3. 🖌️ dibujar_estado_actual()     → Renderiza cada estado según corresponda
4. 🧠 manejar_logica_estado_actual() → Lógica específica por estado
5. 🏪 crear_botones_tienda_dinamicos() → Genera botones de medallas según disponibilidad
6. 🎵 Funciones de música        → Cambian música según estado

ESTRUCTURA DEL ESTADO (diccionario):
----------------------------------------------------------------------------
{
    'estado_actual': "menu_principal",           # Estado actual del juego
    'diccionario_botones_actual': {...},         # Botones del estado actual
    'preguntas_multiple': {...},                 # Biblioteca MC
    'preguntas_VoF': {...},                      # Biblioteca VoF
    'configuraciones': {...},                   # Config global
    'usuarios': {...},                          # Todos los usuarios
    'usuario_actual': "usuario_1",              # Usuario seleccionado
    'ronda_actual': 1,                          # Ronda del juego
    'modo_juego': 'multiple',                   # 'multiple' o 'VoF'
    'texto_pregunta': "...",                    # Texto a mostrar
    ... (y MUCHOS más)
}

FLUJO DE ACTUALIZACIÓN (por frame):
----------------------------------------------------------------------------
1. procesar_botones()       → Detecta clicks y hover
2. obtener_botones_presionados() → Lista de botones clickeados
3. manejar_logica_estado_actual() → Lógica de juego, usuarios, laberinto, etc.
4. procesar_todas_acciones() → Navegación simple entre menús
5. resetear botones         → 'presionado' = False para todos
6. dibujar_estado_actual()  → Renderizar según estado
"""

from verificaciones_botones import obtener_botones_presionados, procesar_todas_acciones
from botones_funciones import procesar_botones, dibujar_botones
from logica_juego import (
    cargar_preguntas_desde_csv, cargar_preguntas_VoF_desde_csv,
    cargar_configuraciones, cargar_usuarios, actualizar_estadisticas_usuario,
    determinar_dificultad_y_tickets, determinar_dificultad_y_tickets_VoF,
    seleccionar_pregunta, seleccionar_pregunta_VoF, randomizar_respuestas,
    verificar_respuesta, verificar_respuesta_VoF, acreditar_tickets_ronda,
    remover_pregunta_usada, reestablecer_configuraciones,
    remover_pregunta_usada_VoF, crear_usuario_y_guardar
)
from menu_definiciones import (
    MENU_PRINCIPAL, MENU_JUEGO_PREGUNTA, MENU_RESULTADO_RONDA, MENU_RESULTADO_FINAL,
    MENU_SELECCION_USUARIO, MENU_CREAR_USUARIO, MENU_JUEGO_PREGUNTA_VoF,
    MENU_RESULTADO_RONDA_VoF, MENU_RESULTADO_FINAL_VoF, MENU_LABERINTO_RESULTADO,
    MENU_LABERINTO_JUEGO, MENU_TIENDA
)
from laberinto_espejos import iniciar_juego_laberinto
from leaderboard import dibujar_leaderboard_organizado

import pygame
import time


# ============================================================================
# 🎬 CREACIÓN DEL ESTADO INICIAL
# ============================================================================

def crear_estado_inicial():
    """
    🏗️ Construye el estado global del juego con TODOS los datos necesarios.
    
    ¿Qué carga?
    - 📚 Preguntas de Multiple Choice (a_preguntas.csv)
    - 📚 Preguntas de Verdadero/Falso (b_preguntas_VoF.csv)
    - ⚙️ Configuraciones (z_configuraciones.json)
    - 👥 Usuarios (z_usuarios.json)
    - 🎵 Sistema de audio inicializado
    
    Returns:
        dict: Estado completo del juego listo para usar
    """
    # ── 1. Cargar datos desde archivos ──────────────────────
    preguntas_multiple = cargar_preguntas_desde_csv("a_preguntas.csv")
    preguntas_VoF = cargar_preguntas_VoF_desde_csv("b_preguntas_VoF.csv")
    configuraciones = cargar_configuraciones("z_configuraciones.json")
    usuarios = cargar_usuarios("z_usuarios.json")
    
    # ── 2. Configuración de audio (sin .get()) ──────────────
    audio_mute = False
    audio_volumen = 0.5
    
    if "audio_mute" in configuraciones:
        audio_mute = configuraciones["audio_mute"]
    
    if "audio_volumen" in configuraciones:
        volumen_temp = configuraciones["audio_volumen"]
        if isinstance(volumen_temp, (int, float)) and 0.0 <= volumen_temp <= 1.0:
            audio_volumen = volumen_temp
    
    # ── 3. Estructura base del estado ───────────────────────
    estado = {
        # Estado actual
        'estado_actual': "menu_principal",
        'diccionario_botones_actual': MENU_PRINCIPAL,
        
        # Datos del juego
        'preguntas_multiple': preguntas_multiple,
        'preguntas_VoF': preguntas_VoF,
        'configuraciones': configuraciones,
        'usuarios': usuarios,
        'usuario_actual': None,
        
        # Estado de la partida actual
        'ronda_actual': 1,
        'opcion_seleccionada': None,
        'texto_pregunta': "",
        'texto_categoria': "",
        'texto_dificultad': "",
        'texto_resultado': "",
        'texto_tickets_ronda': "",
        'pregunta_preparada': False,
        'juego_iniciado': False,
        'modo_juego': None,
        'mostrando_resultado_ronda': False,
        'tiempo_inicio': 0,
        'tiempo_transcurrido': 0,
        
        # Creación de usuarios
        'nombre_nuevo_usuario': "",
        'slot_seleccionado': None,
        'mostrando_confirmacion_creacion': False,  # ⚠️ OBSOLETO? (ya no se usa)
        
        # Laberinto
        'dificultad_laberinto': 'facil',
        'laberinto_filas': 10,
        'laberinto_columnas': 15,
        'laberinto_tickets_ganados': 0,
        'laberinto_tiempo_final': 0,
        'laberinto_mensaje_resultado': "",
        
        # Música (versión simplificada)
        'musica_mute': audio_mute,
        'musica_reproduciendo': True,   # Siempre True (no hay pausa)
        'musica_actual': 'menu_principal',
        'musica_volumen': audio_volumen
    }
    
    # ── 4. Inicializar audio y reproducir música ────────────
    from y_musica import musica_inicializar, musica_cargar_y_reproducir, musica_actualizar_volumen
    
    musica_inicializar()
    volumen_inicial = 0.0 if audio_mute else audio_volumen
    
    print(f"🎵 Iniciando audio: mute={audio_mute}, vol={audio_volumen}")
    exito = musica_cargar_y_reproducir('menu_principal', volumen_inicial)
    
    if not exito:
        print("⚠️  No se pudo cargar menu_principal.mp3")
    
    if audio_mute:
        musica_actualizar_volumen(0.0)
        print("🔇 Iniciando con MUTE aplicado")
    else:
        print(f"🔊 Iniciando con volumen: {audio_volumen}")
    
    return estado


# ============================================================================
# 🔄 ACTUALIZACIÓN DEL ESTADO (BUCLE PRINCIPAL)
# ============================================================================

def actualizar_estado_completo(pantalla, fuente, eventos, estado):
    """
    🔄 Corazón del juego: actualiza TODO el estado en cada frame.
    
    FLUJO:
    1. Procesar botones → detectar clicks y hover
    2. Obtener botones presionados → IDs de los botones clickeados
    3. Manejar lógica del estado actual → juegos, tienda, usuarios, etc.
    4. Procesar acciones simples → navegación entre menús
    5. Actualizar estado
    6. Resetear botones → 'presionado' = False para el próximo frame
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente para textos
        eventos: Lista de eventos del frame
        estado: Estado actual del juego
    
    Returns:
        dict: Estado actualizado
    """
    # ── 0. Inicialización especial para tienda ──────────────
    if estado['estado_actual'] == "tienda" and estado['diccionario_botones_actual'] == MENU_TIENDA:
        estado['diccionario_botones_actual'] = crear_botones_tienda_dinamicos(estado)
    
    # ── 1. Procesar interacciones de botones ────────────────
    estado['diccionario_botones_actual'] = procesar_botones(
        pantalla, fuente, eventos, estado['diccionario_botones_actual']
    )
    
    # ── 2. Obtener botones presionados ──────────────────────
    botones_presionados = obtener_botones_presionados(estado['diccionario_botones_actual'])
    
    # ── 3. Lógica específica del estado actual ──────────────
    estado = manejar_logica_estado_actual(estado, botones_presionados, eventos)
    
    # ── 4. Acciones de navegación simple ────────────────────
    nuevo_estado, nuevo_diccionario = procesar_todas_acciones(
        botones_presionados, 
        estado['estado_actual'], 
        estado['diccionario_botones_actual']
    )
    
    # ── 5. Actualizar estado ────────────────────────────────
    estado['estado_actual'] = nuevo_estado
    estado['diccionario_botones_actual'] = nuevo_diccionario
    
    # ── 6. Resetear botones para el próximo frame ───────────
    claves_botones = list(estado['diccionario_botones_actual'].keys())
    for i in range(len(claves_botones)):
        boton_id = claves_botones[i]
        estado['diccionario_botones_actual'][boton_id]['presionado'] = False
    
    return estado


# ============================================================================
# 🔤 FUNCIONES DE FUENTE Y TEXTO
# ============================================================================

def cargar_fuentes():
    """
    🔤 Busca una fuente que soporte emojis en el sistema.
    
    Intenta (en orden):
    1. segoeuiemoji (Windows)
    2. arial (Windows/Linux)
    3. dejavusans (Linux)
    4. Fuente por defecto de pygame
    
    Returns:
        pygame.font.Font: Fuente lista para usar
    """
    fuente = None
    lista_fuentes = [
        "segoeuiemoji",  # Windows con emojis
        "arial",         # Fuente común
        "dejavusans",    # Linux
        None             # Pygame por defecto
    ]

    for nombre_fuente in lista_fuentes:
        try:
            fuente = pygame.font.SysFont(nombre_fuente, 24)
            print(f"Fuente cargada: {nombre_fuente}")
            break
        except:
            continue

    if fuente is None:
        fuente = pygame.font.Font(None, 24)
        print("Usando fuente por defecto")
    
    return fuente


def dibujar_texto_centrado(pantalla, fuente, texto, x, y, color):
    """
    🖌️ Dibuja texto centrado horizontalmente.
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente a usar
        texto: String a dibujar (si está vacío, no dibuja)
        x: Centro horizontal
        y: Posición vertical
        color: Tupla RGB
    """
    if texto:
        texto_surface = fuente.render(texto, True, color)
        texto_rect = texto_surface.get_rect(center=(x, y))
        pantalla.blit(texto_surface, texto_rect)


def dibujar_texto(pantalla, fuente, texto, x, y, color):
    """
    🖌️ Dibuja texto en una posición específica (alineado a la izquierda).
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente a usar
        texto: String a dibujar (si está vacío, no dibuja)
        x: Posición X (esquina superior izquierda)
        y: Posición Y (esquina superior izquierda)
        color: Tupla RGB
    """
    if texto:
        texto_surface = fuente.render(texto, True, color)
        texto_rect = texto_surface.get_rect(topleft=(x, y))
        pantalla.blit(texto_surface, texto_rect)


# ============================================================================
# 🖌️ DIBUJADO DE ESTADOS
# ============================================================================

def dibujar_estado_actual(pantalla, fuente, estado):
    """
    🖼️ Dibuja el contenido específico de CADA estado.
    
    ¿Qué dibuja según el estado?
    - menu_principal           → Info del usuario, títulos
    - juego_pregunta           → Pregunta, categoría, dificultad, tickets, tiempo
    - juego_resultado_ronda    → Correcta/Incorrecta, respuesta correcta, tickets
    - juego_resultado_final    → Estadísticas finales, record, total tickets
    - seleccion_usuario        → Slots con datos de usuarios
    - crear_usuario           → Campo de texto para nombre
    - laberinto_resultado     → Tickets ganados, tiempo, mensaje
    - tienda                 → Info del usuario, mensajes de compra
    - leaderboard            → Tabla de clasificación (delega a leaderboard.py)
    - opciones               → Botón de sonido ON/OFF
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente para textos
        estado: Estado actual del juego
    """
    # ── 1. Dibujar botones (siempre) ────────────────────────
    dibujar_botones(pantalla, fuente, estado['diccionario_botones_actual'])
    
    # ── 2. Dibujar textos específicos por estado ────────────
    match estado['estado_actual']:
        
        # ====================================================
        # 🏠 MENÚ PRINCIPAL
        # ====================================================
        case "menu_principal":
            dibujar_texto_centrado(pantalla, fuente, "JUEGO DE PREGUNTAS Y RESPUESTAS", 500, 100, (255, 255, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Jugador: {usuario['nombre']}", 500, 150, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Medallas: {usuario['medallas']}", 500, 180, (255, 215, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Record: {usuario['record_boletos']} tickets", 500, 210, (200, 200, 255))
                dibujar_texto_centrado(pantalla, fuente, f"Partidas: {usuario['partidas_jugadas']}", 500, 240, (200, 200, 255))
            else:
                dibujar_texto_centrado(pantalla, fuente, "Selecciona un usuario para jugar", 500, 150, (255, 100, 100))

        # ====================================================
        # ❓ MULTIPLE CHOICE
        # ====================================================
        case "juego_pregunta":
            dibujar_texto_centrado(pantalla, fuente, "MULTIPLE CHOICE", 500, 50, (255, 255, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto(pantalla, fuente, f"Jugador: {usuario['nombre']}", 20, 70, (255, 255, 0))
                dibujar_texto(pantalla, fuente, f"Medallas: {usuario['medallas']}", 20, 100, (255, 215, 0))
            
            dibujar_texto_centrado(pantalla, fuente, estado['texto_pregunta'], 500, 200, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_categoria'], 500, 250, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_dificultad'], 500, 280, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_tickets_ronda'], 500, 310, (255, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Ronda: {estado['ronda_actual']}/10", 500, 340, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, f"Tickets totales: {estado['configuraciones']['tickets_conseguidos']}", 500, 370, (255, 255, 0))
            
            if estado['juego_iniciado']:
                tiempo_actual = time.time() - estado['tiempo_inicio']
                dibujar_texto(pantalla, fuente, f"Tiempo: {tiempo_actual:.1f}s", 800, 70, (200, 200, 255))

        # ====================================================
        # ✅ RESULTADO DE RONDA (MC)
        # ====================================================
        case "juego_resultado_ronda":
            dibujar_texto_centrado(pantalla, fuente, "RESULTADO DE LA RONDA", 500, 100, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_pregunta'], 500, 150, (200, 200, 255))
            
            color_resultado = (0, 255, 0) if estado['configuraciones']['mensaje'] == "¡Correcta!" else (255, 0, 0)
            dibujar_texto_centrado(pantalla, fuente, estado['texto_resultado'], 500, 200, color_resultado)
            dibujar_texto_centrado(pantalla, fuente, estado['texto_tickets_ganados'], 500, 230, (255, 255, 0))
            
            if estado['configuraciones']['mensaje'] == "Incorrecta":
                dibujar_texto_centrado(pantalla, fuente, f"Tu respuesta: {estado['respuesta_seleccionada']}", 500, 280, (255, 100, 100))
                dibujar_texto_centrado(pantalla, fuente, f"Respuesta correcta: {estado['respuesta_correcta']}", 500, 310, (100, 255, 100))
            
            dibujar_texto_centrado(pantalla, fuente, f"Tickets totales: {estado['configuraciones']['tickets_conseguidos']}", 500, 360, (255, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Ronda: {estado['ronda_actual']}/10", 500, 390, (200, 200, 200))
            
            if estado['juego_iniciado']:
                tiempo_actual = time.time() - estado['tiempo_inicio']
                dibujar_texto(pantalla, fuente, f"Tiempo: {tiempo_actual:.1f}s", 800, 70, (200, 200, 255))

        # ====================================================
        # 🏆 RESULTADO FINAL (MC)
        # ====================================================
        case "juego_resultado_final":
            dibujar_texto_centrado(pantalla, fuente, "RESULTADOS FINALES - MULTIPLE CHOICE", 500, 100, (255, 255, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Jugador: {usuario['nombre']}", 500, 130, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Medallas: {usuario['medallas']}", 500, 160, (255, 215, 0))
            
            config = estado['configuraciones']
            dibujar_texto_centrado(pantalla, fuente, f"Correctas: {config['aciertos']}", 500, 200, (0, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Incorrectas: {config['fallas']}", 500, 230, (255, 0, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Tickets ganados: {config['tickets_conseguidos']}", 500, 260, (255, 255, 0))
            
            dibujar_texto_centrado(pantalla, fuente, f"Tiempo total: {estado['tiempo_transcurrido']:.1f} segundos", 500, 290, (200, 200, 255))
            
            total_preguntas = config['aciertos'] + config['fallas']
            if total_preguntas > 0:
                porcentaje = (config['aciertos'] / total_preguntas) * 100
                dibujar_texto_centrado(pantalla, fuente, f"Porcentaje de aciertos: {porcentaje:.1f}%", 500, 320, (200, 200, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Record personal: {usuario['record_boletos']} tickets", 500, 370, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Total tickets: {usuario['total_boletos']}", 500, 400, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Partidas jugadas: {usuario['partidas_jugadas']}", 500, 430, (200, 200, 255))
            
            dibujar_texto_centrado(pantalla, fuente, "¡Gracias por jugar!", 500, 480, (255, 255, 255))

        # ====================================================
        # 🤔 VERDADERO O FALSO
        # ====================================================
        case "juego_pregunta_VoF":
            dibujar_texto_centrado(pantalla, fuente, "VERDADERO O FALSO", 500, 50, (255, 255, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto(pantalla, fuente, f"Jugador: {usuario['nombre']}", 20, 70, (255, 255, 0))
                dibujar_texto(pantalla, fuente, f"Medallas: {usuario['medallas']}", 20, 100, (255, 215, 0))
            
            dibujar_texto_centrado(pantalla, fuente, estado['texto_pregunta'], 500, 200, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_categoria'], 500, 250, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_dificultad'], 500, 280, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_tickets_ronda'], 500, 310, (255, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Ronda: {estado['ronda_actual']}/10", 500, 340, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, f"Tickets totales: {estado['configuraciones']['tickets_conseguidos']}", 500, 370, (255, 255, 0))
            
            if estado['juego_iniciado']:
                tiempo_actual = time.time() - estado['tiempo_inicio']
                dibujar_texto(pantalla, fuente, f"Tiempo: {tiempo_actual:.1f}s", 800, 70, (200, 200, 255))

        # ====================================================
        # ✅ RESULTADO DE RONDA (VoF)
        # ====================================================
        case "juego_resultado_ronda_VoF":
            dibujar_texto_centrado(pantalla, fuente, "RESULTADO DE LA RONDA - VoF", 500, 100, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, estado['texto_pregunta'], 500, 150, (200, 200, 255))
            
            color_resultado = (0, 255, 0) if estado['configuraciones']['mensaje'] == "¡Correcta!" else (255, 0, 0)
            dibujar_texto_centrado(pantalla, fuente, estado['texto_resultado'], 500, 200, color_resultado)
            dibujar_texto_centrado(pantalla, fuente, estado['texto_tickets_ganados'], 500, 230, (255, 255, 0))
            
            if estado['configuraciones']['mensaje'] == "Incorrecta":
                dibujar_texto_centrado(pantalla, fuente, f"Tu respuesta: {estado['respuesta_seleccionada']}", 500, 280, (255, 100, 100))
                dibujar_texto_centrado(pantalla, fuente, f"Respuesta correcta: {estado['respuesta_correcta']}", 500, 310, (100, 255, 100))
            
            dibujar_texto_centrado(pantalla, fuente, f"Tickets totales: {estado['configuraciones']['tickets_conseguidos']}", 500, 360, (255, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Ronda: {estado['ronda_actual']}/10", 500, 390, (200, 200, 200))
            
            if estado['juego_iniciado']:
                tiempo_actual = time.time() - estado['tiempo_inicio']
                dibujar_texto(pantalla, fuente, f"Tiempo: {tiempo_actual:.1f}s", 800, 70, (200, 200, 255))

        # ====================================================
        # 🏆 RESULTADO FINAL (VoF)
        # ====================================================
        case "juego_resultado_final_VoF":
            dibujar_texto_centrado(pantalla, fuente, "RESULTADOS FINALES - VERDADERO O FALSO", 500, 100, (255, 255, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Jugador: {usuario['nombre']}", 500, 130, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Medallas: {usuario['medallas']}", 500, 160, (255, 215, 0))
            
            config = estado['configuraciones']
            dibujar_texto_centrado(pantalla, fuente, f"Correctas: {config['aciertos']}", 500, 200, (0, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Incorrectas: {config['fallas']}", 500, 230, (255, 0, 0))
            dibujar_texto_centrado(pantalla, fuente, f"Tickets ganados: {config['tickets_conseguidos']}", 500, 260, (255, 255, 0))
            
            dibujar_texto_centrado(pantalla, fuente, f"Tiempo total: {estado['tiempo_transcurrido']:.1f} segundos", 500, 290, (200, 200, 255))
            
            total_preguntas = config['aciertos'] + config['fallas']
            if total_preguntas > 0:
                porcentaje = (config['aciertos'] / total_preguntas) * 100
                dibujar_texto_centrado(pantalla, fuente, f"Porcentaje de aciertos: {porcentaje:.1f}%", 500, 320, (200, 200, 255))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Record personal: {usuario['record_boletos']} tickets", 500, 370, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Total tickets: {usuario['total_boletos']}", 500, 400, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Partidas jugadas: {usuario['partidas_jugadas']}", 500, 430, (200, 200, 255))
            
            dibujar_texto_centrado(pantalla, fuente, "¡Gracias por jugar!", 500, 480, (255, 255, 255))
            
        # ====================================================
        # 👤 SELECCIÓN DE USUARIO
        # ====================================================
        case "seleccion_usuario":
            dibujar_texto_centrado(pantalla, fuente, "SELECCIONAR USUARIO", 500, 50, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, "Haz clic en un slot para seleccionar o crear usuario", 500, 80, (200, 200, 200))
            
            # Mostrar datos sobre cada slot
            for i in range(1, 11):
                usuario_id = f'usuario_{i}'
                boton_id = f'boton_usuario_{i}'
                boton_data = estado['diccionario_botones_actual'][boton_id]
                x_boton = boton_data['x']
                y_boton = boton_data['y']
                ancho_boton = boton_data['ancho']
                
                if usuario_id in estado['usuarios']:
                    usuario = estado['usuarios'][usuario_id]
                    centro_x = x_boton + ancho_boton // 2
                    texto_y = y_boton - 60
                    
                    texto_nombre = usuario['nombre'][:10]
                    texto_stats = f"R:{usuario['record_boletos']} T:{usuario['total_boletos']}"
                    
                    dibujar_texto_centrado(pantalla, fuente, texto_nombre, centro_x, texto_y, (255, 255, 255))
                    dibujar_texto_centrado(pantalla, fuente, texto_stats, centro_x, texto_y + 25, (200, 200, 200))
                    dibujar_texto_centrado(pantalla, fuente, usuario['medallas'], centro_x, texto_y + 50, (255, 215, 0))
                else:
                    centro_x = x_boton + ancho_boton // 2
                    texto_y = y_boton - 60
                    
                    dibujar_texto_centrado(pantalla, fuente, f"Slot {i}", centro_x, texto_y, (150, 150, 150))
                    dibujar_texto_centrado(pantalla, fuente, "[VACÍO]", centro_x, texto_y + 25, (100, 100, 100))
                    dibujar_texto_centrado(pantalla, fuente, "➕", centro_x, texto_y + 50, (100, 200, 100))

        # ====================================================
        # ✏️ CREAR USUARIO
        # ====================================================
        case "crear_usuario":
            dibujar_texto_centrado(pantalla, fuente, f"CREAR USUARIO EN SLOT {estado['slot_seleccionado']}", 500, 100, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, "Ingresa tu nombre:", 500, 150, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, estado['nombre_nuevo_usuario'], 500, 200, (255, 255, 0))
            dibujar_texto_centrado(pantalla, fuente, "Presiona ENTER o haz clic en CONFIRMAR", 500, 250, (150, 150, 150))
            dibujar_botones(pantalla, fuente, estado['diccionario_botones_actual'])

        # ====================================================
        # 🗺️ LABERINTO
        # ====================================================
        case "seleccion_dificultad_laberinto":
            dibujar_texto_centrado(pantalla, fuente, "SELECCIONAR DIFICULTAD LABERINTO", 500, 100, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, "Elige el nivel de dificultad:", 500, 140, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, "Todos los modos tienen 2 minutos de tiempo", 500, 170, (200, 200, 200))

        case "laberinto_resultado":
            dibujar_texto_centrado(pantalla, fuente, "RESULTADO LABERINTO", 500, 100, (255, 255, 255))
            
            texto_dificultad = f"Dificultad: {estado['dificultad_laberinto'].upper()}"
            dibujar_texto_centrado(pantalla, fuente, texto_dificultad, 500, 140, (200, 200, 255))
            
            texto_dimensiones = f"Tamaño: {estado['laberinto_filas']}x{estado['laberinto_columnas']}"
            dibujar_texto_centrado(pantalla, fuente, texto_dimensiones, 500, 170, (200, 200, 255))
            
            if estado['laberinto_tickets_ganados'] > 0:
                dibujar_texto_centrado(pantalla, fuente, f"🎉 ¡FELICIDADES! 🎉", 500, 220, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Ganaste {estado['laberinto_tickets_ganados']} tickets", 500, 260, (255, 255, 0))
                
                if estado['laberinto_tiempo_final'] > 0:
                    minutos = int(estado['laberinto_tiempo_final'] // 60)
                    segundos = int(estado['laberinto_tiempo_final'] % 60)
                    dibujar_texto_centrado(pantalla, fuente, f"Tiempo: {minutos}:{segundos:02d}", 500, 290, (200, 200, 255))
                
                if estado['laberinto_mensaje_resultado']:
                    dibujar_texto_centrado(pantalla, fuente, estado['laberinto_mensaje_resultado'], 500, 320, (200, 255, 200))
            else:
                dibujar_texto_centrado(pantalla, fuente, "❌ No ganaste tickets", 500, 220, (255, 100, 100))
                if estado['laberinto_mensaje_resultado']:
                    dibujar_texto_centrado(pantalla, fuente, estado['laberinto_mensaje_resultado'], 500, 250, (255, 200, 200))

        # ====================================================
        # 🏪 TIENDA DE MEDALLAS
        # ====================================================
        case "tienda":
            dibujar_texto_centrado(pantalla, fuente, "🏪 TIENDA DE MEDALLAS 🏪", 500, 100, (255, 255, 0))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Jugador: {usuario['nombre']}", 500, 150, (255, 255, 255))
                dibujar_texto_centrado(pantalla, fuente, f"Tickets: {usuario['total_boletos']}", 500, 180, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Medallas: {usuario['medallas']}", 500, 210, (255, 215, 0))
                
                if 'tienda_mensaje' in estado:
                    color = (50, 255, 50) if estado.get('tienda_exito', False) else (255, 50, 50)
                    dibujar_texto_centrado(pantalla, fuente, estado['tienda_mensaje'], 500, 250, color)
            else:
                dibujar_texto_centrado(pantalla, fuente, "Selecciona un usuario primero", 500, 200, (255, 100, 100))

        # ====================================================
        # 🏆 LEADERBOARD
        # ====================================================
        case "leaderboard":
            # Delegar a función especializada en leaderboard.py
            dibujar_leaderboard_organizado(pantalla, fuente, estado, 10, 490)

        # ====================================================
        # ⚙️ OPCIONES
        # ====================================================
        case "opciones":
            # Actualizar texto del botón según estado de mute
            if estado['musica_mute']:
                estado['diccionario_botones_actual']['boton_sonido']['texto'] = 'SONIDO: OFF'
                estado['diccionario_botones_actual']['boton_sonido']['color_normal'] = (180, 70, 70)
            else:
                estado['diccionario_botones_actual']['boton_sonido']['texto'] = 'SONIDO: ON'
                estado['diccionario_botones_actual']['boton_sonido']['color_normal'] = (100, 180, 100)
            
            dibujar_botones(pantalla, fuente, estado['diccionario_botones_actual'])


# ============================================================================
# 🧠 LÓGICA DE ESTADOS (MANEJADOR PRINCIPAL)
# ============================================================================

def manejar_logica_estado_actual(estado, botones_presionados, eventos):
    """
    🧠 Procesa la lógica específica de CADA estado del juego.
    
    Esta función es el CEREBRO del juego. Decide:
    - Cuándo iniciar una partida
    - Cuándo cambiar de ronda
    - Cuándo terminar el juego
    - Cómo procesar respuestas
    - Cómo crear usuarios
    - Cómo manejar la tienda
    - Etc.
    
    Args:
        estado (dict): Estado actual del juego
        botones_presionados (list): IDs de botones clickeados este frame
        eventos (list): Eventos de pygame (para entrada de texto)
    
    Returns:
        dict: Estado actualizado
    """
    
    match estado['estado_actual']:
        
        # ====================================================
        # 🏠 MENÚ PRINCIPAL
        # ====================================================
        case "menu_principal":
            # Resetear estado de juego al volver al menú
            estado['juego_iniciado'] = False
            estado['ronda_actual'] = 1
            estado['pregunta_preparada'] = False
            estado['mostrando_resultado_ronda'] = False
            estado['tiempo_inicio'] = 0
            estado['tiempo_transcurrido'] = 0
            estado['modo_juego'] = None
            
            # Si no hay usuario, forzar selección
            if estado['usuario_actual'] is None:
                estado['estado_actual'] = "seleccion_usuario"
                estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO

        # ====================================================
        # ❓ JUEGO - MULTIPLE CHOICE
        # ====================================================
        case "juego_pregunta":
            # ── INICIAR NUEVA PARTIDA ───────────────────────
            if not estado['juego_iniciado']:
                reestablecer_configuraciones(estado['configuraciones'], "z_configuraciones.json")
                estado['juego_iniciado'] = True
                estado['pregunta_preparada'] = False
                estado['tiempo_inicio'] = time.time()
                estado['modo_juego'] = 'multiple'
            
            # ── PREPARAR NUEVA PREGUNTA ─────────────────────
            if not estado['pregunta_preparada']:
                config = estado['configuraciones']
                determinar_dificultad_y_tickets(config, estado['ronda_actual'])
                
                if seleccionar_pregunta(estado['preguntas_multiple'], config):
                    randomizar_respuestas(config)
                    
                    # Textos para mostrar
                    estado['texto_pregunta'] = config["pregunta"]["preguntas"]
                    estado['texto_categoria'] = f"Categoría: {config['categoria']}"
                    estado['texto_dificultad'] = f"Dificultad: {config['dificultad']}"
                    estado['texto_tickets_ronda'] = f"Tickets en juego: {config['tickets_ronda']}"
                    
                    # Actualizar textos de botones
                    respuestas = config["respuestas"]
                    nuevos_botones = MENU_JUEGO_PREGUNTA.copy()
                    claves_opciones = ['boton_opcion_1', 'boton_opcion_2', 'boton_opcion_3', 'boton_opcion_4']
                    
                    for i in range(len(claves_opciones)):
                        if i < len(respuestas):
                            nuevos_botones[claves_opciones[i]]['texto'] = respuestas[i]
                    
                    estado['diccionario_botones_actual'] = nuevos_botones
                    estado['pregunta_preparada'] = True
                    estado['opcion_seleccionada'] = None
                else:
                    # No hay más preguntas disponibles
                    estado['tiempo_transcurrido'] = time.time() - estado['tiempo_inicio']
                    estado['estado_actual'] = "juego_resultado_final"
                    estado['diccionario_botones_actual'] = MENU_RESULTADO_FINAL
            
            # ── PROCESAR RESPUESTAS ─────────────────────────
            for boton_id in botones_presionados:
                match boton_id:
                    case 'boton_opcion_1' | 'boton_opcion_2' | 'boton_opcion_3' | 'boton_opcion_4':
                        opcion_map = {'boton_opcion_1': 0, 'boton_opcion_2': 1, 'boton_opcion_3': 2, 'boton_opcion_4': 3}
                        opcion_seleccionada = opcion_map[boton_id]
                        
                        config = estado['configuraciones']
                        verificar_respuesta(config, opcion_seleccionada)
                        acreditar_tickets_ronda(config)
                        remover_pregunta_usada(estado['preguntas_multiple'], config)
                        
                        estado['texto_resultado'] = f"{config['mensaje']}"
                        estado['texto_tickets_ganados'] = f"Tickets ganados: {config['tickets_ronda']}"
                        estado['opcion_seleccionada'] = opcion_seleccionada
                        estado['respuesta_correcta'] = config["verdadera"]
                        estado['respuesta_seleccionada'] = config["respuestas"][opcion_seleccionada]
                        
                        estado['pregunta_preparada'] = False
                        estado['mostrando_resultado_ronda'] = True
                        
                        estado['estado_actual'] = "juego_resultado_ronda"
                        estado['diccionario_botones_actual'] = MENU_RESULTADO_RONDA
                    
                    case 'boton_salir_juego':
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                        estado['juego_iniciado'] = False
                        estado['ronda_actual'] = 1
                        estado['modo_juego'] = None
                        estado['pregunta_preparada'] = False

        # ====================================================
        # ✅ RESULTADO DE RONDA (MC)
        # ====================================================
        case "juego_resultado_ronda":
            for boton_id in botones_presionados:
                if boton_id == 'boton_continuar':
                    estado['ronda_actual'] += 1
                    
                    # Verificar si terminaron las 10 rondas
                    if estado['ronda_actual'] > estado['configuraciones']['limite']:
                        estado['tiempo_transcurrido'] = time.time() - estado['tiempo_inicio']
                        
                        if estado['usuario_actual']:
                            estado['configuraciones']["tiempo_partida"] = estado['tiempo_transcurrido']
                            actualizar_estadisticas_usuario(
                                estado['usuarios'], 
                                estado['usuario_actual'], 
                                estado['configuraciones']
                            )
                            from logica_juego import guardar_json
                            guardar_json("z_usuarios.json", estado['usuarios'])
                        
                        estado['estado_actual'] = "juego_resultado_final"
                        estado['diccionario_botones_actual'] = MENU_RESULTADO_FINAL
                    else:
                        estado['estado_actual'] = "juego_pregunta"
                        estado['diccionario_botones_actual'] = MENU_JUEGO_PREGUNTA
                    break
                    
            if 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None

        # ====================================================
        # 🤔 JUEGO - VERDADERO O FALSO
        # ====================================================
        case "juego_pregunta_VoF":
            # ── INICIAR NUEVA PARTIDA ───────────────────────
            if not estado['juego_iniciado']:
                reestablecer_configuraciones(estado['configuraciones'], "z_configuraciones.json")
                estado['juego_iniciado'] = True
                estado['pregunta_preparada'] = False
                estado['tiempo_inicio'] = time.time()
                estado['modo_juego'] = 'VoF'
            
            # ── PREPARAR NUEVA PREGUNTA ─────────────────────
            if not estado['pregunta_preparada']:
                config = estado['configuraciones']
                determinar_dificultad_y_tickets_VoF(config, estado['ronda_actual'])
                
                if seleccionar_pregunta_VoF(estado['preguntas_VoF'], config):
                    estado['texto_pregunta'] = config["pregunta"]["preguntas"]
                    estado['texto_categoria'] = f"Categoría: {config['categoria']}"
                    estado['texto_dificultad'] = f"Dificultad: {config['dificultad']}"
                    estado['texto_tickets_ronda'] = f"Tickets en juego: {config['tickets_ronda']}"
                    
                    estado['diccionario_botones_actual'] = MENU_JUEGO_PREGUNTA_VoF
                    estado['pregunta_preparada'] = True
                    estado['opcion_seleccionada'] = None
                else:
                    estado['tiempo_transcurrido'] = time.time() - estado['tiempo_inicio']
                    estado['estado_actual'] = "juego_resultado_final_VoF"
                    estado['diccionario_botones_actual'] = MENU_RESULTADO_FINAL_VoF
            
            # ── PROCESAR RESPUESTAS ─────────────────────────
            for boton_id in botones_presionados:
                match boton_id:
                    case 'boton_verdadero':
                        opcion_seleccionada = "verdadero"
                        
                        config = estado['configuraciones']
                        verificar_respuesta_VoF(config, opcion_seleccionada)
                        acreditar_tickets_ronda(config)
                        remover_pregunta_usada_VoF(estado['preguntas_VoF'], config)
                        
                        estado['texto_resultado'] = f"{config['mensaje']}"
                        estado['texto_tickets_ganados'] = f"Tickets ganados: {config['tickets_ronda']}"
                        estado['opcion_seleccionada'] = opcion_seleccionada
                        estado['respuesta_correcta'] = config["verdadera"]
                        estado['respuesta_seleccionada'] = opcion_seleccionada
                        
                        estado['pregunta_preparada'] = False
                        estado['mostrando_resultado_ronda'] = True
                        
                        estado['estado_actual'] = "juego_resultado_ronda_VoF"
                        estado['diccionario_botones_actual'] = MENU_RESULTADO_RONDA_VoF
                    
                    case 'boton_falso':
                        opcion_seleccionada = "falso"
                        
                        config = estado['configuraciones']
                        verificar_respuesta_VoF(config, opcion_seleccionada)
                        acreditar_tickets_ronda(config)
                        remover_pregunta_usada_VoF(estado['preguntas_VoF'], config)
                        
                        estado['texto_resultado'] = f"{config['mensaje']}"
                        estado['texto_tickets_ganados'] = f"Tickets ganados: {config['tickets_ronda']}"
                        estado['opcion_seleccionada'] = opcion_seleccionada
                        estado['respuesta_correcta'] = config["verdadera"]
                        estado['respuesta_seleccionada'] = opcion_seleccionada
                        
                        estado['pregunta_preparada'] = False
                        estado['mostrando_resultado_ronda'] = True
                        
                        estado['estado_actual'] = "juego_resultado_ronda_VoF"
                        estado['diccionario_botones_actual'] = MENU_RESULTADO_RONDA_VoF
                    
                    case 'boton_salir_juego':
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                        estado['juego_iniciado'] = False
                        estado['ronda_actual'] = 1
                        estado['modo_juego'] = None
                        estado['pregunta_preparada'] = False

        # ====================================================
        # ✅ RESULTADO DE RONDA (VoF)
        # ====================================================
        case "juego_resultado_ronda_VoF":
            for boton_id in botones_presionados:
                if boton_id == 'boton_continuar':
                    estado['ronda_actual'] += 1
                    
                    if estado['ronda_actual'] > estado['configuraciones']['limite']:
                        estado['tiempo_transcurrido'] = time.time() - estado['tiempo_inicio']
                        
                        if estado['usuario_actual']:
                            estado['configuraciones']["tiempo_partida"] = estado['tiempo_transcurrido']
                            actualizar_estadisticas_usuario(
                                estado['usuarios'], 
                                estado['usuario_actual'], 
                                estado['configuraciones']
                            )
                            from logica_juego import guardar_json
                            guardar_json("z_usuarios.json", estado['usuarios'])
                        
                        estado['estado_actual'] = "juego_resultado_final_VoF"
                        estado['diccionario_botones_actual'] = MENU_RESULTADO_FINAL_VoF
                    else:
                        estado['estado_actual'] = "juego_pregunta_VoF"
                        estado['diccionario_botones_actual'] = MENU_JUEGO_PREGUNTA_VoF
                    break
                    
            if 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None

        # ====================================================
        # 🏆 RESULTADO FINAL (MC)
        # ====================================================
        case "juego_resultado_final":
            if 'boton_menu_principal' in botones_presionados or 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None

        # ====================================================
        # 🏆 RESULTADO FINAL (VoF)
        # ====================================================
        case "juego_resultado_final_VoF":
            if 'boton_menu_principal' in botones_presionados or 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None

        # ====================================================
        # 👤 SELECCIÓN DE USUARIO
        # ====================================================
        case "seleccion_usuario":
            for boton_id in botones_presionados:
                match boton_id:
                    case 'boton_usuario_1' | 'boton_usuario_2' | 'boton_usuario_3' | 'boton_usuario_4' | \
                         'boton_usuario_5' | 'boton_usuario_6' | 'boton_usuario_7' | 'boton_usuario_8' | \
                         'boton_usuario_9' | 'boton_usuario_10':
                        
                        numero_slot = int(boton_id.split('_')[2])
                        usuario_id = f'usuario_{numero_slot}'
                        
                        if usuario_id in estado['usuarios']:
                            # Usuario EXISTE → seleccionar
                            estado['usuario_actual'] = usuario_id
                            estado['estado_actual'] = "menu_principal"
                            estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                            print(f"✅ Usuario seleccionado: {estado['usuarios'][usuario_id]['nombre']}")
                        else:
                            # Slot VACÍO → crear nuevo usuario
                            estado['slot_seleccionado'] = numero_slot
                            estado['nombre_nuevo_usuario'] = ""
                            estado['estado_actual'] = "crear_usuario"
                            estado['diccionario_botones_actual'] = MENU_CREAR_USUARIO
                            print(f"📝 Creando usuario en slot {numero_slot}")
                    
                    case 'boton_volver':
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL

        # ====================================================
        # ✏️ CREAR USUARIO 
        # ====================================================
        case "crear_usuario":
            from logica_juego import crear_usuario_y_guardar
            
            # 1. Capturar entrada de texto (con filtro de repeticiones)
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and estado['nombre_nuevo_usuario']:
                        estado = crear_usuario_y_guardar(estado, MENU_PRINCIPAL)
                    elif evento.key == pygame.K_BACKSPACE:
                        if estado['nombre_nuevo_usuario']:
                            estado['nombre_nuevo_usuario'] = estado['nombre_nuevo_usuario'][:-1]
                    elif evento.unicode:
                        if (evento.unicode.isalnum() or evento.unicode == ' ') and \
                           len(estado['nombre_nuevo_usuario']) < 15:
                            estado['nombre_nuevo_usuario'] += evento.unicode
            
            # 2. Botón confirmar
            if 'boton_confirmar' in botones_presionados and estado['nombre_nuevo_usuario']:
                estado = crear_usuario_y_guardar(estado, MENU_PRINCIPAL)
            
            # 3. Botón volver
            if 'boton_volver' in botones_presionados:
                estado['estado_actual'] = "seleccion_usuario"
                estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO
                estado['nombre_nuevo_usuario'] = ""
                estado['slot_seleccionado'] = None

        # ====================================================
        # 🗺️ LABERINTO - SELECCIÓN DE DIFICULTAD
        # ====================================================
        case "seleccion_dificultad_laberinto":
            boton_procesado = False
            
            for boton_id in botones_presionados:
                if not boton_procesado:
                    if boton_id == 'boton_volver':
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                        boton_procesado = True
                        
                    elif boton_id == 'boton_facil':
                        estado['dificultad_laberinto'] = 'facil'
                        estado['laberinto_filas'] = 8
                        estado['laberinto_columnas'] = 15
                        estado['estado_actual'] = "laberinto_juego"
                        estado['diccionario_botones_actual'] = MENU_LABERINTO_JUEGO
                        print(f"✅ Configurado laberinto FÁCIL: {estado['laberinto_filas']}x{estado['laberinto_columnas']}")
                        boton_procesado = True
                        
                    elif boton_id == 'boton_medio':
                        estado['dificultad_laberinto'] = 'medio'
                        estado['laberinto_filas'] = 10
                        estado['laberinto_columnas'] = 18
                        estado['estado_actual'] = "laberinto_juego"
                        estado['diccionario_botones_actual'] = MENU_LABERINTO_JUEGO
                        print(f"✅ Configurado laberinto MEDIO: {estado['laberinto_filas']}x{estado['laberinto_columnas']}")
                        boton_procesado = True
                        
                    elif boton_id == 'boton_dificil':
                        estado['dificultad_laberinto'] = 'dificil'
                        estado['laberinto_filas'] = 12
                        estado['laberinto_columnas'] = 18
                        estado['estado_actual'] = "laberinto_juego"
                        estado['diccionario_botones_actual'] = MENU_LABERINTO_JUEGO
                        print(f"✅ Configurado laberinto DIFÍCIL: {estado['laberinto_filas']}x{estado['laberinto_columnas']}")
                        boton_procesado = True
                        
                    elif boton_id == 'boton_deathrow':
                        estado['dificultad_laberinto'] = 'deathrow'
                        estado['laberinto_filas'] = 12
                        estado['laberinto_columnas'] = 22
                        estado['estado_actual'] = "laberinto_juego"
                        estado['diccionario_botones_actual'] = MENU_LABERINTO_JUEGO
                        print(f"✅ Configurado laberinto DEATHROW: {estado['laberinto_filas']}x{estado['laberinto_columnas']}")
                        boton_procesado = True

        # ====================================================
        # 🗺️ LABERINTO - JUEGO ACTIVO
        # ====================================================
        case "laberinto_juego":
            if 'boton_salir_juego' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                return estado
            
            print(f"🎯 Iniciando laberinto con: {estado['laberinto_filas']}x{estado['laberinto_columnas']}")
            
            filas = estado['laberinto_filas']
            columnas = estado['laberinto_columnas']
            
            if filas < 5 or filas > 40 or columnas < 5 or columnas > 40:
                print("❌ Dimensiones inválidas, usando 10x15")
                filas = 10
                columnas = 15
                estado['laberinto_filas'] = filas
                estado['laberinto_columnas'] = columnas
            
            nuevo_estado, estado_actualizado = iniciar_juego_laberinto(
                pygame.display.get_surface(),
                pygame.font.Font(None, 36),
                estado,
                filas,
                columnas
            )
            
            estado.update(estado_actualizado)
            estado['estado_actual'] = nuevo_estado
            estado['diccionario_botones_actual'] = MENU_LABERINTO_RESULTADO

        # ====================================================
        # 🗺️ LABERINTO - RESULTADO
        # ====================================================
        case "laberinto_resultado":
            if 'boton_menu_principal' in botones_presionados or 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['dificultad_laberinto'] = 'facil'
                estado['laberinto_filas'] = 10
                estado['laberinto_columnas'] = 15
                estado['laberinto_tickets_ganados'] = 0
                estado['laberinto_tiempo_final'] = 0
                estado['laberinto_mensaje_resultado'] = ""

        # ====================================================
        # 🏪 TIENDA DE MEDALLAS
        # ====================================================
        case "tienda":
            if estado['usuario_actual'] is None:
                estado['estado_actual'] = "seleccion_usuario"
                estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO
                return estado
            
            if estado['diccionario_botones_actual'] == MENU_TIENDA:
                estado['diccionario_botones_actual'] = crear_botones_tienda_dinamicos(estado)
            
            if 'boton_volver' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                if 'tienda_mensaje' in estado:
                    del estado['tienda_mensaje']
                if 'tienda_exito' in estado:
                    del estado['tienda_exito']
                return estado
            
            for boton_id in botones_presionados:
                if boton_id in estado['diccionario_botones_actual']:
                    boton_data = estado['diccionario_botones_actual'][boton_id]
                    
                    if 'emoji' in boton_data:
                        emoji = boton_data['emoji']
                        
                        if estado['usuario_actual']:
                            from tienda_medallas import comprar_medalla, MEDALLAS_TIENDA
                            
                            if emoji in MEDALLAS_TIENDA:
                                exito, mensaje, tickets_restantes = comprar_medalla(
                                    estado['usuarios'], 
                                    estado['usuario_actual'], 
                                    emoji
                                )
                                estado['tienda_mensaje'] = mensaje
                                estado['tienda_exito'] = exito
                                estado['tienda_medalla_seleccionada'] = emoji
                                
                                if exito:
                                    estado['diccionario_botones_actual'] = crear_botones_tienda_dinamicos(estado)

        # ====================================================
        # 🏆 LEADERBOARD
        # ====================================================
        case "leaderboard":
            if 'boton_volver' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL

        # ====================================================
        # ⚙️ OPCIONES
        # ====================================================
        case "opciones":
            if 'boton_sonido' in botones_presionados:
                from y_musica import toggle_mute_con_guardado
                estado = toggle_mute_con_guardado(estado)
            
            if 'boton_volver' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL

    return estado


# ============================================================================
# 🏪 BOTONES DINÁMICOS DE LA TIENDA
# ============================================================================

def crear_botones_tienda_dinamicos(estado):
    """
    🏪 Genera botones para la tienda según medallas disponibles.
    
    ¿Qué hace?
    - Toma MENU_TIENDA como base (solo tiene botón 'volver')
    - Agrega un botón por cada medalla que el usuario NO tiene
    - Cada botón muestra: [emoji] y [precio]
    - Color verde si puede comprar, rojo si no
    
    Args:
        estado (dict): Estado del juego (con usuario actual)
    
    Returns:
        dict: Diccionario de botones de la tienda listo para usar
    """
    from menu_definiciones import MENU_TIENDA
    from tienda_medallas import MEDALLAS_TIENDA, obtener_medallas_disponibles
    
    # Si no hay usuario, devolver tienda vacía
    if estado['usuario_actual'] is None or estado['usuario_actual'] not in estado['usuarios']:
        return MENU_TIENDA.copy()
    
    usuario = estado['usuarios'][estado['usuario_actual']]
    botones_tienda = MENU_TIENDA.copy()
    
    # Obtener medallas que el usuario NO posee
    medallas_disponibles = obtener_medallas_disponibles(usuario["medallas"])
    
    if not medallas_disponibles:
        return botones_tienda
    
    # Configuración de posición (grid 4 columnas)
    COLUMNAS = 4
    ANCHO_BOTON = 200
    ALTO_BOTON = 80
    ESPACIO_X = 10
    ESPACIO_Y = 10
    X_INICIO = 100
    Y_INICIO = 250
    
    # Crear botón para cada medalla disponible
    for i, (emoji, datos_medalla) in enumerate(medallas_disponibles):
        fila = i // COLUMNAS
        columna = i % COLUMNAS
        
        x = X_INICIO + columna * (ANCHO_BOTON + ESPACIO_X)
        y = Y_INICIO + fila * (ALTO_BOTON + ESPACIO_Y)
        
        puede_comprar = usuario["total_boletos"] >= datos_medalla["precio"]
        color = (100, 180, 100) if puede_comprar else (180, 100, 100)
        
        texto_boton = f"{emoji}\n{datos_medalla['precio']}"
        boton_id = f'boton_medalla_{emoji}'
        
        botones_tienda[boton_id] = {
            'x': x,
            'y': y,
            'ancho': ANCHO_BOTON,
            'alto': ALTO_BOTON,
            'texto': texto_boton,
            'color_normal': color,
            'presionado': False,
            'emoji': emoji  # Metadato para identificar la medalla
        }
    
    return botones_tienda


# ============================================================================
# 🎵 FUNCIONES DE MÚSICA (WRAPPERS)
# ============================================================================

def musica_aplicar_estado(estado):
    """
    🎵 Aplica el estado de música actual a pygame.
    Solo maneja mute/volumen (no hay pausa).
    """
    from y_musica import musica_actualizar_volumen
    
    if estado['musica_mute']:
        musica_actualizar_volumen(0.0)
    else:
        musica_actualizar_volumen(estado['musica_volumen'])
    
    print(f"🔊 Estado aplicado: mute={estado['musica_mute']}, vol={estado['musica_volumen']}")


def cambiar_musica(estado, nombre_musica):
    """
    🎵 Cambia la pista de música si es diferente a la actual.
    
    Args:
        estado: Estado del juego
        nombre_musica: Nombre del archivo (sin extensión)
    
    Returns:
        dict: Estado actualizado
    """
    if estado['musica_actual'] != nombre_musica:
        nuevo_estado = estado.copy()
        nuevo_estado['musica_actual'] = nombre_musica
        
        volumen = 0.0 if nuevo_estado['musica_mute'] else nuevo_estado['musica_volumen']
        
        from y_musica import musica_cargar_y_reproducir
        musica_cargar_y_reproducir(nombre_musica, volumen)
        
        print(f"🔄 Música cambiada: '{estado['musica_actual']}' -> '{nombre_musica}'")
        return nuevo_estado
    
    return estado


def actualizar_musica_segun_estado(estado):
    """
    🎵 Decide qué música debe sonar según el estado del juego.
    
    Mapeo:
    - Menús               → menu_principal
    - Laberinto          → laberinto_espejos
    - Multiple Choice    → multiple_choice
    - Verdadero/Falso    → verdadero_falso
    - Victoria           → victoria (si tickets > 0)
    - Derrota            → derrota (si tickets = 0)
    """
    estado_actual = estado['estado_actual']
    modo_juego = estado.get('modo_juego')
    
    # Menús
    if estado_actual in ["menu_principal", "seleccion_usuario", 
                         "seleccion_dificultad_laberinto", "crear_usuario"]:
        return cambiar_musica(estado, 'menu_principal')
    
    # Laberinto
    elif estado_actual == "laberinto_juego":
        return cambiar_musica(estado, 'laberinto_espejos')
    
    # Multiple Choice
    elif estado_actual in ["juego_pregunta", "juego_resultado_ronda", 
                          "juego_resultado_final"] and modo_juego == 'multiple':
        return cambiar_musica(estado, 'multiple_choice')
    
    # Verdadero o Falso
    elif estado_actual in ["juego_pregunta_VoF", "juego_resultado_ronda_VoF",
                          "juego_resultado_final_VoF"] and modo_juego == 'VoF':
        return cambiar_musica(estado, 'verdadero_falso')
    
    # Resultados (victoria/derrota)
    elif estado_actual in ["juego_resultado_final", "juego_resultado_final_VoF",
                          "laberinto_resultado"]:
        if estado_actual == "laberinto_resultado":
            tickets = estado.get('laberinto_tickets_ganados', 0)
        else:
            tickets = estado.get('configuraciones', {}).get('tickets_conseguidos', 0)
        
        if tickets > 0:
            return cambiar_musica(estado, 'victoria')
        else:
            return cambiar_musica(estado, 'derrota')
    
    return estado


def interruptor_mutear(estado):
    """
    🔇 Wrapper para toggle_mute_con_guardado de y_musica.
    """
    from y_musica import toggle_mute_con_guardado
    return toggle_mute_con_guardado(estado)


# ============================================================================
# 🖼️ FUNCIONES DE FONDOS
# ============================================================================

def obtener_fondo_actual(fondos_cargados, estado_actual, estado_por_defecto="menu_principal"):
    """
    🖼️ Obtiene el fondo de forma segura, sin usar .get().
    
    Args:
        fondos_cargados (dict): Diccionario de fondos precargados
        estado_actual (str): Estado actual del juego
        estado_por_defecto (str): Estado por defecto (debe existir)
    
    Returns:
        pygame.Surface: Fondo a mostrar
    
    Raises:
        ValueError: Si el estado por defecto no existe
    """
    if estado_por_defecto not in fondos_cargados:
        raise ValueError(f"❌ Estado por defecto '{estado_por_defecto}' no está en fondos_cargados")
    
    if estado_actual in fondos_cargados:
        return fondos_cargados[estado_actual]
    
    print(f"⚠️  Estado '{estado_actual}' no tiene fondo, usando '{estado_por_defecto}'")
    return fondos_cargados[estado_por_defecto]


