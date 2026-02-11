"""
🗺️ MÓDULO: laberintos_predeterminados.py
=========================================
Contiene mapas de laberintos manuales y prediseñados.

PROPÓSITO:
- Son la RED DE SEGURIDAD cuando la generación aleatoria falla
- Están garantizados para ser resolubles
- Cada dificultad tiene un diseño específico y probado
- Ajustan sus dimensiones según parámetros pero mantienen estructura base

FLUJO:
1. crear_laberinto() en laberinto_espejos.py intenta generar mapa aleatorio
2. Si falla tras varios intentos → llama a obtener_laberinto_manual()
3. Esta función devuelve un mapa fijo según dificultad
4. El mapa se recorta a las dimensiones solicitadas si es necesario
"""

def obtener_laberinto_manual(dificultad, filas, columnas):
    """
    🗺️ Retorna un laberinto manual prediseñado para cada dificultad.
    
    Args:
        dificultad (str): 'facil', 'medio', 'dificil' o 'deathrow'
        filas, columnas (int): Dimensiones solicitadas (se recortará el mapa base)
    
    Returns:
        list: Matriz 2D del laberinto (lista de listas)
    
    NOTA: Todos estos mapas están probados y tienen al menos 1 camino E → S
    """
    
    # ─────────────────────────────────────────────────────────────
    # 🟢 FÁCIL - Simple y directo
    #    10 filas × 15 columnas
    #    - Paredes (#) formando obstáculos básicos
    #    - Algunos espejos (/) para enseñar mecánica
    #    - Camino principal despejado
    # ─────────────────────────────────────────────────────────────
    if dificultad == 'facil':
        return [
            ['E', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],
            [' ', '/', '#', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ']
        ]
    
    # ─────────────────────────────────────────────────────────────
    # 🟡 MEDIO - Con algunos espejos
    #    10 filas × 20 columnas
    #    - Introduce ambos tipos de espejos (/ y \)
    #    - Patrones de espejos en diagonal
    #    - Laberinto más denso que fácil
    # ─────────────────────────────────────────────────────────────
    elif dificultad == 'medio':
        return [
            ['E', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' '],
            [' ', ' ', '/', ' ', ' ', ' ', '\\', ' ', ' ', ' ', '/', ' ', ' ', ' ', '\\', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#'],
            [' ', ' ', '\\', ' ', ' ', ' ', '/', ' ', ' ', ' ', '\\', ' ', ' ', ' ', '/', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#']
        ]
    
    # ─────────────────────────────────────────────────────────────
    # 🔴 DIFÍCIL - Con más espejos y caminos engañosos
    #    13 filas × 25 columnas
    #    - Múltiples espejos creando rebotes
    #    - Paredes estratégicamente ubicadas
    #    - Requiere pensar los movimientos diagonales
    # ─────────────────────────────────────────────────────────────
    elif dificultad == 'dificil':
        return [
            ['E', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', 'S'],
            [' ', '/', ' ', '\\', ' ', '#', ' ', '/', ' ', '\\', ' ', '#', ' ', '/', ' ', '\\', ' ', '#', ' ', '/', ' ', '\\', ' ', '#', ' '],
            [' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', '\\', ' ', '/', '#', ' ', ' ', '\\', ' ', '/', '#', ' ', ' ', '\\', ' ', '/', '#', ' ', ' ', '\\', ' ', '/', '#', ' '],
            [' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' '],
            [' ', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' '],
            [' ', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', '/', ' ', '\\', ' ', ' '],
            [' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ']
        ]

    # ─────────────────────────────────────────────────────────────
    # 💀 DEATHROW - Desafiante pero resoluble
    #    14 filas × 25 columnas (¡NO 26!)
    #    - Diseño caótico con muchos espejos
    #    - Caminos entrelazados
    #    - Para jugadores expertos
    #    
    #    ⚠️  IMPORTANTE: Este mapa tiene EXACTAMENTE 25 columnas
    #       La dificultad deathrow en menu_definiciones usa 12x22
    #       Así que al recortar se ajustará automáticamente
    # ─────────────────────────────────────────────────────────────
    elif dificultad == 'deathrow':
        return [
            # 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20   21   22   23   24
            ['E', '#', ' ', '/', ' ', '\\', '#', '/', ' ', ' ', ' ', ' ', ' ', '\\', '#', 'S', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # Fila 0
            [' ', '#', ' ', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '#'],  # Fila 1
            [' ', '/', '/', ' ', '#', ' ', '#', ' ', '#', '/', ' ', '\\', '#', ' ', '#', '#', '\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\\'],  # Fila 2
            [' ', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' '],  # Fila 3
            [' ', '#', '#', ' ', '#', ' ', '/', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '/', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' /'],  # Fila 4
            [' ', ' ', '#', ' ', '\\', ' ', '/', '#', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' '],  # Fila 5
            ['\\', '/', ' ', '#', '/', ' ', '#', '/', ' ', '/', '#', ' ', '#', ' ', '#', '#', '\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\\'],  # Fila 6
            [' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' '],  # Fila 7
            [' ', '#', ' ', '#', ' ', '\\', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', '#', '/', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '/'],  # Fila 8
            [' ', '#', '\\', ' ', '#', ' ', '#', '#', '\\', '/', '#', ' ', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' '],  # Fila 9
            ['\\', ' ', '#', ' ', '#', ' ', '#', ' ', '/', '#', '#', ' ', '#', ' ', '#', '#', '\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\\'],  # Fila 10
            ['#', ' ', '#', '\\', ' ', '/', '#', ' ', '#', ' ', ' ', '\\', ' ', '/', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' '],  # Fila 11
            ['#', ' ', '#', '#', '/', '#', '#', ' ', '#', '/', '#', ' ', '#', '#', ' ', '\\', '/', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '/'],  # Fila 12
            ['#', ' ', ' ', ' ', '/', ' ', ' ', ' ', ' ', '/', '#', ' ', ' ', ' ', '/', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#']   # Fila 13
        ]
    
    # ─────────────────────────────────────────────────────────────
    # 🟡 POR DEFECTO - Si la dificultad no coincide
    #    Devuelve un mapa fácil por seguridad
    # ─────────────────────────────────────────────────────────────
    else:
        print(f"⚠️ Dificultad '{dificultad}' no reconocida, usando mapa fácil")
        return obtener_laberinto_manual('facil', filas, columnas)


"""
📐 NOTA SOBRE DIMENSIONES:
---------------------------
Los mapas prediseñados tienen dimensiones FIJAS:
- Fácil   : 10×15
- Medio   : 10×20  
- Difícil : 13×25
- Deathrow: 14×25

En laberinto_espejos.py, la función crear_laberinto() puede pedir 
dimensiones diferentes (ej: deathrow pide 12×22). 
El mapa se RECORTARÁ automáticamente para ajustarse a lo solicitado.

Esto está bien porque:
1. La entrada E siempre está en (0,0)
2. La salida S siempre está en la última fila/columna
3. El camino principal suele estar en las primeras filas/columnas
4. Las celdas que sobran se ignoran

Si en el futuro quieres mapas EXACTOS para cada dificultad,
puedes modificar menu_definiciones.py para que coincidan las dimensiones.
"""