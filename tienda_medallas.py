"""
tienda_medallas.py
Módulo para manejar la tienda de medallas del juego
"""

import json
from logica_juego import guardar_json

# Catálogo de medallas disponibles para compra
MEDALLAS_TIENDA = {
    "🏆": {"nombre": "Trofeo Dorado", "precio": 200, "descripcion": "Trofeo de campeón"},
    "👑": {"nombre": "Corona Real", "precio": 150, "descripcion": "Corona de rey/reina"},
    "💰": {"nombre": "Bolsa de Dinero", "precio": 100, "descripcion": "Eres rico en tickets"},
    "⚡": {"nombre": "Rayo Veloz", "precio": 80, "descripcion": "Jugador rápido"},
    "🌟": {"nombre": "Estrella Brillante", "precio": 50, "descripcion": "Destacado jugador"},
    "🎮": {"nombre": "Control de Juego", "precio": 30, "descripcion": "Jugador experimentado"},
    "💡": {"nombre": "Bombilla Idea", "precio": 70, "descripcion": "Muy inteligente"},
    "🧠": {"nombre": "Cerebro", "precio": 90, "descripcion": "Estratega maestro"},
    "🍕": {"nombre": "Pizza", "precio": 40, "descripcion": "Jugador divertido"},
    "❤️": {"nombre": "Corazón", "precio": 60, "descripcion": "Jugador favorito"},
    "🛡️": {"nombre": "Escudo", "precio": 120, "descripcion": "Defensor invencible"},
    "🎯": {"nombre": "Diana", "precio": 110, "descripcion": "Precisión perfecta"},
    "🚀": {"nombre": "Cohete", "precio": 130, "descripcion": "Ascenso rápido"},
    "🏅": {"nombre": "Medalla Deportiva", "precio": 75, "descripcion": "Atleta del juego"},
    "🎨": {"nombre": "Paleta de Arte", "precio": 55, "descripcion": "Creativo jugador"}
}

def obtener_medallas_disponibles(medallas_actuales):
    """
    Retorna las medallas que el usuario NO tiene aún.
    
    Args:
        medallas_actuales (str): String con las medallas actuales del usuario
    
    Returns:
        list: Lista de tuplas (emoji, datos) de medallas disponibles
    """
    disponibles = []
    for emoji, datos in MEDALLAS_TIENDA.items():
        if emoji not in medallas_actuales:
            disponibles.append((emoji, datos))
    return disponibles

def obtener_medallas_compradas(medallas_actuales):
    """
    Retorna las medallas que el usuario YA tiene.
    
    Args:
        medallas_actuales (str): String con las medallas actuales del usuario
    
    Returns:
        list: Lista de tuplas (emoji, datos) de medallas compradas
    """
    compradas = []
    for emoji, datos in MEDALLAS_TIENDA.items():
        if emoji in medallas_actuales:
            compradas.append((emoji, datos))
    return compradas

def comprar_medalla(usuarios, usuario_id, emoji_medalla):
    """
    Permite a un usuario comprar una medalla.
    
    Args:
        usuarios (dict): Diccionario de todos los usuarios
        usuario_id (str): ID del usuario (ej: 'usuario_1')
        emoji_medalla (str): Emoji de la medalla a comprar
    
    Returns:
        tuple: (éxito, mensaje, tickets_restantes)
    """
    if usuario_id not in usuarios:
        return False, "Usuario no encontrado", 0
    
    usuario = usuarios[usuario_id]
    
    # Verificar si la medalla existe en la tienda
    if emoji_medalla not in MEDALLAS_TIENDA:
        return False, "Medalla no disponible en la tienda", usuario["total_boletos"]
    
    # Verificar si ya tiene la medalla
    if emoji_medalla in usuario["medallas"]:
        return False, "Ya tienes esta medalla", usuario["total_boletos"]
    
    # Verificar precio
    precio = MEDALLAS_TIENDA[emoji_medalla]["precio"]
    tickets_actuales = usuario["total_boletos"]
    
    if tickets_actuales < precio:
        mensaje = f"Necesitas {precio} tickets (tienes {tickets_actuales})"
        return False, mensaje, tickets_actuales
    
    # Realizar compra
    usuario["total_boletos"] -= precio
    usuario["medallas"] += emoji_medalla
    
    # Guardar cambios
    guardar_json("z_usuarios.json", usuarios)
    
    tickets_restantes = usuario["total_boletos"]
    nombre_medalla = MEDALLAS_TIENDA[emoji_medalla]["nombre"]
    mensaje = f"¡Comprada {nombre_medalla} por {precio} tickets!"
    
    return True, mensaje, tickets_restantes

def puede_comprar_medalla(usuario, emoji_medalla):
    """
    Verifica si un usuario puede comprar una medalla.
    
    Args:
        usuario (dict): Datos del usuario
        emoji_medalla (str): Emoji de la medalla
    
    Returns:
        tuple: (puede_comprar, mensaje_error)
    """
    if emoji_medalla not in MEDALLAS_TIENDA:
        return False, "Medalla no disponible"
    
    if emoji_medalla in usuario["medallas"]:
        return False, "Ya tienes esta medalla"
    
    precio = MEDALLAS_TIENDA[emoji_medalla]["precio"]
    if usuario["total_boletos"] < precio:
        return False, f"Faltan {precio - usuario['total_boletos']} tickets"
    
    return True, ""

