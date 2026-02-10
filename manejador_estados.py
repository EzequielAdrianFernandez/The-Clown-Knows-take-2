from verificaciones_botones import obtener_botones_presionados, procesar_todas_acciones
from botones_funciones import procesar_botones, dibujar_botones
from logica_juego import (cargar_preguntas_desde_csv, cargar_preguntas_VoF_desde_csv, cargar_configuraciones, cargar_usuarios, actualizar_estadisticas_usuario,determinar_dificultad_y_tickets, determinar_dificultad_y_tickets_VoF,seleccionar_pregunta, seleccionar_pregunta_VoF, randomizar_respuestas,verificar_respuesta, verificar_respuesta_VoF, acreditar_tickets_ronda,remover_pregunta_usada, reestablecer_configuraciones,remover_pregunta_usada_VoF)
from menu_definiciones import (MENU_PRINCIPAL, MENU_JUEGO_PREGUNTA, MENU_RESULTADO_RONDA, MENU_RESULTADO_FINAL, MENU_SELECCION_USUARIO, MENU_CREAR_USUARIO, MENU_CONFIRMAR_CREACION, MENU_JUEGO_PREGUNTA_VoF, MENU_RESULTADO_RONDA_VoF, MENU_RESULTADO_FINAL_VoF,MENU_LABERINTO_RESULTADO,MENU_LABERINTO_JUEGO,MENU_TIENDA)
from laberinto_espejos import iniciar_juego_laberinto


import pygame
import time


def crear_estado_inicial():
    """
    Crea el estado inicial del juego con todos los datos cargados
    """
    # Cargar datos del juego
    preguntas_multiple = cargar_preguntas_desde_csv("a_preguntas.csv")
    preguntas_VoF = cargar_preguntas_VoF_desde_csv("b_preguntas_VoF.csv")
    configuraciones = cargar_configuraciones("z_configuraciones.json")
    usuarios = cargar_usuarios("z_usuarios.json")
    
    # OBTENER CONFIGURACIÓN DE AUDIO (SOLO mute y volumen)
    audio_mute = False  # Valor por defecto
    audio_volumen = 0.5  # Valor por defecto
    
    # Verificar si existen las configuraciones de audio
    if "audio_mute" in configuraciones:
        audio_mute = configuraciones["audio_mute"]
    
    if "audio_volumen" in configuraciones:
        # Asegurar que el volumen está en rango válido
        volumen_temp = configuraciones["audio_volumen"]
        if isinstance(volumen_temp, (int, float)) and 0.0 <= volumen_temp <= 1.0:
            audio_volumen = volumen_temp
    
    estado = {
        'estado_actual': "menu_principal",
        'diccionario_botones_actual': MENU_PRINCIPAL,
        'preguntas_multiple': preguntas_multiple,
        'preguntas_VoF': preguntas_VoF,
        'configuraciones': configuraciones,
        'usuarios': usuarios,
        'usuario_actual': None,
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
        'nombre_nuevo_usuario': "",
        'slot_seleccionado': None,
        'mostrando_confirmacion_creacion': False,
        'dificultad_laberinto': 'facil',
        'laberinto_filas': 10,
        'laberinto_columnas': 15,
        'laberinto_tickets_ganados': 0,
        'laberinto_tiempo_final': 0,
        'laberinto_mensaje_resultado': "",
        
        # Estado de la música SIMPLIFICADO (SOLO MUTE)
        'musica_mute': audio_mute,
        'musica_reproduciendo': True,  # SIEMPRE true (no hay pausa)
        'musica_actual': 'menu_principal',
        'musica_volumen': audio_volumen
    }
    
    # Inicializar sistema de audio
    from y_musica import musica_inicializar, musica_cargar_y_reproducir, musica_actualizar_volumen
    
    # Inicializar pygame mixer
    musica_inicializar()
    
    # Determinar volumen inicial
    volumen_inicial = 0.0 if audio_mute else audio_volumen
    
    # Cargar y reproducir música del menú principal
    print(f"🎵 Iniciando audio: mute={audio_mute}, vol={audio_volumen}")
    
    exito = musica_cargar_y_reproducir('menu_principal', volumen_inicial)
    
    if not exito:
        print("⚠️  No se pudo cargar menu_principal.mp3")
    
    # Asegurar que el volumen esté correcto (por si acaso)
    if audio_mute:
        musica_actualizar_volumen(0.0)
        print("🔇 Iniciando con MUTE aplicado")
    else:
        print(f"🔊 Iniciando con volumen: {audio_volumen}")
    
    return estado

