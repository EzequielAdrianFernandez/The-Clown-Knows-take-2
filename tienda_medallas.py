"""
🏪 MÓDULO: tienda_medallas.py
==============================
SISTEMA DE TIENDA Y MEDALLAS DEL JUEGO.

¿QUÉ HACE ESTE MÓDULO?
----------------------------------------------------------------------------
1. 🎁 CATÁLOGO DE MEDALLAS → 15 medallas con emoji, nombre, precio y descripción
2. 💰 COMPRA DE MEDALLAS   → Verifica tickets, resta precio, agrega emoji al usuario
3. 📊 GESTIÓN DE INVENTARIO → Qué medallas tiene/cómo comprar/estado de la tienda
4. 🔍 VALIDACIONES        → Verifica si puede comprar, si ya la tiene, si existe

ESTRUCTURA DE DATOS:
----------------------------------------------------------------------------
MEDALLAS_TIENDA = {
    "🏆": {
        "nombre": "Trofeo Dorado",
        "precio": 200,
        "descripcion": "Trofeo de campeón"
    },
    ... (15 medallas)
}

FLUJO DE COMPRA (desde manejador_estados.py):
----------------------------------------------------------------------------
1. crear_botones_tienda_dinamicos() → Genera botones según medallas disponibles
2. usuario hace clic en botón con emoji
3. comprar_medalla() → Valida, resta tickets, agrega medalla, guarda JSON
4. Se actualiza la tienda (botones desaparecen si ya no hay tickets/medallas)
"""

import json
from logica_juego import guardar_json


# ============================================================================
# 🎁 CATÁLOGO DE MEDALLAS (FUENTE ÚNICA DE VERDAD)
# ============================================================================

MEDALLAS_TIENDA = {
    # 🏆 Trofeos y reconocimientos (más caros)
    "🏆": {
        "nombre": "Trofeo Dorado",
        "precio": 200,
        "descripcion": "Trofeo de campeón"
    },
    "👑": {
        "nombre": "Corona Real",
        "precio": 150,
        "descripcion": "Corona de rey/reina"
    },
    "💰": {
        "nombre": "Bolsa de Dinero",
        "precio": 100,
        "descripcion": "Eres rico en tickets"
    },
    
    # 🎮 Habilidades y logros (precio medio)
    "⚡": {
        "nombre": "Rayo Veloz",
        "precio": 80,
        "descripcion": "Jugador rápido"
    },
    "🌟": {
        "nombre": "Estrella Brillante",
        "precio": 50,
        "descripcion": "Destacado jugador"
    },
    "🎮": {
        "nombre": "Control de Juego",
        "precio": 30,
        "descripcion": "Jugador experimentado"
    },
    "💡": {
        "nombre": "Bombilla Idea",
        "precio": 70,
        "descripcion": "Muy inteligente"
    },
    "🧠": {
        "nombre": "Cerebro",
        "precio": 90,
        "descripcion": "Estratega maestro"
    },
    
    # 🍕 Divertidas y sociales (precio accesible)
    "🍕": {
        "nombre": "Pizza",
        "precio": 40,
        "descripcion": "Jugador divertido"
    },
    "❤️": {
        "nombre": "Corazón",
        "precio": 60,
        "descripcion": "Jugador favorito"
    },
    
    # 🛡️ Combate y precisión
    "🛡️": {
        "nombre": "Escudo",
        "precio": 120,
        "descripcion": "Defensor invencible"
    },
    "🎯": {
        "nombre": "Diana",
        "precio": 110,
        "descripcion": "Precisión perfecta"
    },
    "🚀": {
        "nombre": "Cohete",
        "precio": 130,
        "descripcion": "Ascenso rápido"
    },
    
    # 🏅 Creatividad y deporte
    "🏅": {
        "nombre": "Medalla Deportiva",
        "precio": 75,
        "descripcion": "Atleta del juego"
    },
    "🎨": {
        "nombre": "Paleta de Arte",
        "precio": 55,
        "descripcion": "Creativo jugador"
    }
}


# ============================================================================
# 📊 GESTIÓN DE INVENTARIO DE MEDALLAS
# ============================================================================

def obtener_medallas_disponibles(medallas_actuales):
    """
    🔍 Retorna las medallas que el usuario NO tiene aún.
    
    Itera sobre TODAS las medallas del catálogo y verifica si el emoji
    está presente en el string de medallas del usuario.
    
    Args:
        medallas_actuales (str): String con las medallas actuales del usuario
                                 Ej: "🎮🏆👑💰⚡"
    
    Returns:
        list: Lista de tuplas (emoji, datos) de medallas disponibles para comprar
              Ej: [ ("🌟", {...}), ("🍕", {...}), ... ]
    """
    disponibles = []
    for emoji, datos in MEDALLAS_TIENDA.items():
        # Verificar si el emoji NO está en el string
        emoji_encontrado = False
        for caracter in medallas_actuales:
            if caracter == emoji:
                emoji_encontrado = True
                break
        
        if not emoji_encontrado:
            disponibles.append((emoji, datos))
    
    return disponibles


