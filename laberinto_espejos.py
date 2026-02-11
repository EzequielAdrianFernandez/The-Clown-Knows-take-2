import random
import time
import pygame
from laberintos_predeterminados import obtener_laberinto_manual

# Dimensiones de la pantalla
ANCHO_PANTALLA = 1000 
ALTO_PANTALLA = 700 

# Constantes del juego
CELDA_SIZE = 40  # Tamaño de cada celda en píxeles

# Colores
COLOR_FONDO = (25, 25, 50)
COLOR_CELDA_VACIA = (50, 50, 80)
COLOR_PARED = (100, 50, 50)
COLOR_ENTRADA = (50, 180, 50)
COLOR_SALIDA = (180, 50, 50)
COLOR_JUGADOR = (255, 255, 0)
COLOR_ESPEO = (100, 200, 255)
COLOR_TEXTO = (255, 255, 255)
COLOR_TIEMPO_BUENO = (50, 255, 50)
COLOR_TIEMPO_MEDIO = (255, 255, 50)
COLOR_TIEMPO_MALO = (255, 50, 50)

def calcular_margenes_centrados(columnas, filas, espacio_ui_superior=150):
    """
    Calcula márgenes para centrar el laberinto en la pantalla.
    """
    # Calcular tamaño total del laberinto
    laberinto_ancho = columnas * CELDA_SIZE
    laberinto_alto = filas * CELDA_SIZE
    
    # Centrar horizontalmente
    margen_x = (ANCHO_PANTALLA - laberinto_ancho) // 2
    
    # Centrar verticalmente, dejando espacio para UI
    espacio_disponible = ALTO_PANTALLA - espacio_ui_superior
    margen_y = espacio_ui_superior + max(0, (espacio_disponible - laberinto_alto) // 2)
    
    # Asegurar que no sea negativo
    margen_x = max(0, margen_x)
    margen_y = max(espacio_ui_superior, margen_y)
    
    return margen_x, margen_y

def crear_laberinto(filas, columnas,dificultad="facil", intentos_max=80):
    """Genera un laberinto válido con al menos un camino entre E y S."""
    #calcular y preparar laberinto centrado
    max_filas_por_pantalla = (ALTO_PANTALLA - 50) // CELDA_SIZE
    max_columnas_por_pantalla = ANCHO_PANTALLA // CELDA_SIZE
    
    if filas < 5:
        filas = 5
    if columnas < 5:
        columnas = 5
    if filas > max_filas_por_pantalla:
        print(f"⚠️  Reduciendo filas de {filas} a {max_filas_por_pantalla} para que entre en pantalla")
        filas = max_filas_por_pantalla
    if columnas > max_columnas_por_pantalla:
        print(f"⚠️  Reduciendo columnas de {columnas} a {max_columnas_por_pantalla} para que entre en pantalla")
        columnas = max_columnas_por_pantalla


    
    # Validar dimensiones mínimas y máximas
    if filas < 5:
        filas = 5
    if columnas < 5:
        columnas = 5
    if filas > 23:
        filas = 23
    if columnas > 22:
        columnas = 22
    
    laberinto_valido_encontrado = False
    laberinto_final = None
    
    for intento in range(intentos_max):
        laberinto = [[' ' for _ in range(columnas)] for _ in range(filas)]

        # Crea paredes "#" y espejos "/" y "\" de manera aleatoria
        for i in range(filas):
            for j in range(columnas):
                if random.random() < 0.3:  # 30% probabilidad de pared
                    laberinto[i][j] = '#'
                elif random.random() < 0.1:  # 10% probabilidad de espejo
                    laberinto[i][j] = random.choice(['/', '\\'])
        
        # Determina entrada "E" y salida "S" en las esquinas opuestas
        laberinto[0][0] = 'E'
        laberinto[filas-1][columnas-1] = 'S'
        
        # Verifica si el laberinto es resoluble
        if resolver_laberinto(laberinto, (0, 0)) is not None:
            laberinto_valido_encontrado = True
            laberinto_final = laberinto
            break
    
    # Si no se encontró un laberinto válido, usar mapa manual según dificultad
    if not laberinto_valido_encontrado:
        print(f"⚠️  No se encontró laberinto válido en {intentos_max} intentos")
        print(f"   Usando mapa manual para dificultad: {dificultad}")
        laberinto_final = obtener_laberinto_manual(dificultad, filas, columnas)
    
    return laberinto_final

def iniciar_juego_laberinto(pantalla, fuente, estado_juego, filas=10, columnas=15):
    # === AGREGAR ESTO AL INICIO ===
    from y_musica import musica_cargar_y_reproducir, musica_actualizar_volumen
    from menu_definiciones import MENU_LABERINTO_RESULTADO
    from botones_funciones import inicializar_botones_laberinto
    # Cargar música del laberinto
    volumen = 0.5
    if 'musica_volumen' in estado_juego:
        volumen = estado_juego['musica_volumen']
    
    if 'musica_mute' in estado_juego and estado_juego['musica_mute']:
        volumen = 0.0
    
    print("🎵 Iniciando música del laberinto...")
    exito = musica_cargar_y_reproducir('laberinto_espejos', volumen)
    
    if not exito:
        print("⚠️ No se encontró laberinto_espejos, intentando con alternativa...")
        musica_cargar_y_reproducir('electro_swing', volumen)
    
    # Verificar si estamos muteados
    if 'musica_mute' in estado_juego and estado_juego['musica_mute']:
        volumen = 0.0
    
    # Cargar música del laberinto
    print("🎵 Iniciando música del laberinto...")
    exito = musica_cargar_y_reproducir('laberinto_espejos', volumen)
    
    # Si falla, cargar música alternativa
    if not exito:
        print("⚠️ No se encontró laberinto_espejos, intentando con electro_swing...")
        musica_cargar_y_reproducir('electro_swing', volumen)
    # === FIN DEL AGREGADO ===
    
    # VERIFICAR DIMENSIONES RECIBIDAS
    print(f"🔍 Laberinto recibió: {filas}x{columnas}")
    
    # Validar dimensiones antes de continuar
    if filas < 5 or filas > 40 or columnas < 5 or columnas > 40:
        print("❌ Dimensiones inválidas, usando 10x15")
        filas = 10
        columnas = 15
    
    # Mostrar instrucciones
    if not mostrar_tabla_recompensas(pantalla, fuente):
        estado_juego['laberinto_tickets_ganados'] = 0
        estado_juego['laberinto_tiempo_final'] = 0
        estado_juego['laberinto_mensaje_resultado'] = "Juego cancelado"
        return "laberinto_resultado", estado_juego
    
    # Configuración inicial - USAR LAS DIMENSIONES VALIDADAS
    dificultad = 'facil'  
    if 'dificultad_laberinto' in estado_juego:
        dificultad = estado_juego['dificultad_laberinto']
        laberinto = crear_laberinto(filas, columnas, dificultad)
    
    # VERIFICAR DIMENSIONES DEL LABERINTO CREADO
    print(f"📐 Laberinto creado: {len(laberinto)}x{len(laberinto[0])}")
    
    jugador_pos = (0, 0)
    direccion = 'derecha'
    tiempo_inicio = time.time()
    tiempo_limite = 120
    uso_resolver = False
    solucion = None
    modo_resolver = False
    
    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)
        
        # Procesar eventos
        eventos_procesados = False
        for evento in pygame.event.get():
            eventos_procesados = True
            if evento.type == pygame.QUIT:
                estado_juego['laberinto_tickets_ganados'] = 0
                estado_juego['laberinto_tiempo_final'] = tiempo_transcurrido
                estado_juego['laberinto_mensaje_resultado'] = "Juego interrumpido"
                return "laberinto_resultado", estado_juego
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_juego['laberinto_tickets_ganados'] = 0
                    estado_juego['laberinto_tiempo_final'] = tiempo_transcurrido
                    estado_juego['laberinto_mensaje_resultado'] = "Juego cancelado"
                    return "laberinto_resultado", estado_juego
                elif evento.key == pygame.K_r and not uso_resolver:
                    # Mostrar solución
                    uso_resolver = True
                    modo_resolver = True
                    solucion = resolver_laberinto(laberinto, jugador_pos)
                elif evento.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    # Movimiento del jugador
                    if evento.key == pygame.K_w:
                        direccion = 'arriba'
                    elif evento.key == pygame.K_s:
                        direccion = 'abajo'
                    elif evento.key == pygame.K_a:
                        direccion = 'izquierda'
                    elif evento.key == pygame.K_d:
                        direccion = 'derecha'
                    
                    jugador_pos, direccion = mover_jugador(laberinto, jugador_pos, direccion)
        
        # Si no hay eventos, continuar el bucle
        if not eventos_procesados:
            pass
        
        # Verificar condiciones de fin de juego
        fila_actual, col_actual = jugador_pos
        
        # Verificar si la posición del jugador es válida
        if (fila_actual < 0 or fila_actual >= len(laberinto) or 
            col_actual < 0 or col_actual >= len(laberinto[0])):
            # Posición inválida, resetear a entrada
            jugador_pos = (0, 0)
            fila_actual, col_actual = jugador_pos
        
        # Llegó a la salida
        if (fila_actual < len(laberinto) and col_actual < len(laberinto[0]) and 
            laberinto[fila_actual][col_actual] == 'S'):
            tickets_ganados = calcular_tickets_ganados(tiempo_transcurrido, uso_resolver)
            
            # Actualizar estado del juego con resultados
            estado_juego['laberinto_tickets_ganados'] = tickets_ganados
            estado_juego['laberinto_tiempo_final'] = tiempo_transcurrido
            
            if uso_resolver:
                estado_juego['laberinto_mensaje_resultado'] = "¡Completado con ayuda!"
            elif tiempo_transcurrido < 30:
                estado_juego['laberinto_mensaje_resultado'] = "¡Velocidad increíble!"
            elif tiempo_transcurrido < 60:
                estado_juego['laberinto_mensaje_resultado'] = "¡Excelente tiempo!"
            else:
                estado_juego['laberinto_mensaje_resultado'] = "¡Bien hecho!"
            
            # Actualizar estadísticas del usuario
            if estado_juego['usuario_actual'] and estado_juego['usuario_actual'] in estado_juego['usuarios']:
                usuario = estado_juego['usuarios'][estado_juego['usuario_actual']]
                usuario['total_boletos'] += tickets_ganados
                estado_juego['configuraciones']['tickets_conseguidos'] = tickets_ganados
                
                # Guardar cambios
                from logica_juego import guardar_json
                guardar_json("z_usuarios.json", estado_juego['usuarios'])
            
            return "laberinto_resultado", estado_juego
        
        # Tiempo agotado
        if tiempo_restante <= 0:
            estado_juego['laberinto_tickets_ganados'] = 0
            estado_juego['laberinto_tiempo_final'] = tiempo_transcurrido
            estado_juego['laberinto_mensaje_resultado'] = "¡Tiempo agotado!"
            
            if estado_juego['usuario_actual'] and estado_juego['usuario_actual'] in estado_juego['usuarios']:
                estado_juego['configuraciones']['tickets_conseguidos'] = 0
            
            return "laberinto_resultado", estado_juego
        
        # Dibujar
        pantalla.fill(COLOR_FONDO)
        dibujar_laberinto(pantalla, fuente, laberinto, jugador_pos, tiempo_restante, modo_resolver, solucion)
        pygame.display.flip()
    
    estado_juego['laberinto_tickets_ganados'] = 0
    estado_juego['laberinto_tiempo_final'] = 0
    estado_juego['laberinto_mensaje_resultado'] = "Juego finalizado"
    estado_juego['diccionario_botones_laberinto'] = inicializar_botones_laberinto(MENU_LABERINTO_RESULTADO)
    return "laberinto_resultado", estado_juego