def actualizar_estado_completo(pantalla, fuente, eventos, estado):
    """
    Actualiza todo el estado del juego
    """
    # Procesar interacciones de botones
    estado['diccionario_botones_actual'] = procesar_botones(
        pantalla, fuente, eventos, estado['diccionario_botones_actual']
    )
    
    # Obtener botones presionados
    botones_presionados = obtener_botones_presionados(estado['diccionario_botones_actual'])
    
    # INICIALIZAR BOTONES DE TIENDA SI ES NECESARIO
    if estado['estado_actual'] == "tienda" and estado['diccionario_botones_actual'] == MENU_TIENDA:
        estado['diccionario_botones_actual'] = crear_botones_tienda_dinamicos(estado)
    
    # Obtener botones presionados
    botones_presionados = obtener_botones_presionados(estado['diccionario_botones_actual'])
    
    # Manejar lógica específica del estado actual
    estado = manejar_logica_estado_actual(estado, botones_presionados, eventos)
    
    # Procesar acciones y cambiar estado si es necesario
    nuevo_estado, nuevo_diccionario = procesar_todas_acciones(
        botones_presionados, 
        estado['estado_actual'], 
        estado['diccionario_botones_actual']
    )
    
    # Actualizar estado
    estado['estado_actual'] = nuevo_estado
    estado['diccionario_botones_actual'] = nuevo_diccionario
    
    return estado

def cargar_fuentes():
    fuente = None
    lista_fuentes = [
        "segoeuiemoji",  # Fuente para poder usar emogis emojis de Windows
        "arial",         # Fuente común en Windows y Linux
        "dejavusans",   # Fuente común en Linux
        None             # Fuente por defecto de pygame en caso de fallo en la carga 
    ]

    for nombre_fuente in lista_fuentes:
        try:
            fuente = pygame.font.SysFont(nombre_fuente, 24)
            print(f"Fuente cargada: {nombre_fuente}")
            break
        except:
            continue

    if fuente is None:
        fuente = pygame.font.Font(None, 24)  # Fuente por defecto
        print("Usando fuente por defecto")
    return fuente

#=== DIBUJO DEL PANTALLA === 

def dibujar_texto_centrado(pantalla, fuente, texto, x, y, color):
    """Dibuja texto centrado horizontalmente en la posición x"""
    if texto:  # Solo dibujar si el texto no está vacío
        texto_surface = fuente.render(texto, True, color)
        texto_rect = texto_surface.get_rect(center=(x, y))
        pantalla.blit(texto_surface, texto_rect)

def dibujar_texto(pantalla, fuente, texto, x, y, color):
    """Dibuja texto en una posición específica"""
    if texto:
        texto_surface = fuente.render(texto, True, color)
        texto_rect = texto_surface.get_rect(topleft=(x, y))
        pantalla.blit(texto_surface, texto_rect)


