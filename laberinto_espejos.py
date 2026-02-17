

import random
import time
import pygame
from laberintos_predeterminados import obtener_laberinto_manual

# ──────────────────────────────────────────────────────────────────────────
# 🎨 CONSTANTES DE CONFIGURACIÓN
# ──────────────────────────────────────────────────────────────────────────

# Dimensiones de la pantalla
ANCHO_PANTALLA = 1000 
ALTO_PANTALLA = 700 

# Tamaño de celda (píxeles)
CELDA_SIZE = 40  

# 🎨 Paleta de colores
COLOR_FONDO = (25, 25, 50)           # Azul noche
COLOR_CELDA_VACIA = (50, 50, 80)     # Gris azulado
COLOR_PARED = (100, 50, 50)          # Rojo ladrillo
COLOR_ENTRADA = (50, 180, 50)        # Verde
COLOR_SALIDA = (180, 50, 50)         # Rojo
COLOR_JUGADOR = (255, 255, 0)        # Amarillo
COLOR_ESPEO = (100, 200, 255)        # Celeste
COLOR_TEXTO = (255, 255, 255)        # Blanco
COLOR_TIEMPO_BUENO = (50, 255, 50)   # Verde (mucho tiempo)
COLOR_TIEMPO_MEDIO = (255, 255, 50)  # Amarillo (tiempo medio)
COLOR_TIEMPO_MALO = (255, 50, 50)    # Rojo (poco tiempo)

# ──────────────────────────────────────────────────────────────────────────
# 📐 FUNCIONES AUXILIARES DE POSICIONAMIENTO
# ──────────────────────────────────────────────────────────────────────────