def obtener_medallas_compradas(medallas_actuales):
    """
    🔍 Retorna las medallas que el usuario YA tiene.
    
    Args:
        medallas_actuales (str): String con las medallas actuales del usuario
    
    Returns:
        list: Lista de tuplas (emoji, datos) de medallas ya compradas
    """
    compradas = []
    for emoji, datos in MEDALLAS_TIENDA.items():
        # Verificar si el emoji SÍ está en el string
        emoji_encontrado = False
        for caracter in medallas_actuales:
            if caracter == emoji:
                emoji_encontrado = True
                break
        
        if emoji_encontrado:
            compradas.append((emoji, datos))
    
    return compradas


# ============================================================================
# 💰 LÓGICA DE COMPRA
# ============================================================================

def comprar_medalla(usuarios, usuario_id, emoji_medalla):
    """
    💰 Procesa la compra de una medalla.
    
    FLUJO:
    1. Validar que usuario existe
    2. Validar que medalla existe en catálogo
    3. Validar que NO la tiene ya
    4. Validar que tiene suficientes tickets
    5. Restar precio y agregar emoji
    6. Guardar en JSON
    7. Retornar resultado
    
    Args:
        usuarios (dict): Diccionario de todos los usuarios
        usuario_id (str): ID del usuario (ej: 'usuario_1')
        emoji_medalla (str): Emoji de la medalla a comprar (ej: "🏆")
    
    Returns:
        tuple: (éxito, mensaje, tickets_restantes)
               éxito (bool): True si se compró, False si no
               mensaje (str): Descripción del resultado
               tickets_restantes (int): Tickets que le quedan al usuario
    """
    # ── 1. Validar usuario ─────────────────────────────────────
    if usuario_id not in usuarios:
        return False, "❌ Usuario no encontrado", 0
    
    usuario = usuarios[usuario_id]
    
    # ── 2. Validar medalla ─────────────────────────────────────
    if emoji_medalla not in MEDALLAS_TIENDA:
        return False, "❌ Medalla no disponible en la tienda", usuario["total_boletos"]
    
    # ── 3. Validar que no la tenga ya ──────────────────────────
    medalla_ya_tiene = False
    for caracter in usuario["medallas"]:
        if caracter == emoji_medalla:
            medalla_ya_tiene = True
            break
    
    if medalla_ya_tiene:
        return False, "❌ Ya tienes esta medalla", usuario["total_boletos"]
    
    # ── 4. Validar precio ──────────────────────────────────────
    precio = MEDALLAS_TIENDA[emoji_medalla]["precio"]
    tickets_actuales = usuario["total_boletos"]
    
    if tickets_actuales < precio:
        mensaje = f"❌ Necesitas {precio} tickets (tienes {tickets_actuales})"
        return False, mensaje, tickets_actuales
    
    # ── 5. Realizar compra ────────────────────────────────────
    usuario["total_boletos"] -= precio
    usuario["medallas"] += emoji_medalla
    
    # ── 6. Guardar cambios ────────────────────────────────────
    guardar_json("z_usuarios.json", usuarios)
    
    tickets_restantes = usuario["total_boletos"]
    nombre_medalla = MEDALLAS_TIENDA[emoji_medalla]["nombre"]
    mensaje = f"✅ ¡Comprada {nombre_medalla} por {precio} tickets!"
    
    return True, mensaje, tickets_restantes


def puede_comprar_medalla(usuario, emoji_medalla):
    """
    🔍 Verifica si un usuario puede comprar una medalla específica.
    
    Args:
        usuario (dict): Datos del usuario
        emoji_medalla (str): Emoji de la medalla
    
    Returns:
        tuple: (puede_comprar, mensaje_error)
               puede_comprar (bool): True si puede, False si no
               mensaje_error (str): Vacío si puede, descripción si no
    """
    # ── 1. Existe la medalla? ─────────────────────────────────
    if emoji_medalla not in MEDALLAS_TIENDA:
        return False, "Medalla no disponible"
    
    # ── 2. Ya la tiene? ───────────────────────────────────────
    for caracter in usuario["medallas"]:
        if caracter == emoji_medalla:
            return False, "Ya tienes esta medalla"
    
    # ── 3. Tiene suficientes tickets? ─────────────────────────
    precio = MEDALLAS_TIENDA[emoji_medalla]["precio"]
    if usuario["total_boletos"] < precio:
        faltan = precio - usuario["total_boletos"]
        return False, f"Faltan {faltan} tickets"
    
    return True, ""


# ============================================================================
# 🖌️ GENERACIÓN DE BOTONES (PARA manejador_estados.py)
# ============================================================================

