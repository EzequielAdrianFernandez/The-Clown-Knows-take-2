def obtener_leaderboard_record(usuarios, limite=10):
    """
    Obtiene el leaderboard ordenado por RECORD (mejor partida).
    
    Args:
        usuarios (dict): Diccionario de usuarios
        limite (int): Cantidad máxima de jugadores a mostrar
    
    Returns:
        list: Lista de tuplas (nombre, record_boletos, total_boletos, partidas_jugadas)
    """
    lista_usuarios = []
    
    for usuario_id, datos_usuario in usuarios.items():
        nombre = datos_usuario["nombre"]
        record = datos_usuario["record_boletos"]
        total = datos_usuario["total_boletos"]
        partidas = datos_usuario["partidas_jugadas"]
        medallas = datos_usuario["medallas"]
        
        # Solo incluir usuarios con al menos 1 partida
        if partidas > 0:
            lista_usuarios.append((nombre, record, total, partidas, medallas, usuario_id))
    
    # Ordenar por RECORD (mayor primero)
    lista_ordenada = sorted(lista_usuarios, key=lambda x: x[1], reverse=True)
    
    # Limitar a los primeros N
    return lista_ordenada[:limite]

def obtener_leaderboard_total(usuarios, limite=10):
    """
    Obtiene el leaderboard ordenado por TOTAL de tickets acumulados.
    
    Args:
        usuarios (dict): Diccionario de usuarios
        limite (int): Cantidad máxima de jugadores a mostrar
    
    Returns:
        list: Lista de tuplas (nombre, total_boletos, record_boletos, partidas_jugadas)
    """
    lista_usuarios = []
    
    for usuario_id, datos_usuario in usuarios.items():
        nombre = datos_usuario["nombre"]
        total = datos_usuario["total_boletos"]
        record = datos_usuario["record_boletos"]
        partidas = datos_usuario["partidas_jugadas"]
        medallas = datos_usuario["medallas"]
        
        # Solo incluir usuarios con al menos 1 partida
        if partidas > 0:
            lista_usuarios.append((nombre, total, record, partidas, medallas, usuario_id))
    
    # Ordenar por TOTAL (mayor primero)
    lista_ordenada = sorted(lista_usuarios, key=lambda x: x[1], reverse=True)
    
    # Limitar a los primeros N
    return lista_ordenada[:limite]