def calcular_margenes_centrados(columnas, filas, espacio_ui_superior=150):
    """
    📐 Centra el laberinto en la pantalla.
    
    Args:
        columnas: Ancho del laberinto en celdas
        filas: Alto del laberinto en celdas
        espacio_ui_superior: Espacio reservado arriba para textos
    
    Returns:
        tuple: (margen_x, margen_y) posición superior izquierda para dibujar
    """
    laberinto_ancho = columnas * CELDA_SIZE
    laberinto_alto = filas * CELDA_SIZE
    
    margen_x = (ANCHO_PANTALLA - laberinto_ancho) // 2
    espacio_disponible = ALTO_PANTALLA - espacio_ui_superior
    margen_y = espacio_ui_superior + max(0, (espacio_disponible - laberinto_alto) // 2)
    
    return max(0, margen_x), max(espacio_ui_superior, margen_y)


# ──────────────────────────────────────────────────────────────────────────
# 🏗️ GENERACIÓN DEL LABERINTO
# ──────────────────────────────────────────────────────────────────────────

def crear_laberinto(filas, columnas, dificultad="facil", intentos_max=80):
    """
    🏗️ Genera un laberinto aleatorio o carga uno predeterminado.
    
    Estrategia:
    1. Intenta generar un laberinto aleatorio con 30% paredes, 10% espejos
    2. Verifica que sea resoluble (camino E → S)
    3. Si falla, usa un mapa manual según dificultad
    
    Args:
        filas, columnas: Dimensiones deseadas
        dificultad: "facil", "medio", "dificil", "deathrow"
        intentos_max: Intentos de generación aleatoria
    
    Returns:
        list: Matriz 2D del laberinto
    """
    # Limitar dimensiones para que entren en pantalla
    max_filas = (ALTO_PANTALLA - 50) // CELDA_SIZE
    max_columnas = ANCHO_PANTALLA // CELDA_SIZE
    
    filas = max(5, min(filas, max_filas, 23))
    columnas = max(5, min(columnas, max_columnas, 22))
    
    laberinto_valido_encontrado = False
    laberinto_final = None
    
    for intento in range(intentos_max):
        laberinto = [[' ' for _ in range(columnas)] for _ in range(filas)]

        # Generación aleatoria de paredes y espejos
        for i in range(filas):
            for j in range(columnas):
                if random.random() < 0.3:
                    laberinto[i][j] = '#'
                elif random.random() < 0.1:
                    laberinto[i][j] = random.choice(['/', '\\'])
        
        # Esquinas: entrada (0,0) y salida (f-1,c-1)
        laberinto[0][0] = 'E'
        laberinto[filas-1][columnas-1] = 'S'
        
        if resolver_laberinto(laberinto, (0, 0)) is not None:
            laberinto_valido_encontrado = True
            laberinto_final = laberinto
            break
    
    if not laberinto_valido_encontrado:
        print(f"⚠️ Usando mapa manual para dificultad: {dificultad}")
        laberinto_final = obtener_laberinto_manual(dificultad, filas, columnas)
    
    return laberinto_final


# ──────────────────────────────────────────────────────────────────────────
# 🎮 JUEGO PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────

def iniciar_juego_laberinto(pantalla, fuente, estado_juego, filas=10, columnas=15):
    """
    🎮 Punto de entrada al minijuego del laberinto.
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente para textos
        estado_juego: Diccionario de estado global
        filas, columnas: Dimensiones del laberinto
    
    Returns:
        tuple: (nuevo_estado, estado_juego_actualizado)
    """
    # ── 1. INICIAR MÚSICA DEL LABERINTO ───────────────────
    from y_musica import musica_cargar_y_reproducir
    
    volumen = estado_juego.get('musica_volumen', 0.5)
    if estado_juego.get('musica_mute', False):
        volumen = 0.0
    
    print("🎵 Iniciando música del laberinto...")
    exito = musica_cargar_y_reproducir('laberinto_espejos', volumen)
    if not exito:
        musica_cargar_y_reproducir('electro_swing', volumen)
    
    # ── 2. VALIDAR DIMENSIONES ────────────────────────────
    print(f"🔍 Laberinto recibió: {filas}x{columnas}")
    if filas < 5 or filas > 40 or columnas < 5 or columnas > 40:
        print("❌ Dimensiones inválidas, usando 10x15")
        filas, columnas = 10, 15
    
    # ── 3. MOSTRAR TABLA DE RECOMPENSAS ───────────────────
    if not mostrar_tabla_recompensas(pantalla, fuente):
        # Jugador canceló
        estado_juego.update({
            'laberinto_tickets_ganados': 0,
            'laberinto_tiempo_final': 0,
            'laberinto_mensaje_resultado': "Juego cancelado"
        })
        return "laberinto_resultado", estado_juego
    
    # ── 4. CREAR LABERINTO ────────────────────────────────
    dificultad = estado_juego.get('dificultad_laberinto', 'facil')
    laberinto = crear_laberinto(filas, columnas, dificultad)
    print(f"📐 Laberinto creado: {len(laberinto)}x{len(laberinto[0])}")
    
    # ── 5. ESTADO INICIAL DEL JUEGO ───────────────────────
    jugador_pos = (0, 0)
    direccion = 'derecha'
    tiempo_inicio = time.time()
    tiempo_limite = 120
    uso_resolver = False
    solucion = None
    modo_resolver = False
    
    # ── 6. BUCLE PRINCIPAL ────────────────────────────────
    ejecutando = True
    while ejecutando:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)
        
        # ── 6.1 PROCESAR EVENTOS ──────────────────────────
        eventos_procesados = False
        for evento in pygame.event.get():
            eventos_procesados = True
            
            if evento.type == pygame.QUIT:
                estado_juego.update({
                    'laberinto_tickets_ganados': 0,
                    'laberinto_tiempo_final': tiempo_transcurrido,
                    'laberinto_mensaje_resultado': "Juego interrumpido"
                })
                return "laberinto_resultado", estado_juego
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_juego.update({
                        'laberinto_tickets_ganados': 0,
                        'laberinto_tiempo_final': tiempo_transcurrido,
                        'laberinto_mensaje_resultado': "Juego cancelado"
                    })
                    return "laberinto_resultado", estado_juego
                
                elif evento.key == pygame.K_r and not uso_resolver:
                    # Mostrar solución
                    uso_resolver = True
                    modo_resolver = True
                    solucion = resolver_laberinto(laberinto, jugador_pos)
                
                elif evento.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    # Movimiento WASD
                    if evento.key == pygame.K_w:
                        direccion = 'arriba'
                    elif evento.key == pygame.K_s:
                        direccion = 'abajo'
                    elif evento.key == pygame.K_a:
                        direccion = 'izquierda'
                    elif evento.key == pygame.K_d:
                        direccion = 'derecha'
                    
                    jugador_pos, direccion = mover_jugador(laberinto, jugador_pos, direccion)
        
        # ── 6.2 VERIFICAR CONDICIONES DE FIN ──────────────
        fila_actual, col_actual = jugador_pos
        
        # Validar posición (por si se sale)
        if (fila_actual < 0 or fila_actual >= len(laberinto) or 
            col_actual < 0 or col_actual >= len(laberinto[0])):
            jugador_pos = (0, 0)
            fila_actual, col_actual = jugador_pos
        
        # 🏆 Llegó a la salida
        if (fila_actual < len(laberinto) and col_actual < len(laberinto[0]) and 
            laberinto[fila_actual][col_actual] == 'S'):
            
            tickets_ganados = calcular_tickets_ganados(tiempo_transcurrido, uso_resolver)
            
            # Actualizar estado
            estado_juego.update({
                'laberinto_tickets_ganados': tickets_ganados,
                'laberinto_tiempo_final': tiempo_transcurrido,
                'laberinto_mensaje_resultado': (
                    "¡Completado con ayuda!" if uso_resolver else
                    "¡Velocidad increíble!" if tiempo_transcurrido < 30 else
                    "¡Excelente tiempo!" if tiempo_transcurrido < 60 else
                    "¡Bien hecho!"
                )
            })
            
            # Actualizar estadísticas del usuario
            if estado_juego.get('usuario_actual') and estado_juego['usuario_actual'] in estado_juego['usuarios']:
                usuario = estado_juego['usuarios'][estado_juego['usuario_actual']]
                usuario['total_boletos'] += tickets_ganados
                estado_juego['configuraciones']['tickets_conseguidos'] = tickets_ganados
                
                from logica_juego import guardar_json
                guardar_json("z_usuarios.json", estado_juego['usuarios'])
            
            return "laberinto_resultado", estado_juego
        
        # ⏰ Tiempo agotado
        if tiempo_restante <= 0:
            estado_juego.update({
                'laberinto_tickets_ganados': 0,
                'laberinto_tiempo_final': tiempo_transcurrido,
                'laberinto_mensaje_resultado': "¡Tiempo agotado!"
            })
            estado_juego['configuraciones']['tickets_conseguidos'] = 0
            return "laberinto_resultado", estado_juego
        
        # ── 6.3 DIBUJAR ───────────────────────────────────
        pantalla.fill(COLOR_FONDO)
        dibujar_laberinto(pantalla, fuente, laberinto, jugador_pos, 
                         tiempo_restante, modo_resolver, solucion)
        pygame.display.flip()
    
    # ── 7. SALIDA POR FUERA DEL BUCLE (NO DEBERÍA LLEGAR) ──
    estado_juego.update({
        'laberinto_tickets_ganados': 0,
        'laberinto_tiempo_final': 0,
        'laberinto_mensaje_resultado': "Juego finalizado"
    })
    return "laberinto_resultado", estado_juego