def dibujar_estado_actual(pantalla, fuente, estado):
    """
    Dibuja el estado actual del juego con textos específicos
    """
    # Dibujar botones
    dibujar_botones(pantalla, fuente, estado['diccionario_botones_actual'])
    
    # Dibujar textos específicos del estado
    match estado['estado_actual']:
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

        # === MULTIPLE CHOICE ===
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

        # === VERDADERO O FALSO ===
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
        # === SELECCIÓN DE USUARIO ===
        case "seleccion_usuario":
            dibujar_texto_centrado(pantalla, fuente, "SELECCIONAR USUARIO", 500, 50, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, "Haz clic en un slot para seleccionar o crear usuario", 500, 80, (200, 200, 200))
            
            # Mostrar lista de usuarios disponibles - texto sobre los botones
            for i in range(1, 11):
                usuario_id = f'usuario_{i}'
                
                # Obtener posición del botón desde el diccionario
                boton_id = f'boton_usuario_{i}'
                boton_data = estado['diccionario_botones_actual'][boton_id]
                x_boton = boton_data['x']
                y_boton = boton_data['y']
                ancho_boton = boton_data['ancho']
                
                if usuario_id in estado['usuarios']:
                    usuario = estado['usuarios'][usuario_id]
                    
                    # Texto compacto centrado sobre el botón
                    texto_nombre = usuario['nombre'][:10]  # Limitar longitud del nombre
                    texto_stats = f"R:{usuario['record_boletos']} T:{usuario['total_boletos']}"
                    
                    # Calcular posición centrada sobre el botón (más separación para emojis)
                    centro_x = x_boton + ancho_boton // 2
                    texto_y = y_boton - 60  # 60 píxeles arriba del botón
                    
                    dibujar_texto_centrado(pantalla, fuente, texto_nombre, centro_x, texto_y, (255, 255, 255))
                    dibujar_texto_centrado(pantalla, fuente, texto_stats, centro_x, texto_y + 25, (200, 200, 200))
                    dibujar_texto_centrado(pantalla, fuente, usuario['medallas'], centro_x, texto_y + 50, (255, 215, 0))
                else:
                    # Slot vacío - texto sobre el botón
                    centro_x = x_boton + ancho_boton // 2
                    texto_y = y_boton - 60  # 60 píxeles arriba del botón
                    
                    dibujar_texto_centrado(pantalla, fuente, f"Slot {i}", centro_x, texto_y, (150, 150, 150))
                    dibujar_texto_centrado(pantalla, fuente, "[VACÍO]", centro_x, texto_y + 25, (100, 100, 100))
                    dibujar_texto_centrado(pantalla, fuente, "➕", centro_x, texto_y + 50, (100, 200, 100))
        #=== LABERINTO ===
        case "seleccion_dificultad_laberinto":
            dibujar_texto_centrado(pantalla, fuente, "SELECCIONAR DIFICULTAD LABERINTO", 500, 100, (255, 255, 255))
            dibujar_texto_centrado(pantalla, fuente, "Elige el nivel de dificultad:", 500, 140, (200, 200, 200))
            dibujar_texto_centrado(pantalla, fuente, "Todos los modos tienen 2 minutos de tiempo", 500, 170, (200, 200, 200))

        case "laberinto_resultado":
            dibujar_texto_centrado(pantalla, fuente, "RESULTADO LABERINTO", 500, 100, (255, 255, 255))
            
            # Mostrar dificultad
            texto_dificultad = f"Dificultad: {estado['dificultad_laberinto'].upper()}"
            dibujar_texto_centrado(pantalla, fuente, texto_dificultad, 500, 140, (200, 200, 255))
            
            # Mostrar dimensiones
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

        #=== TIENDA DE MEDALLAS ===
        case "tienda":
            dibujar_texto_centrado(pantalla, fuente, "🏪 TIENDA DE MEDALLAS 🏪", 500, 100, (255, 255, 0))
            
            if estado['usuario_actual'] and estado['usuario_actual'] in estado['usuarios']:
                usuario = estado['usuarios'][estado['usuario_actual']]
                dibujar_texto_centrado(pantalla, fuente, f"Jugador: {usuario['nombre']}", 500, 150, (255, 255, 255))
                dibujar_texto_centrado(pantalla, fuente, f"Tickets: {usuario['total_boletos']}", 500, 180, (255, 255, 0))
                dibujar_texto_centrado(pantalla, fuente, f"Medallas: {usuario['medallas']}", 500, 210, (255, 215, 0))
                
                # Mostrar mensaje de compra si existe
                if 'tienda_mensaje' in estado:
                    color = (50, 255, 50) if estado.get('tienda_exito', False) else (255, 50, 50)
                    dibujar_texto_centrado(pantalla, fuente, estado['tienda_mensaje'], 500, 250, color)
            else:
                dibujar_texto_centrado(pantalla, fuente, "Selecciona un usuario primero", 500, 200, (255, 100, 100))

        #=== LEADERBOARD ===
        case "leaderboard":
            dibujar_texto_centrado(pantalla, fuente, "🏆 LEADERBOARD 🏆", 500, 50, (255, 255, 0))
            
            # Obtener ambos leaderboards
            from logica_juego import obtener_leaderboard_record, obtener_leaderboard_total
            
            leaderboard_record = obtener_leaderboard_record(estado['usuarios'], limite=5)
            leaderboard_total = obtener_leaderboard_total(estado['usuarios'], limite=5)
            
            # Título RECORD
            dibujar_texto_centrado(pantalla, fuente, "MEJOR PARTIDA INDIVIDUAL", 250, 100, (255, 200, 100))
            
            # Mostrar leaderboard de RECORD
            for i, (nombre, record, total, partidas, medallas, usuario_id) in enumerate(leaderboard_record):
                y_pos = 140 + i * 40
                
                # Posición
                dibujar_texto(pantalla, fuente, f"{i+1}.", 100, y_pos, (255, 255, 255))
                
                # Nombre y emojis
                nombre_texto = f"{nombre[:12]} {medallas}"
                dibujar_texto(pantalla, fuente, nombre_texto, 140, y_pos, (200, 200, 255))
                
                # Record
                dibujar_texto(pantalla, fuente, f"{record} tickets", 350, y_pos, (255, 255, 0))
                
                # Partidas jugadas
                dibujar_texto(pantalla, fuente, f"({partidas} partidas)", 450, y_pos, (150, 150, 150))
            
            # Título TOTAL
            dibujar_texto_centrado(pantalla, fuente, "TOTAL ACUMULADO", 750, 100, (255, 200, 100))
            
            # Mostrar leaderboard de TOTAL
            for i, (nombre, total, record, partidas, medallas, usuario_id) in enumerate(leaderboard_total):
                y_pos = 140 + i * 40
                
                # Posición
                dibujar_texto(pantalla, fuente, f"{i+1}.", 600, y_pos, (255, 255, 255))
                
                # Nombre y emojis
                nombre_texto = f"{nombre[:12]} {medallas}"
                dibujar_texto(pantalla, fuente, nombre_texto, 640, y_pos, (200, 200, 255))
                
                # Total
                dibujar_texto(pantalla, fuente, f"{total} tickets", 850, y_pos, (100, 255, 100))
                
                # Mejor partida
                dibujar_texto(pantalla, fuente, f"Mejor: {record}", 950, y_pos, (255, 200, 100))
            
            # Si no hay suficientes usuarios
            if len(leaderboard_record) == 0:
                dibujar_texto_centrado(pantalla, fuente, "¡Aún no hay jugadores con partidas!", 500, 350, (255, 100, 100))
            
            # Instrucciones
            dibujar_texto_centrado(pantalla, fuente, "Juega más partidas para subir en el ranking!", 500, 550, (200, 200, 200))