def dibujar_laberinto(pantalla, fuente, laberinto, jugador_pos, tiempo_restante, modo_resolver=False, solucion=None):
    """Dibuja el laberinto completo en PyGame"""
    filas = len(laberinto)
    columnas = len(laberinto[0])

    #para centrar el laberinto
    MARGEN_X, MARGEN_Y = calcular_margenes_centrados(columnas, filas)

    # Dibujar información del juego
    minutos = int(tiempo_restante // 60)
    segundos = int(tiempo_restante % 60)
    
    # Color del tiempo según lo que queda
    if tiempo_restante > 60:
        color_tiempo = COLOR_TIEMPO_BUENO
    elif tiempo_restante > 30:
        color_tiempo = COLOR_TIEMPO_MEDIO
    else:
        color_tiempo = COLOR_TIEMPO_MALO

    texto_tiempo = fuente.render(f"Tiempo: {minutos}:{segundos:02d}", True, color_tiempo)
    pantalla.blit(texto_tiempo, (MARGEN_X, 50))
    
    texto_instrucciones = fuente.render("Movimiento: WASD | R: Mostrar solución", True, COLOR_TEXTO)
    pantalla.blit(texto_instrucciones, (MARGEN_X, 80))
    
    # Dibujar cada celda del laberinto
    for fila in range(filas):
        for columna in range(columnas):
            x = MARGEN_X + columna * CELDA_SIZE
            y = MARGEN_Y + fila * CELDA_SIZE
            
            # Dibujar fondo de celda
            if laberinto[fila][columna] == 'E':
                pygame.draw.rect(pantalla, COLOR_ENTRADA, (x, y, CELDA_SIZE, CELDA_SIZE))
            elif laberinto[fila][columna] == 'S':
                pygame.draw.rect(pantalla, COLOR_SALIDA, (x, y, CELDA_SIZE, CELDA_SIZE))
            elif laberinto[fila][columna] == '#':
                pygame.draw.rect(pantalla, COLOR_PARED, (x, y, CELDA_SIZE, CELDA_SIZE))
            else:
                pygame.draw.rect(pantalla, COLOR_CELDA_VACIA, (x, y, CELDA_SIZE, CELDA_SIZE))
            
            # Dibujar bordes
            pygame.draw.rect(pantalla, (200, 200, 200), (x, y, CELDA_SIZE, CELDA_SIZE), 1)
            
            # Dibujar contenido de celda
            if laberinto[fila][columna] == '/':
                # Dibujar espejo /
                pygame.draw.line(pantalla, COLOR_ESPEO, (x + 5, y + CELDA_SIZE - 5), (x + CELDA_SIZE - 5, y + 5), 3)
            elif laberinto[fila][columna] == '\\':
                # Dibujar espejo \
                pygame.draw.line(pantalla, COLOR_ESPEO, (x + 5, y + 5), (x + CELDA_SIZE - 5, y + CELDA_SIZE - 5), 3)
            elif laberinto[fila][columna] == 'E':
                texto = fuente.render("E", True, (255, 255, 255))
                pantalla.blit(texto, (x + 15, y + 10))
            elif laberinto[fila][columna] == 'S':
                texto = fuente.render("S", True, (255, 255, 255))
                pantalla.blit(texto, (x + 15, y + 10))
    
    # Dibujar jugador
    jugador_x = MARGEN_X + jugador_pos[1] * CELDA_SIZE + CELDA_SIZE // 2
    jugador_y = MARGEN_Y + jugador_pos[0] * CELDA_SIZE + CELDA_SIZE // 2
    pygame.draw.circle(pantalla, COLOR_JUGADOR, (jugador_x, jugador_y), CELDA_SIZE // 3)
    
    # Dibujar solución si está activo el modo resolver
    if modo_resolver and solucion:
        for i in range(len(solucion) - 1):
            pos_actual = solucion[i]
            pos_siguiente = solucion[i + 1]
            
            x1 = MARGEN_X + pos_actual[1] * CELDA_SIZE + CELDA_SIZE // 2
            y1 = MARGEN_Y + pos_actual[0] * CELDA_SIZE + CELDA_SIZE // 2
            x2 = MARGEN_X + pos_siguiente[1] * CELDA_SIZE + CELDA_SIZE // 2
            y2 = MARGEN_Y + pos_siguiente[0] * CELDA_SIZE + CELDA_SIZE // 2
            
            pygame.draw.line(pantalla, (255, 255, 0), (x1, y1), (x2, y2), 2)

def mover_jugador(laberinto, pos, direccion):
    """Mueve al jugador y aplica rebotes en diagonal con espejos"""
    fila, col = pos
    hubo_rebote = False
    direccion_rebote = direccion
    
    # Calcular próxima posición
    delta_fila, delta_col = 0, 0
    if direccion == 'arriba':
        delta_fila = -1
    elif direccion == 'abajo':
        delta_fila = 1
    elif direccion == 'izquierda':
        delta_col = -1
    elif direccion == 'derecha':
        delta_col = 1
    elif 'diagonal' in direccion:
        if 'sup' in direccion:
            delta_fila = -1
        else:
            delta_fila = 1
        if 'der' in direccion:
            delta_col = 1
        else:
            delta_col = -1
    
    nueva_fila, nueva_col = fila + delta_fila, col + delta_col
    
    # Verificar rebote en espejo
    if (0 <= nueva_fila < len(laberinto) and 0 <= nueva_col < len(laberinto[0])):
        if laberinto[nueva_fila][nueva_col] in ['/', '\\']:
            espejo = laberinto[nueva_fila][nueva_col]
            if espejo == '/':
                if direccion == 'arriba':
                    direccion_rebote = 'diagonal_sup_der'
                elif direccion == 'derecha':
                    direccion_rebote = 'diagonal_sup_der'
                elif direccion == 'abajo':
                    direccion_rebote = 'diagonal_inf_izq'
                elif direccion == 'izquierda':
                    direccion_rebote = 'diagonal_inf_izq'
            else:  # espejo '\'
                if direccion == 'arriba':
                    direccion_rebote = 'diagonal_sup_izq'
                elif direccion == 'izquierda':
                    direccion_rebote = 'diagonal_sup_izq'
                elif direccion == 'abajo':
                    direccion_rebote = 'diagonal_inf_der'
                elif direccion == 'derecha':
                    direccion_rebote = 'diagonal_inf_der'
            
            hubo_rebote = True
            
            # Recalcular movimiento con nueva dirección
            if 'sup' in direccion_rebote:
                delta_fila = -1
            else:
                delta_fila = 1
            if 'der' in direccion_rebote:
                delta_col = 1
            else:
                delta_col = -1
            
            nueva_fila, nueva_col = fila + delta_fila, col + delta_col
    
    # Verificar límites y paredes
    if (nueva_fila < 0 or nueva_fila >= len(laberinto) or 
        nueva_col < 0 or nueva_col >= len(laberinto[0]) or 
        laberinto[nueva_fila][nueva_col] == '#'):
        nueva_pos = pos
    else:
        nueva_pos = (nueva_fila, nueva_col)
    
    return nueva_pos, direccion_rebote if hubo_rebote else direccion

def resolver_laberinto(laberinto, pos, visitados=None, camino=None):
    """Función recursiva que encuentra una solución (camino de E a S)."""
    
    # Verificar que el laberinto existe y tiene dimensiones válidas
    if not laberinto or len(laberinto) == 0 or len(laberinto[0]) == 0:
        return None
    
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []
    
    fila, col = pos
    resultado = None

    # Verificar que la posición está dentro de los límites
    if (fila < 0 or fila >= len(laberinto) or 
        col < 0 or col >= len(laberinto[0])):
        return None

    if laberinto[fila][col] == 'S':
        resultado = camino + [pos]
    
    elif pos in visitados or laberinto[fila][col] == '#':
        resultado = None
    
    else:
        visitados.add(pos)
        for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
            nueva_pos, _ = mover_jugador(laberinto, pos, direccion)
            if nueva_pos != pos:
                solucion = resolver_laberinto(laberinto, nueva_pos, visitados, camino + [pos])
                if solucion:
                    resultado = solucion
                    break  

    return resultado

def calcular_tickets_ganados(tiempo_transcurrido, uso_resolver=False):
    """Calcula los tickets ganados según el tiempo y si usó resolver"""
    if uso_resolver:
        return 7
    
    if tiempo_transcurrido < 30:
        return 60
    elif tiempo_transcurrido < 60:
        return 30
    elif tiempo_transcurrido < 120:
        return 15
    else:
        return 0

def mostrar_tabla_recompensas(pantalla, fuente, diccionario_botones=None):
    """Muestra la tabla de recompensas al inicio del juego"""
    # Si no se pasan botones, crear uno temporal
    if diccionario_botones is None:
        diccionario_botones = {
            'boton_volver_instrucciones': {
                'x': 20, 'y': 20, 
                'ancho': 210, 'alto': 40, 
                'texto': 'VOLVER AL MENÚ', 
                'color_normal': (180, 70, 70),
                'presionado': False
            }
        }
    
    # Importar aquí para evitar dependencia circular
    from botones_funciones import procesar_botones, dibujar_botones
    from verificaciones_botones import obtener_botones_presionados
    
    esperando = True
    resultado = True  # True = continuar, False = cancelar
    
    while esperando:
        # Procesar TODOS los eventos primero
        eventos = pygame.event.get()
        
        # Procesar botones con los eventos
        diccionario_botones = procesar_botones(pantalla, fuente, eventos, diccionario_botones)
        
        # Obtener botones presionados
        botones_presionados = obtener_botones_presionados(diccionario_botones)
        
        # Verificar si se presionó el botón de volver
        if 'boton_volver_instrucciones' in botones_presionados:
            resultado = False
            esperando = False
            break  # Salir inmediatamente
        
        # Verificar otros eventos
        for evento in eventos:
            if evento.type == pygame.QUIT:
                resultado = False
                esperando = False
                break
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    resultado = True
                    esperando = False
                    break
                elif evento.key == pygame.K_ESCAPE:
                    resultado = False
                    esperando = False
                    break
        
        # Solo dibujar si todavía estamos esperando
        if esperando:
            pantalla.fill(COLOR_FONDO)
            
            # Dibujar título
            titulo = fuente.render("🏆 LABERINTO DE ESPEJOS 🏆", True, (255, 255, 0))
            pantalla.blit(titulo, (250, 100))
            
            recompensas = [
                "TABLA DE RECOMPENSAS:",
                "⚡ Menos de 30 segundos: 60 tickets",
                "🔥 Menos de 1 minuto: 30 tickets", 
                "👍 Menos de 2 minutos: 15 tickets",
                "❌ Más de 2 minutos: 0 tickets",
                "⚠️  Pedir ayuda (R): 7 tickets",
                "",
                "Controles:",
                "W - Arriba",
                "A - Izquierda", 
                "S - Abajo",
                "D - Derecha",
                "R - Mostrar solución",
                "",
                "Presiona ESPACIO para comenzar"
            ]
            
            for i, linea in enumerate(recompensas):
                texto = fuente.render(linea, True, COLOR_TEXTO)
                pantalla.blit(texto, (200, 150 + i * 30))
            
            # Dibujar botón
            dibujar_botones(pantalla, fuente, diccionario_botones)
            
            pygame.display.flip()
    
    return resultado