# ──────────────────────────────────────────────────────────────────────────
# 🖌️ DIBUJADO
# ──────────────────────────────────────────────────────────────────────────

def dibujar_laberinto(pantalla, fuente, laberinto, jugador_pos, 
                      tiempo_restante, modo_resolver=False, solucion=None):
    """
    🖌️ Renderiza el laberinto completo en pantalla.
    
    Dibuja:
    - Celdas (vacías, paredes, entrada, salida)
    - Espejos (/ y \)
    - Jugador (círculo amarillo)
    - Temporizador con colores dinámicos
    - Solución (si está activada)
    """
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    MARGEN_X, MARGEN_Y = calcular_margenes_centrados(columnas, filas)
    
    # ── Temporizador con color según urgencia ────────────
    minutos = int(tiempo_restante // 60)
    segundos = int(tiempo_restante % 60)
    
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
    
    # ── Dibujar celdas ───────────────────────────────────
    for fila in range(filas):
        for columna in range(columnas):
            x = MARGEN_X + columna * CELDA_SIZE
            y = MARGEN_Y + fila * CELDA_SIZE
            
            # Fondo según tipo de celda
            if laberinto[fila][columna] == 'E':
                pygame.draw.rect(pantalla, COLOR_ENTRADA, (x, y, CELDA_SIZE, CELDA_SIZE))
            elif laberinto[fila][columna] == 'S':
                pygame.draw.rect(pantalla, COLOR_SALIDA, (x, y, CELDA_SIZE, CELDA_SIZE))
            elif laberinto[fila][columna] == '#':
                pygame.draw.rect(pantalla, COLOR_PARED, (x, y, CELDA_SIZE, CELDA_SIZE))
            else:
                pygame.draw.rect(pantalla, COLOR_CELDA_VACIA, (x, y, CELDA_SIZE, CELDA_SIZE))
            
            # Borde
            pygame.draw.rect(pantalla, (200, 200, 200), (x, y, CELDA_SIZE, CELDA_SIZE), 1)
            
            # Contenido (espejos o letras)
            if laberinto[fila][columna] == '/':
                pygame.draw.line(pantalla, COLOR_ESPEO, 
                               (x + 5, y + CELDA_SIZE - 5), 
                               (x + CELDA_SIZE - 5, y + 5), 3)
            elif laberinto[fila][columna] == '\\':
                pygame.draw.line(pantalla, COLOR_ESPEO, 
                               (x + 5, y + 5), 
                               (x + CELDA_SIZE - 5, y + CELDA_SIZE - 5), 3)
            elif laberinto[fila][columna] == 'E':
                texto = fuente.render("E", True, (255, 255, 255))
                pantalla.blit(texto, (x + 15, y + 10))
            elif laberinto[fila][columna] == 'S':
                texto = fuente.render("S", True, (255, 255, 255))
                pantalla.blit(texto, (x + 15, y + 10))
    
    # ── Dibujar jugador (círculo) ────────────────────────
    jugador_x = MARGEN_X + jugador_pos[1] * CELDA_SIZE + CELDA_SIZE // 2
    jugador_y = MARGEN_Y + jugador_pos[0] * CELDA_SIZE + CELDA_SIZE // 2
    pygame.draw.circle(pantalla, COLOR_JUGADOR, (jugador_x, jugador_y), CELDA_SIZE // 3)
    
    # ── Dibujar solución (línea amarilla) ────────────────
    if modo_resolver and solucion:
        for i in range(len(solucion) - 1):
            pos_actual = solucion[i]
            pos_siguiente = solucion[i + 1]
            
            x1 = MARGEN_X + pos_actual[1] * CELDA_SIZE + CELDA_SIZE // 2
            y1 = MARGEN_Y + pos_actual[0] * CELDA_SIZE + CELDA_SIZE // 2
            x2 = MARGEN_X + pos_siguiente[1] * CELDA_SIZE + CELDA_SIZE // 2
            y2 = MARGEN_Y + pos_siguiente[0] * CELDA_SIZE + CELDA_SIZE // 2
            
            pygame.draw.line(pantalla, (255, 255, 0), (x1, y1), (x2, y2), 2)


# ──────────────────────────────────────────────────────────────────────────
# 🕹️ LÓGICA DE MOVIMIENTO Y FÍSICA
# ──────────────────────────────────────────────────────────────────────────

def mover_jugador(laberinto, pos, direccion):
    """
    🕹️ Calcula nueva posición del jugador considerando espejos.
    
    Los espejos (/ y \) desvían el movimiento en diagonal:
    - /  : derecha → diagonal_sup_der,  arriba → diagonal_sup_der
    - \  : izquierda → diagonal_sup_izq, arriba → diagonal_sup_izq
    
    Returns:
        tuple: (nueva_posición, nueva_dirección)
    """
    fila, col = pos
    hubo_rebote = False
    direccion_rebote = direccion
    
    # Calcular delta según dirección
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
        delta_fila = -1 if 'sup' in direccion else 1
        delta_col = 1 if 'der' in direccion else -1
    
    nueva_fila, nueva_col = fila + delta_fila, col + delta_col
    
    # Verificar rebote en espejo
    if (0 <= nueva_fila < len(laberinto) and 0 <= nueva_col < len(laberinto[0])):
        if laberinto[nueva_fila][nueva_col] in ['/', '\\']:
            espejo = laberinto[nueva_fila][nueva_col]
            
            if espejo == '/':
                if direccion in ['arriba', 'derecha']:
                    direccion_rebote = 'diagonal_sup_der'
                else:  # abajo, izquierda
                    direccion_rebote = 'diagonal_inf_izq'
            else:  # espejo '\'
                if direccion in ['arriba', 'izquierda']:
                    direccion_rebote = 'diagonal_sup_izq'
                else:  # abajo, derecha
                    direccion_rebote = 'diagonal_inf_der'
            
            hubo_rebote = True
            
            # Recalcular con nueva dirección
            delta_fila = -1 if 'sup' in direccion_rebote else 1
            delta_col = 1 if 'der' in direccion_rebote else -1
            nueva_fila, nueva_col = fila + delta_fila, col + delta_col
    
    # Validar movimiento (paredes y bordes)
    if (nueva_fila < 0 or nueva_fila >= len(laberinto) or 
        nueva_col < 0 or nueva_col >= len(laberinto[0]) or 
        laberinto[nueva_fila][nueva_col] == '#'):
        nueva_pos = pos
    else:
        nueva_pos = (nueva_fila, nueva_col)
    
    return nueva_pos, direccion_rebote if hubo_rebote else direccion


# ──────────────────────────────────────────────────────────────────────────
# 🧩 ALGORITMO DE RESOLUCIÓN
# ──────────────────────────────────────────────────────────────────────────

def resolver_laberinto(laberinto, pos, visitados=None, camino=None):
    """
    🧩 Encuentra un camino desde la entrada hasta la salida (DFS recursivo).
    
    Args:
        laberinto: Matriz 2D
        pos: Posición actual (fila, columna)
        visitados: Set de posiciones ya exploradas
        camino: Lista del recorrido actual
    
    Returns:
        list: Lista de posiciones desde E hasta S, o None si no hay solución
    """
    if not laberinto or len(laberinto) == 0 or len(laberinto[0]) == 0:
        return None
    
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []
    
    fila, col = pos
    
    # Fuera de límites
    if (fila < 0 or fila >= len(laberinto) or 
        col < 0 or col >= len(laberinto[0])):
        return None
    
    # Caso base: llegó a la salida
    if laberinto[fila][col] == 'S':
        return camino + [pos]
    
    # Pared, ya visitado o espejo (no se puede pisar)
    if pos in visitados or laberinto[fila][col] in ['#', '/', '\\']:
        return None
    
    visitados.add(pos)
    
    for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
        nueva_pos, _ = mover_jugador(laberinto, pos, direccion)
        if nueva_pos != pos:
            solucion = resolver_laberinto(laberinto, nueva_pos, visitados, camino + [pos])
            if solucion:
                return solucion
    
    return None


# ──────────────────────────────────────────────────────────────────────────
# 💰 CÁLCULO DE RECOMPENSAS
# ──────────────────────────────────────────────────────────────────────────

def calcular_tickets_ganados(tiempo_transcurrido, uso_resolver=False):
    """
    💰 Calcula tickets según tiempo y si pidió ayuda.
    
    Reglas:
    - Con ayuda: 7 tickets
    - < 30s: 60 tickets
    - < 60s: 30 tickets
    - < 120s: 15 tickets
    - > 120s: 0 tickets
    """
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


# ──────────────────────────────────────────────────────────────────────────
# 📋 PANTALLA DE INSTRUCCIONES
# ──────────────────────────────────────────────────────────────────────────

def mostrar_tabla_recompensas(pantalla, fuente, diccionario_botones=None):
    """
    📋 Muestra pantalla con reglas, controles y botón de volver.
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente para textos
        diccionario_botones: Botón "VOLVER" (se crea uno por defecto si no existe)
    
    Returns:
        bool: True = comenzar juego, False = volver al menú
    """
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
    
    from botones_funciones import procesar_botones, dibujar_botones
    from verificaciones_botones import obtener_botones_presionados
    
    esperando = True
    resultado = True  # True = continuar
    
    while esperando:
        eventos = pygame.event.get()
        
        # Procesar interacción con botones
        diccionario_botones = procesar_botones(pantalla, fuente, eventos, diccionario_botones)
        botones_presionados = obtener_botones_presionados(diccionario_botones)
        
        # Botón "VOLVER"
        if 'boton_volver_instrucciones' in botones_presionados:
            resultado = False
            esperando = False
            break
        
        # Otros eventos (teclas)
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
        
        if esperando:
            # Dibujar interfaz
            pantalla.fill(COLOR_FONDO)
            
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
            
            dibujar_botones(pantalla, fuente, diccionario_botones)
            pygame.display.flip()
    
    return resultado