#=== MANEJADOR PRINCIPAL DE LÓGICA DE ESTADOS ===#

def manejar_logica_estado_actual(estado, botones_presionados, eventos):
    """Maneja la lógica específica de cada estado"""
    
    match estado['estado_actual']:
        case "menu_principal":
            # Resetear el juego si vuelve al menú principal
            estado['juego_iniciado'] = False
            estado['ronda_actual'] = 1
            estado['pregunta_preparada'] = False
            estado['mostrando_resultado_ronda'] = False
            estado['tiempo_inicio'] = 0
            estado['tiempo_transcurrido'] = 0
            estado['modo_juego'] = None
            
            # Verificar si hay usuario seleccionado para mostrar botón jugar
            if estado['usuario_actual'] is None:
                # Si no hay usuario, cambiar a selección de usuario
                estado['estado_actual'] = "seleccion_usuario"
                estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO
        
        case "juego_pregunta":
            # Lógica para Multiple Choice (existente)
            if not estado['juego_iniciado']:
                reestablecer_configuraciones(estado['configuraciones'], "z_configuraciones.json")
                estado['juego_iniciado'] = True
                estado['pregunta_preparada'] = False
                estado['tiempo_inicio'] = time.time()
                estado['modo_juego'] = 'multiple'
            
            if not estado['pregunta_preparada']:
                config = estado['configuraciones']
                determinar_dificultad_y_tickets(config, estado['ronda_actual'])
                
                if seleccionar_pregunta(estado['preguntas_multiple'], config):
                    randomizar_respuestas(config)
                    
                    estado['texto_pregunta'] = config["pregunta"]["preguntas"]
                    estado['texto_categoria'] = f"Categoría: {config['categoria']}"
                    estado['texto_dificultad'] = f"Dificultad: {config['dificultad']}"
                    estado['texto_tickets_ronda'] = f"Tickets en juego: {config['tickets_ronda']}"
                    
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
                    estado['tiempo_transcurrido'] = time.time() - estado['tiempo_inicio']
                    estado['estado_actual'] = "juego_resultado_final"
                    estado['diccionario_botones_actual'] = MENU_RESULTADO_FINAL
            
            for boton_id in botones_presionados:
                if boton_id.startswith('boton_opcion_'):
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
                    break

                #QUICK FIX:salir al menu principal desde el juego
                if 'boton_salir_juego' in botones_presionados:
                    estado['estado_actual'] = "menu_principal"
                    estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                    estado['juego_iniciado'] = False
                    estado['ronda_actual'] = 1
                    estado['modo_juego'] = None
                    estado['pregunta_preparada'] = False

        case "juego_resultado_ronda":
            # Lógica para el botón continuar en Multiple Choice
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


        case "juego_pregunta_VoF":
            #Lógica para Verdadero o Falso
            if not estado['juego_iniciado']:
                reestablecer_configuraciones(estado['configuraciones'], "z_configuraciones.json")
                estado['juego_iniciado'] = True
                estado['pregunta_preparada'] = False
                estado['tiempo_inicio'] = time.time()
                estado['modo_juego'] = 'VoF'
            
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
            
            for boton_id in botones_presionados:
                if boton_id in ['boton_verdadero', 'boton_falso']:
                    opcion_seleccionada = "verdadero" if boton_id == 'boton_verdadero' else "falso"
                    
                    config = estado['configuraciones']
                    verificar_respuesta_VoF(config, opcion_seleccionada)
                    acreditar_tickets_ronda(config)
                    remover_pregunta_usada_VoF(estado['preguntas_VoF'], config)  # ← CAMBIADO
                    
                    estado['texto_resultado'] = f"{config['mensaje']}"
                    estado['texto_tickets_ganados'] = f"Tickets ganados: {config['tickets_ronda']}"
                    estado['opcion_seleccionada'] = opcion_seleccionada
                    estado['respuesta_correcta'] = config["verdadera"]
                    estado['respuesta_seleccionada'] = opcion_seleccionada
                    
                    estado['pregunta_preparada'] = False
                    estado['mostrando_resultado_ronda'] = True
                    
                    estado['estado_actual'] = "juego_resultado_ronda_VoF"
                    estado['diccionario_botones_actual'] = MENU_RESULTADO_RONDA_VoF
                    break
                #QUICK FIX:salir al menu principal desde el juego VoF
                if 'boton_salir_juego' in botones_presionados:
                    estado['estado_actual'] = "menu_principal"
                    estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                    estado['juego_iniciado'] = False
                    estado['ronda_actual'] = 1
                    estado['modo_juego'] = None
                    estado['pregunta_preparada'] = False

        case "juego_resultado_ronda_VoF":
            # NUEVO: Resultado de ronda para VoF
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

        case "juego_resultado_final":
            if 'boton_menu_principal' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None

            if 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None

        case "juego_resultado_final_VoF":
            if 'boton_menu_principal' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None
            
            if 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['juego_iniciado'] = False
                estado['ronda_actual'] = 1
                estado['modo_juego'] = None


        case "seleccion_usuario":
            # Manejar selección de usuario existente o slot vacío
            for i in range(1, 11):  # Para 10 usuarios posibles
                boton_id = f'boton_usuario_{i}'
                if boton_id in botones_presionados:
                    usuario_id = f'usuario_{i}'
                    if usuario_id in estado['usuarios']:
                        # Usuario existe, seleccionarlo
                        estado['usuario_actual'] = usuario_id
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                    else:
                        # Slot vacío, mostrar confirmación de creación
                        estado['slot_seleccionado'] = i
                        estado['mostrando_confirmacion_creacion'] = True
                        estado['estado_actual'] = "confirmar_creacion"
                        estado['diccionario_botones_actual'] = MENU_CONFIRMAR_CREACION
                    break
            
            # Botón volver
            if 'boton_volver' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL

        case "confirmar_creacion":
            # Manejar confirmación para crear usuario en slot vacío
            if 'boton_crear' in botones_presionados:
                estado['estado_actual'] = "crear_usuario"
                estado['diccionario_botones_actual'] = MENU_CREAR_USUARIO
                estado['nombre_nuevo_usuario'] = ""
            
            if 'boton_cancelar' in botones_presionados:
                estado['estado_actual'] = "seleccion_usuario"
                estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO
                estado['slot_seleccionado'] = None
                estado['mostrando_confirmacion_creacion'] = False

        case "crear_usuario":
            # Manejar entrada de texto para nombre de usuario
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and estado['nombre_nuevo_usuario']:
                        # Crear usuario con el nombre ingresado en el slot seleccionado
                        usuario_id = f"usuario_{estado['slot_seleccionado']}"
                        estado['usuarios'][usuario_id] = {
                            "nombre": estado['nombre_nuevo_usuario'],
                            "record_boletos": 0,
                            "total_boletos": 0,
                            "partidas_jugadas": 0,
                            "tiempo_promedio": 0,
                            "medallas": ""
                        }
                        from logica_juego import guardar_json
                        guardar_json("z_usuarios.json", estado['usuarios'])
                        
                        estado['usuario_actual'] = usuario_id
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                        estado['nombre_nuevo_usuario'] = ""
                        estado['slot_seleccionado'] = None
                        estado['mostrando_confirmacion_creacion'] = False
                    elif evento.key == pygame.K_BACKSPACE:
                        estado['nombre_nuevo_usuario'] = estado['nombre_nuevo_usuario'][:-1]
                    else:
                        # Agregar caracter al nombre (solo letras y números)
                        if evento.unicode.isalnum() or evento.unicode == ' ':
                            if len(estado['nombre_nuevo_usuario']) < 15:  # Limitar longitud
                                estado['nombre_nuevo_usuario'] += evento.unicode
            
            # Botón confirmar
            if 'boton_confirmar' in botones_presionados and estado['nombre_nuevo_usuario']:
                usuario_id = f"usuario_{estado['slot_seleccionado']}"
                estado['usuarios'][usuario_id] = {
                    "nombre": estado['nombre_nuevo_usuario'],
                    "record_boletos": 0,
                    "total_boletos": 0,
                    "partidas_jugadas": 0,
                    "tiempo_promedio": 0,
                    "medallas": ""
                }
                from logica_juego import guardar_json
                guardar_json("z_usuarios.json", estado['usuarios'])
                
                estado['usuario_actual'] = usuario_id
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                estado['nombre_nuevo_usuario'] = ""
                estado['slot_seleccionado'] = None
                estado['mostrando_confirmacion_creacion'] = False
            
            # Botón volver
            if 'boton_volver' in botones_presionados:
                estado['estado_actual'] = "seleccion_usuario"
                estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO
                estado['nombre_nuevo_usuario'] = ""
                estado['slot_seleccionado'] = None
                estado['mostrando_confirmacion_creacion'] = False

                        # ======================================= PARA LABERINTO ===================================================
        case "seleccion_dificultad_laberinto":
            # Manejar selección de dificultad CUANDO SE PRESIONAN BOTONES
            # Usar variable de control en vez de break
            boton_procesado = False
            
            for boton_id in botones_presionados:
                # Solo procesar si no se ha procesado un botón todavía
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

        case "laberinto_juego":
            # QUICK FIX: Permitir salir al menú principal desde el juego del laberinto
            if 'boton_salir_juego' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                return estado
            
            # VERIFICAR DIMENSIONES ACTUALES
            print(f"🎯 Iniciando laberinto con: {estado['laberinto_filas']}x{estado['laberinto_columnas']}")
            
            # Validar dimensiones antes de continuar
            filas = estado['laberinto_filas']
            columnas = estado['laberinto_columnas']
            
            # Verificar que las dimensiones son válidas
            if filas < 5 or filas > 40 or columnas < 5 or columnas > 40:
                print("❌ Dimensiones inválidas, usando valores por defecto")
                filas = 10
                columnas = 15
                estado['laberinto_filas'] = filas
                estado['laberinto_columnas'] = columnas
            
            # Iniciar el juego del laberinto
            nuevo_estado, estado_actualizado = iniciar_juego_laberinto(
                pygame.display.get_surface(),  # Pantalla actual
                pygame.font.Font(None, 36),    # Fuente temporal
                estado,
                filas,     # ← USAR LAS DIMENSIONES VALIDADAS
                columnas   # ← USAR LAS DIMENSIONES VALIDADAS
            )
            
            # Actualizar estado con los resultados del laberinto
            estado.update(estado_actualizado)
            estado['estado_actual'] = nuevo_estado
            estado['diccionario_botones_actual'] = MENU_LABERINTO_RESULTADO

        case "laberinto_resultado":
            if 'boton_menu_principal' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                # Resetear estado del laberinto
                estado['dificultad_laberinto'] = 'facil'
                estado['laberinto_filas'] = 10
                estado['laberinto_columnas'] = 15
                estado['laberinto_tickets_ganados'] = 0
                estado['laberinto_tiempo_final'] = 0
                estado['laberinto_mensaje_resultado'] = ""


            if 'boton_salir' in botones_presionados:
                estado['estado_actual'] = "menu_principal"
                estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                # Resetear estado del laberinto
                estado['dificultad_laberinto'] = 'facil'
                estado['laberinto_filas'] = 10
                estado['laberinto_columnas'] = 15
                estado['laberinto_tickets_ganados'] = 0
                estado['laberinto_tiempo_final'] = 0
                estado['laberinto_mensaje_resultado'] = ""

        case "tienda":
                    # Verificar que hay usuario seleccionado
                    if estado['usuario_actual'] is None:
                        estado['estado_actual'] = "seleccion_usuario"
                        estado['diccionario_botones_actual'] = MENU_SELECCION_USUARIO
                        return estado
                    
                    # CREAR BOTONES DINÁMICOS (si no existen o se acaba de entrar)
                    if estado['diccionario_botones_actual'] == MENU_TIENDA:
                        estado['diccionario_botones_actual'] = crear_botones_tienda_dinamicos(estado)
                    
                    # Botón volver
                    if 'boton_volver' in botones_presionados:
                        estado['estado_actual'] = "menu_principal"
                        estado['diccionario_botones_actual'] = MENU_PRINCIPAL
                        # Limpiar mensajes de tienda
                        if 'tienda_mensaje' in estado:
                            del estado['tienda_mensaje']
                        if 'tienda_exito' in estado:
                            del estado['tienda_exito']
                        return estado
                    
                    # Botones dinámicos de medallas
                    for boton_id in botones_presionados:
                        if boton_id.startswith('boton_medalla_'):
                            emoji = boton_id.replace('boton_medalla_', '')
                            
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
                                    
                                    # ACTUALIZAR BOTONES después de compra exitosa
                                    if exito:
                                        estado['diccionario_botones_actual'] = crear_botones_tienda_dinamicos(estado)

    return estado