def dibujar_leaderboard_organizado(pantalla, fuente, estado, inicio_x_izq, distancia_columnas):
    """
    Dibuja el leaderboard organizado con 3 columnas cada una.
    
    Args:
        pantalla: Superficie de pygame
        fuente: Fuente para texto
        estado: Estado del juego
        inicio_x_izq: Posición X inicial para columna izquierda
        distancia_columnas: Distancia horizontal entre el inicio de columna izquierda y derecha
    """
    # Importar funciones
    from manejador_estados import dibujar_texto_centrado, dibujar_texto  
    
    # Obtener datos
    datos_record = obtener_leaderboard_record(estado['usuarios'], limite=5)  # ←【LÍMITE JUGADORES: 5】
    datos_total = obtener_leaderboard_total(estado['usuarios'], limite=5)    # ←【LÍMITE JUGADORES: 5】
    
    # Título principal
    dibujar_texto_centrado(pantalla, fuente, "🏆 LEADERBOARD 🏆", 500, 50, (255, 255, 0))
    
    # === CONFIGURACIÓN DE COLUMNAS SIMPLIFICADA (3 COLUMNAS) ===
    # Columna izquierda: RECORD (solo 3 columnas)
    config_columnas_record = [
        [50, (255, 255, 255), "numero"],      # ← Columna 1: Número (más angosto)
        [350, (200, 200, 255), "nombre"],     # ← Columna 2: Nombre + medallas  
        [80, (255, 255, 0), "record"],       # ← Columna 3: Record de tickets
    ]
    
    # Columna derecha: TOTAL (solo 3 columnas)
    config_columnas_total = [
        [50, (255, 255, 255), "numero"],      # ← Columna 1: Número
        [350, (200, 200, 255), "nombre"],     # ← Columna 2: Nombre + medallas
        [80, (100, 255, 100), "total"],      # ← Columna 3: Total acumulado
    ]
    
    # === CALCULAR POSICIÓN COLUMNA DERECHA ===
    inicio_x_der = inicio_x_izq + distancia_columnas
    
    # === DIBUJAR COLUMNA IZQUIERDA (RECORD) ===
    titulo_y = 100                            # ←【POSICIÓN Y TÍTULOS】
    datos_inicio_y = 140                      # ←【POSICIÓN Y INICIO DATOS】
    altura_fila = 40                          # ←【ESPACIADO VERTICAL entre usuarios】
    
    # Calcular ancho total columna izquierda (para centrar título)
    ancho_total_izq = 0
    for config in config_columnas_record:
        ancho_total_izq += config[0]
    centro_izq = inicio_x_izq + (ancho_total_izq // 2)
    
    # Título columna izquierda
    dibujar_texto_centrado(pantalla, fuente, "MEJOR PARTIDA", 
                          centro_izq, titulo_y, (255, 200, 100))
    
    # Dibujar datos de RECORD
    cantidad_record = len(datos_record)
    
    if cantidad_record > 0:
        for i in range(cantidad_record):
            usuario_data = datos_record[i]
            nombre = usuario_data[0]
            record = usuario_data[1]
            medallas = usuario_data[4]  # Solo necesitamos nombre, record y medallas
            
            y_pos = datos_inicio_y + i * altura_fila
            x_actual = inicio_x_izq
            
            # Dibujar las 3 columnas para esta fila
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
                    # Limitar nombre a 10 caracteres (más espacio para emojis)
                    nombre_limitado = nombre
                    if len(nombre) > 10:
                        nombre_limitado = nombre[:10]
                    texto = f"{nombre_limitado} {medallas}"
                elif tipo_columna == "record":
                    texto = f"{record} 🎫"  # Agregamos emoji de ticket
                
                # Dibujar texto
                dibujar_texto(pantalla, fuente, texto, x_actual, y_pos, color_columna)
                
                # Mover a la siguiente columna
                x_actual += ancho_columna
    else:
        # Mensaje si no hay datos
        dibujar_texto_centrado(pantalla, fuente, "Sin datos", 
                              centro_izq, datos_inicio_y, (150, 150, 150))
    
    # === DIBUJAR COLUMNA DERECHA (TOTAL) ===
    # Calcular ancho total columna derecha (para centrar título)
    ancho_total_der = 0
    for config in config_columnas_total:
        ancho_total_der += config[0]
    centro_der = inicio_x_der + (ancho_total_der // 2)
    
    # Título columna derecha
    dibujar_texto_centrado(pantalla, fuente, "TOTAL ACUMULADO", 
                          centro_der, titulo_y, (255, 200, 100))
    
    # Dibujar datos de TOTAL
    cantidad_total = len(datos_total)
    
    if cantidad_total > 0:
        for i in range(cantidad_total):
            usuario_data = datos_total[i]
            nombre = usuario_data[0]
            total = usuario_data[1]
            medallas = usuario_data[4]  # Solo necesitamos nombre, total y medallas
            
            y_pos = datos_inicio_y + i * altura_fila
            x_actual = inicio_x_der
            
            # Dibujar las 3 columnas para esta fila
            for j in range(len(config_columnas_total)):
                config = config_columnas_total[j]
                ancho_columna = config[0]
                color_columna = config[1]
                tipo_columna = config[2]
                
                # Generar texto según el tipo de columna
                texto = ""
                if tipo_columna == "numero":
                    texto = f"{i+1}."
                elif tipo_columna == "nombre":
                    # Limitar nombre a 10 caracteres
                    nombre_limitado = nombre
                    if len(nombre) > 10:
                        nombre_limitado = nombre[:10]
                    texto = f"{nombre_limitado} {medallas}"
                elif tipo_columna == "total":
                    texto = f"{total} 🎫"  # Agregamos emoji de ticket
                
                # Dibujar texto
                dibujar_texto(pantalla, fuente, texto, x_actual, y_pos, color_columna)
                
                # Mover a la siguiente columna
                x_actual += ancho_columna
    else:
        # Mensaje si no hay datos
        dibujar_texto_centrado(pantalla, fuente, "Sin datos", 
                              centro_der, datos_inicio_y, (150, 150, 150))
    
    # === MENSAJES FINALES ===
    # Mensaje si no hay usuarios en absoluto
    if cantidad_record == 0 and cantidad_total == 0:
        dibujar_texto_centrado(pantalla, fuente, "¡Aún no hay jugadores con partidas!", 
                              500, datos_inicio_y + 150, (255, 100, 100))
    
    # Instrucciones
    dibujar_texto_centrado(pantalla, fuente, "Juega más partidas para subir en el ranking!",
                          500, 550, (200, 200, 200))