def crear_botones_tienda(usuario, x_inicio=150, y_inicio=280, ancho=180, alto=100, columnas=4, espacio=20):
    """
    🖌️ Crea diccionario de botones para la tienda basado en medallas disponibles.
    
    NOTA: Esta función NO se usa actualmente.
    En su lugar, manejador_estados.py usa crear_botones_tienda_dinamicos()
    que es una versión MINIMALISTA (solo emoji + precio).
    
    Args:
        usuario (dict): Datos del usuario
        x_inicio (int): Posición X inicial
        y_inicio (int): Posición Y inicial
        ancho (int): Ancho de cada botón
        alto (int): Alto de cada botón
        columnas (int): Número de columnas (grid)
        espacio (int): Espacio entre botones
    
    Returns:
        dict: Diccionario de botones para la tienda (base MENU_TIENDA + botones dinámicos)
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
            'tooltip': mensaje if not puede_comprar else "Haz clic para comprar",
            'emoji': emoji  # Metadato para identificación
        }
    
    return botones_tienda


# ============================================================================
# 📊 RESUMEN DE TIENDA (VERSIÓN COMPLETA - NO USADA)
# ============================================================================

def obtener_resumen_tienda(usuario):
    """
    📊 Obtiene un resumen de la situación de la tienda para un usuario.
    
    VERSIÓN COMPLETA (listas) - NO USADA ACTUALMENTE.
    Ver versión optimizada abajo.
    
    Args:
        usuario (dict): Datos del usuario
    
    Returns:
        dict: Resumen con tickets, medallas compradas, disponibles, etc.
    """
    disponibles = obtener_medallas_disponibles(usuario["medallas"])
    compradas = obtener_medallas_compradas(usuario["medallas"])
    
    # Calcular gasto total
    gasto_total = 0
    for emoji, _ in compradas:
        gasto_total += MEDALLAS_TIENDA[emoji]["precio"]
    
    return {
        'tickets': usuario["total_boletos"],
        'medallas_actuales': usuario["medallas"],
        'total_medallas': len(MEDALLAS_TIENDA),
        'medallas_compradas': len(compradas),
        'medallas_disponibles': len(disponibles),
        'gasto_total': gasto_total
    }


# ============================================================================
# 📊 RESUMEN DE TIENDA (VERSIÓN OPTIMIZADA - EN USO)
# ============================================================================

def obtener_resumen_tienda_optimizado(usuario):
    """
    📊 Obtiene un resumen de la tienda SIN crear listas intermedias.
    
    Versión eficiente que trabaja directamente con strings.
    Ideal para mostrar información rápida en la interfaz.
    
    Args:
        usuario (dict): Datos del usuario
    
    Returns:
        dict: Información resumida de la tienda con:
            - tickets_disponibles: Tickets actuales
            - medallas_compradas: Cantidad de medallas que ya tiene
            - medallas_disponibles: Cantidad que le faltan
            - total_medallas: Total en el catálogo (15)
            - porcentaje_completado: % de colección
            - puede_comprar_algunas: Si tiene al menos 1 medalla alcanzable
            - estado_tienda: "disponibles", "completada" o "necesitas X tickets"
            - tickets_necesarios_minimos: Precio de la medalla más barata disponible
    """
    medallas_usuario = usuario["medallas"]
    tickets_usuario = usuario["total_boletos"]
    
    # Inicializar contadores
    medallas_compradas = 0
    total_medallas = len(MEDALLAS_TIENDA)
    puede_comprar_algunas = False
    tickets_necesarios_minimos = float('inf')
    
    # Recorrer todas las medallas del catálogo UNA SOLA VEZ
    for emoji_medalla in MEDALLAS_TIENDA:
        # Verificar si el usuario YA TIENE esta medalla
        tiene_medalla = False
        for i in range(len(medallas_usuario)):
            if medallas_usuario[i] == emoji_medalla:
                tiene_medalla = True
                medallas_compradas += 1
                break
        
        # Si NO la tiene, verificar si PUEDE COMPRARLA
        if not tiene_medalla:
            precio_medalla = MEDALLAS_TIENDA[emoji_medalla]["precio"]
            if tickets_usuario >= precio_medalla:
                puede_comprar_algunas = True
            if precio_medalla < tickets_necesarios_minimos:
                tickets_necesarios_minimos = precio_medalla
    
    # Calcular porcentaje de colección completada
    porcentaje_completado = 0.0
    if total_medallas > 0:
        porcentaje_completado = (medallas_compradas / total_medallas) * 100
    
    # Medallas disponibles (las que le faltan)
    medallas_disponibles = total_medallas - medallas_compradas
    
    # Determinar estado textual de la tienda para este usuario
    estado_tienda = "disponibles"
    if medallas_disponibles == 0:
        estado_tienda = "completada"
    elif not puede_comprar_algunas and tickets_usuario < tickets_necesarios_minimos:
        tickets_faltantes = tickets_necesarios_minimos - tickets_usuario
        estado_tienda = f"necesitas {tickets_faltantes} tickets más"
    
    # Si no hay medallas disponibles (infinito), poner 0
    if tickets_necesarios_minimos == float('inf'):
        tickets_necesarios_minimos = 0
    
    return {
        "tickets_disponibles": tickets_usuario,
        "medallas_compradas": medallas_compradas,
        "medallas_disponibles": medallas_disponibles,
        "total_medallas": total_medallas,
        "porcentaje_completado": porcentaje_completado,
        "puede_comprar_algunas": puede_comprar_algunas,
        "estado_tienda": estado_tienda,
        "tickets_necesarios_minimos": tickets_necesarios_minimos
    }

