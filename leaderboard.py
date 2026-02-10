

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