#=== BOTONES DINAMICOS ===#
def crear_botones_tienda_dinamicos(estado):
    """
    Crea botones dinámicos para la tienda basados en medallas disponibles.
    Versión MINIMALISTA: solo emoji y precio.
    """
    from menu_definiciones import MENU_TIENDA
    from tienda_medallas import MEDALLAS_TIENDA, obtener_medallas_disponibles
    
    # Si no hay usuario, devolver menú básico
    if estado['usuario_actual'] is None or estado['usuario_actual'] not in estado['usuarios']:
        return MENU_TIENDA.copy()
    
    usuario = estado['usuarios'][estado['usuario_actual']]
    botones_tienda = MENU_TIENDA.copy()
    
    # Obtener medallas que el usuario NO tiene
    medallas_disponibles = obtener_medallas_disponibles(usuario["medallas"])
    
    # Si no hay medallas disponibles, mostrar mensaje
    if not medallas_disponibles:
        # Podrías agregar un botón especial o mensaje
        return botones_tienda
    
    # CONFIGURACIÓN MINIMALISTA - BOTONES PEQUEÑOS
    COLUMNAS = 4  # columnas
    ANCHO_BOTON = 200  # ANCHO
    ALTO_BOTON = 80    # Más compacto
    ESPACIO_X = 10
    ESPACIO_Y = 10
    X_INICIO = 100     # punto de inicio del primer botón Horizontal
    Y_INICIO = 250     # punto de inicio del primer botón Vertical
    
    # Crear botones para cada medalla disponible
    for i, (emoji, datos_medalla) in enumerate(medallas_disponibles):
        fila = i // COLUMNAS
        columna = i % COLUMNAS
        
        x = X_INICIO + columna * (ANCHO_BOTON + ESPACIO_X)
        y = Y_INICIO + fila * (ALTO_BOTON + ESPACIO_Y)
        
        # Verificar si puede comprar
        puede_comprar = usuario["total_boletos"] >= datos_medalla["precio"]
        color = (100, 180, 100) if puede_comprar else (180, 100, 100)
        
        # TEXTO MINIMALISTA: solo emoji y precio
        texto_boton = f"{emoji}\n{datos_medalla['precio']}"  # Solo emoji y precio
        
        # Crear ID único para el botón
        boton_id = f'boton_medalla_{emoji}'
        
        botones_tienda[boton_id] = {
            'x': x,
            'y': y,
            'ancho': ANCHO_BOTON,
            'alto': ALTO_BOTON,
            'texto': texto_boton,
            'color_normal': color,
            'presionado': False
        }
    
    return botones_tienda