def crear_botones_tienda(usuario, x_inicio=150, y_inicio=280, ancho=180, alto=100, columnas=4, espacio=20):
    """
    Crea diccionario de botones para la tienda basado en medallas disponibles.
    
    Args:
        usuario (dict): Datos del usuario
        x_inicio (int): Posición X inicial
        y_inicio (int): Posición Y inicial
        ancho (int): Ancho de cada botón
        alto (int): Alto de cada botón
        columnas (int): Número de columnas
        espacio (int): Espacio entre botones
    
    Returns:
        dict: Diccionario de botones para la tienda
    """
    from menu_definiciones import MENU_TIENDA
    
    botones_tienda = MENU_TIENDA.copy()
    disponibles = obtener_medallas_disponibles(usuario["medallas"])
    
    for i, (emoji, datos) in enumerate(disponibles):
        fila = i // columnas
        columna = i % columnas
        
        x = x_inicio + columna * (ancho + espacio)
        y = y_inicio + fila * (alto + espacio)
        
        boton_id = f'boton_medalla_{emoji}'
        
        # Verificar si puede comprar
        puede_comprar, mensaje = puede_comprar_medalla(usuario, emoji)
        color = (100, 200, 100) if puede_comprar else (180, 70, 70)
        
        botones_tienda[boton_id] = {
            'x': x,
            'y': y,
            'ancho': ancho,
            'alto': alto,
            'texto': f"{emoji}\n{datos['nombre']}\n{datos['precio']} tickets",
            'color_normal': color,
            'presionado': False,
            'tooltip': mensaje if not puede_comprar else "Haz clic para comprar"
        }
    
    return botones_tienda

def obtener_resumen_tienda(usuario):
    """
    Obtiene un resumen de la situación de la tienda para un usuario.
    
    Args:
        usuario (dict): Datos del usuario
    
    Returns:
        dict: Resumen con tickets, medallas compradas, disponibles, etc.
    """
    disponibles = obtener_medallas_disponibles(usuario["medallas"])
    compradas = obtener_medallas_compradas(usuario["medallas"])
    
    return {
        'tickets': usuario["total_boletos"],
        'medallas_actuales': usuario["medallas"],
        'total_medallas': len(MEDALLAS_TIENDA),
        'medallas_compradas': len(compradas),
        'medallas_disponibles': len(disponibles),
        'gasto_total': sum(MEDALLAS_TIENDA[emoji]["precio"] for emoji in compradas)
    }

def obtener_resumen_tienda(usuario):
    """
    Obtiene un resumen de la situación de la tienda para el usuario.
    Versión optimizada que trabaja directamente con strings.
    
    Args:
        usuario (dict): Datos del usuario
    
    Returns:
        dict: Información resumida de la tienda
    """
    medallas_usuario = usuario["medallas"]
    tickets_usuario = usuario["total_boletos"]
    
    # Contadores inicializados
    medallas_compradas = 0
    total_medallas = len(MEDALLAS_TIENDA)
    puede_comprar_algunas = False
    tickets_necesarios_minimos = float('inf')
    
    # Recorrer todas las medallas disponibles en la tienda
    for emoji_medalla in MEDALLAS_TIENDA:
        # Verificar si el usuario ya tiene esta medalla
        tiene_medalla = False
        # Buscar el emoji en la string de medallas del usuario
        for i in range(len(medallas_usuario)):
            if medallas_usuario[i] == emoji_medalla:
                tiene_medalla = True
                medallas_compradas += 1
                break
        
        # Si no tiene la medalla, verificar si puede comprarla
        if not tiene_medalla:
            precio_medalla = MEDALLAS_TIENDA[emoji_medalla]["precio"]
            if tickets_usuario >= precio_medalla:
                puede_comprar_algunas = True
            if precio_medalla < tickets_necesarios_minimos:
                tickets_necesarios_minimos = precio_medalla
    
    # Calcular porcentaje
    porcentaje_completado = 0.0
    if total_medallas > 0:
        porcentaje_completado = (medallas_compradas / total_medallas) * 100
    
    # Medallas disponibles
    medallas_disponibles = total_medallas - medallas_compradas
    
    # Determinar mensaje de estado
    estado_tienda = "disponibles"
    if medallas_disponibles == 0:
        estado_tienda = "completada"
    elif not puede_comprar_algunas and tickets_usuario < tickets_necesarios_minimos:
        estado_tienda = f"necesitas {tickets_necesarios_minimos - tickets_usuario} tickets más"
    
    return {
        "tickets_disponibles": tickets_usuario,
        "medallas_compradas": medallas_compradas,
        "medallas_disponibles": medallas_disponibles,
        "total_medallas": total_medallas,
        "porcentaje_completado": porcentaje_completado,
        "puede_comprar_algunas": puede_comprar_algunas,
        "estado_tienda": estado_tienda,
        "tickets_necesarios_minimos": tickets_necesarios_minimos if tickets_necesarios_minimos != float('inf') else 0
    }
