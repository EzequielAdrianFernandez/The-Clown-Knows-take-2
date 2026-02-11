"""
🏆 MÓDULO: leaderboard.py
==========================
Gestiona la obtención y visualización de las tablas de clasificación.

FUNCIONES PRINCIPALES:
1. obtener_leaderboard_record()  → Ranking por MEJOR PARTIDA INDIVIDUAL (record_boletos)
2. obtener_leaderboard_total()   → Ranking por TOTAL ACUMULADO (total_boletos)
3. dibujar_leaderboard_organizado() → Renderiza ambos rankings en pantalla

FLUJO DE DATOS:
manejador_estados.py (caso "leaderboard")
        ↓
dibujar_leaderboard_organizado()
        ↓
obtener_leaderboard_record()  →  ordena por record_boletos (mayor a menor)
obtener_leaderboard_total()   →  ordena por total_boletos (mayor a menor)
        ↓
dibujar_texto_centrado() / dibujar_texto()  ← desde manejador_estados
"""

def obtener_leaderboard_record(usuarios, limite=10):
    """
    🏅 Obtiene el leaderboard ordenado por RECORD (mejor partida individual).
    
    ¿Qué hace?
    - Itera sobre todos los usuarios del sistema
    - Filtra SOLO aquellos con al menos 1 partida jugada (partidas_jugadas > 0)
    - Ordena de MAYOR a MENOR record_boletos
    - Limita a los primeros N (por defecto 10)
    
    Args:
        usuarios (dict): Diccionario de usuarios cargado desde z_usuarios.json
        limite (int): Cantidad máxima de jugadores a mostrar
    
    Returns:
        list: Lista de tuplas con formato:
              (nombre, record_boletos, total_boletos, partidas_jugadas, medallas, usuario_id)
              Ej: ("pachacho", 240, 3844, 38, "🎮🏆👑💰⚡", "usuario_1")
    """
    lista_usuarios = []
    
    # Recorrer todos los usuarios del sistema
    for usuario_id, datos_usuario in usuarios.items():
        nombre = datos_usuario["nombre"]
        record = datos_usuario["record_boletos"]
        total = datos_usuario["total_boletos"]
        partidas = datos_usuario["partidas_jugadas"]
        medallas = datos_usuario["medallas"]
        
        # Solo incluir usuarios CON AL MENOS 1 PARTIDA JUGADA
        if partidas > 0:
            lista_usuarios.append((nombre, record, total, partidas, medallas, usuario_id))
    
    # Ordenar por RECORD (mayor a menor) usando sorted() con lambda
    lista_ordenada = sorted(lista_usuarios, key=lambda x: x[1], reverse=True)
    
    # Limitar a los primeros N y devolver
    return lista_ordenada[:limite]


def obtener_leaderboard_total(usuarios, limite=10):
    """
    🎫 Obtiene el leaderboard ordenado por TOTAL de tickets acumulados.
    
    ¿Qué hace?
    - Itera sobre todos los usuarios del sistema
    - Filtra SOLO aquellos con al menos 1 partida jugada
    - Ordena de MAYOR a MENOR total_boletos
    - Limita a los primeros N (por defecto 10)
    
    Args:
        usuarios (dict): Diccionario de usuarios
        limite (int): Cantidad máxima de jugadores a mostrar
    
    Returns:
        list: Lista de tuplas con formato:
              (nombre, total_boletos, record_boletos, partidas_jugadas, medallas, usuario_id)
              Ej: ("pachacho", 3844, 240, 38, "🎮🏆👑💰⚡", "usuario_1")
    """
    lista_usuarios = []
    
    for usuario_id, datos_usuario in usuarios.items():
        nombre = datos_usuario["nombre"]
        total = datos_usuario["total_boletos"]
        record = datos_usuario["record_boletos"]
        partidas = datos_usuario["partidas_jugadas"]
        medallas = datos_usuario["medallas"]
        
        # Solo incluir usuarios CON AL MENOS 1 PARTIDA
        if partidas > 0:
            lista_usuarios.append((nombre, total, record, partidas, medallas, usuario_id))
    
    # Ordenar por TOTAL (mayor a menor)
    lista_ordenada = sorted(lista_usuarios, key=lambda x: x[1], reverse=True)
    
    return lista_ordenada[:limite]