#=== MUSICA ===#
def musica_aplicar_estado(estado):
    """
    Aplica el estado de música actual a pygame.
    SOLO maneja mute/volumen (ya no hay pausa).
    """
    from y_musica import musica_actualizar_volumen
    
    # Aplicar mute/volumen
    if estado['musica_mute']:
        musica_actualizar_volumen(0.0)
    else:
        musica_actualizar_volumen(estado['musica_volumen'])
    
    # NO HAY play/pause - la música SIEMPRE se reproduce
    # La música ya está reproduciéndose desde crear_estado_inicial
    
    print(f"🔊 Estado aplicado: mute={estado['musica_mute']}, vol={estado['musica_volumen']}")

def cambiar_musica(estado, nombre_musica):
    """
    Cambia la música actual.
    VERSIÓN SIMPLIFICADA: Solo mute/volumen, no pausa.
    
    Args:
        estado: Estado actual del juego
        nombre_musica: Nombre de la música a reproducir
    
    Returns:
        Estado actualizado
    """
    # Solo cambiar si es diferente a la actual
    if estado['musica_actual'] != nombre_musica:
        nuevo_estado = estado.copy()
        nuevo_estado['musica_actual'] = nombre_musica
        
        # Cargar y reproducir nueva música
        volumen = 0.0 if nuevo_estado['musica_mute'] else nuevo_estado['musica_volumen']
        
        from y_musica import musica_cargar_y_reproducir
        musica_cargar_y_reproducir(nombre_musica, volumen)
        
        print(f"🔄 Música cambiada: '{estado['musica_actual']}' -> '{nombre_musica}'")
        return nuevo_estado
    
    # Si es la misma música, no hacer nada
    return estado

def actualizar_musica_segun_estado(estado):

    """
    Decide qué música reproducir según el estado del juego.
    
    Args:
        estado: Estado actual del juego
    
    Returns:
        Estado actualizado
    """
    estado_actual = estado['estado_actual']
    modo_juego = estado.get('modo_juego')
    
    # Menús
    if estado_actual in ["menu_principal", "seleccion_usuario", 
                         "seleccion_dificultad_laberinto", "crear_usuario",
                         "confirmar_creacion"]:
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
        # Determinar si es victoria o derrota
        if estado_actual == "laberinto_resultado":
            tickets = estado.get('laberinto_tickets_ganados', 0)
        else:
            tickets = estado.get('configuraciones', {}).get('tickets_conseguidos', 0)
        
        if tickets > 0:
            return cambiar_musica(estado, 'victoria')
        else:
            return cambiar_musica(estado, 'derrota')
    
    # Por defecto, no cambiar
    return estado

def interruptor_mutear(estado):
    """
    Alterna entre mute y unmute.
    Ahora delega a la función de y_musica.
    """
    from y_musica import toggle_mute_con_guardado
    return toggle_mute_con_guardado(estado)