def dibujar_leaderboard_organizado(pantalla, fuente, estado, inicio_x_izq, distancia_columnas):
    """
    🖼️ Dibuja el leaderboard completo en pantalla con 3 columnas por tabla.
    
    ESTRUCTURA VISUAL:
    
    ┌─────────────────────────────────────────────────────────────────┐
    │                    🏆 LEADERBOARD 🏆                           │
    ├───────────────────────────────────┬───────────────────────────┤
    │      MEJOR PARTIDA               │      TOTAL ACUMULADO      │
    ├───────────────────────────────────┼───────────────────────────┤
    │ 1.  pachacho 🎮🏆👑   240 🎫    │ 1.  pachacho 🎮🏆👑   3844 🎫 │
    │ 2.  germanchin 👑💰    140 🎫    │ 2.  germanchin 👑💰    2038 🎫 │
    │ 3.  echequiel 💡🌟      30 🎫    │ 3.  pachachi 🌟🎮       98 🎫 │
    │ 4.  gonchalo 🎮🍕       18 🎫    │ 4.  maga 🎮💡🧠         30 🎫 │
    │ 5.  pachachi 🌟🎮       15 🎫    │ 5.  gonchalo 🎮🍕       34 🎫 │
    └───────────────────────────────────┴───────────────────────────┘
                          Juega más partidas...
    
    Args:
        pantalla: Superficie de pygame donde dibujar
        fuente: Fuente para textos (con soporte emoji)
        estado: Diccionario de estado del juego (contiene 'usuarios')
        inicio_x_izq: Posición X donde comienza la columna izquierda (ej: 100)
        distancia_columnas: Distancia entre columna izquierda y derecha (ej: 400)
    
    NOTA: Esta función importa dibujar_texto_centrado() y dibujar_texto()
          desde manejador_estados.py (importación local para evitar ciclos)
    """
    # Importación LOCAL para evitar dependencia circular
    from manejador_estados import dibujar_texto_centrado, dibujar_texto  
    
    # ── 1. OBTENER DATOS DE LOS RANKINGS ─────────────────────────
    # Límite fijo de 5 jugadores para que entre en pantalla
    datos_record = obtener_leaderboard_record(estado['usuarios'], limite=5)
    datos_total = obtener_leaderboard_total(estado['usuarios'], limite=5)
    
    # ── 2. TÍTULO PRINCIPAL (centrado en la pantalla) ───────────
    dibujar_texto_centrado(pantalla, fuente, "🏆 LEADERBOARD 🏆", 500, 50, (255, 255, 0))
    
    # ── 3. CONFIGURACIÓN DE COLUMNAS ────────────────────────────
    # Cada columna se define con: [ancho, color, tipo]
    # Los tipos son: "numero" (1.,2.), "nombre" (nombre + medallas), "record/total"
    
    # Columna IZQUIERDA: MEJOR PARTIDA (record)
    config_columnas_record = [
        [50,  (255, 255, 255), "numero"],   # N° de posición
        [350, (200, 200, 255), "nombre"],   # Nombre + medallas
        [80,  (255, 255, 0),   "record"],   # Record + 🎫
    ]
    
    # Columna DERECHA: TOTAL ACUMULADO
    config_columnas_total = [
        [50,  (255, 255, 255), "numero"],   # N° de posición
        [350, (200, 200, 255), "nombre"],   # Nombre + medallas
        [80,  (100, 255, 100), "total"],    # Total + 🎫
    ]
    
    # ── 4. CALCULAR POSICIÓN DE COLUMNA DERECHA ─────────────────
    # Se calcula dinámicamente según inicio_x_izq + distancia_columnas
    inicio_x_der = inicio_x_izq + distancia_columnas
    
    # ────────────────────────────────────────────────────────────
    # 🎯 COLUMNA IZQUIERDA - MEJOR PARTIDA
    # ────────────────────────────────────────────────────────────
    titulo_y = 100           # Posición Y de los títulos
    datos_inicio_y = 140     # Posición Y del primer jugador
    altura_fila = 40         # Espacio vertical entre filas
    
    # Calcular ancho total y centro para titular la columna
    ancho_total_izq = 0
    for config in config_columnas_record:
        ancho_total_izq += config[0]
    centro_izq = inicio_x_izq + (ancho_total_izq // 2)
    
    # Título de columna izquierda
    dibujar_texto_centrado(pantalla, fuente, "MEJOR PARTIDA", 
                          centro_izq, titulo_y, (255, 200, 100))
    
    # Dibujar datos (si hay)
    cantidad_record = len(datos_record)
    if cantidad_record > 0:
        for i in range(cantidad_record):
            usuario_data = datos_record[i]
            nombre = usuario_data[0]
            record = usuario_data[1]
            medallas = usuario_data[4]
            
            y_pos = datos_inicio_y + i * altura_fila
            x_actual = inicio_x_izq
            
            # Dibujar las 3 columnas de esta fila
            for j in range(len(config_columnas_record)):
                config = config_columnas_record[j]
                ancho_columna = config[0]
                color_columna = config[1]
                tipo_columna = config[2]
                
                # Generar texto según el tipo de columna
                texto = ""
                if tipo_columna == "numero":
                    texto = f"{i+1}."
                elif tipo_columna == "nombre":
                    # Limitar nombre a 10 caracteres para que entre
                    nombre_limitado = nombre
                    if len(nombre) > 10:
                        nombre_limitado = nombre[:10]
                    texto = f"{nombre_limitado} {medallas}"
                elif tipo_columna == "record":
                    texto = f"{record} 🎫"  # Emoji de ticket
                
                dibujar_texto(pantalla, fuente, texto, x_actual, y_pos, color_columna)
                x_actual += ancho_columna
    else:
        # Mensaje si no hay jugadores con partidas
        dibujar_texto_centrado(pantalla, fuente, "Sin datos", 
                              centro_izq, datos_inicio_y, (150, 150, 150))
    
    # ────────────────────────────────────────────────────────────
    # 🎯 COLUMNA DERECHA - TOTAL ACUMULADO
    # ────────────────────────────────────────────────────────────
    ancho_total_der = 0
    for config in config_columnas_total:
        ancho_total_der += config[0]
    centro_der = inicio_x_der + (ancho_total_der // 2)
    
    # Título de columna derecha
    dibujar_texto_centrado(pantalla, fuente, "TOTAL ACUMULADO", 
                          centro_der, titulo_y, (255, 200, 100))
    
    # Dibujar datos (si hay)
    cantidad_total = len(datos_total)
    if cantidad_total > 0:
        for i in range(cantidad_total):
            usuario_data = datos_total[i]
            nombre = usuario_data[0]
            total = usuario_data[1]
            medallas = usuario_data[4]
            
            y_pos = datos_inicio_y + i * altura_fila
            x_actual = inicio_x_der
            
            for j in range(len(config_columnas_total)):
                config = config_columnas_total[j]
                ancho_columna = config[0]
                color_columna = config[1]
                tipo_columna = config[2]
                
                texto = ""
                if tipo_columna == "numero":
                    texto = f"{i+1}."
                elif tipo_columna == "nombre":
                    nombre_limitado = nombre
                    if len(nombre) > 10:
                        nombre_limitado = nombre[:10]
                    texto = f"{nombre_limitado} {medallas}"
                elif tipo_columna == "total":
                    texto = f"{total} 🎫"
                
                dibujar_texto(pantalla, fuente, texto, x_actual, y_pos, color_columna)
                x_actual += ancho_columna
    else:
        dibujar_texto_centrado(pantalla, fuente, "Sin datos", 
                              centro_der, datos_inicio_y, (150, 150, 150))
    
    # ────────────────────────────────────────────────────────────
    # 📢 MENSAJES FINALES
    # ────────────────────────────────────────────────────────────
    # Si no hay NINGÚN jugador con partidas
    if cantidad_record == 0 and cantidad_total == 0:
        dibujar_texto_centrado(pantalla, fuente, "¡Aún no hay jugadores con partidas!", 
                              500, datos_inicio_y + 150, (255, 100, 100))
    
    # Llamado a la acción
    dibujar_texto_centrado(pantalla, fuente, "Juega más partidas para subir en el ranking!",
                          500, 550, (200, 200, 200))