import pygame

def _calcular_color_hover(color_normal):
    """
    🎨 Calcula un color más claro u oscuro para el efecto hover.
    
    Args:
        color_normal (tuple): Color RGB original del botón
    
    Returns:
        tuple: Color RGB modificado (más claro si es oscuro, más oscuro si es claro)
    """
    r, g, b = color_normal
    brillo = (0.299 * r + 0.587 * g + 0.114 * b)  # Fórmula de luminancia
    es_oscuro = brillo < 128
    factor = 1.4 if es_oscuro else 0.7  # Clarificar si es oscuro, oscurecer si es claro
    
    r_hover = min(255, int(r * factor)) if es_oscuro else max(0, int(r * factor))
    g_hover = min(255, int(g * factor)) if es_oscuro else max(0, int(g * factor))
    b_hover = min(255, int(b * factor)) if es_oscuro else max(0, int(b * factor))
    
    return (r_hover, g_hover, b_hover)

def _crear_rectangulo_boton(boton_data):
    """
    📐 Crea o recupera el rectángulo de colisión de un botón.
    
    Args:
        boton_data (dict): Datos del botón (x, y, ancho, alto)
    
    Returns:
        pygame.Rect: Rectángulo para detección de colisiones
    """
    rect_existe = 'rect' in boton_data and boton_data['rect'] is not None
    
    if not rect_existe:
        return pygame.Rect(
            boton_data['x'], 
            boton_data['y'], 
            boton_data['ancho'], 
            boton_data['alto']
        )
    return boton_data['rect']

def obtener_color_boton_actual(boton_data, tiene_colision):
    """
    🎨 Determina el color que debe tener el botón según si el mouse está encima.
    
    Args:
        boton_data (dict): Diccionario del botón (debe tener 'color_normal')
        tiene_colision (bool): True si el mouse está sobre el botón
    
    Returns:
        tuple: Color RGB a utilizar
    """
    color_base = boton_data['color_normal']
    color_hover = _calcular_color_hover(color_base)
    
    return color_hover if tiene_colision else color_base

# ============================================================================
# 🎮 FUNCIONES PRINCIPALES
# ============================================================================

def procesar_botones(pantalla,ventana,eventos, diccionario_botones):
    """
    🖱️ Procesa interacciones de botones y actualiza su estado.
    
    ¿Qué hace?
    - Detecta si el mouse está sobre cada botón (hover)
    - Detecta clicks completos (MOUSEBUTTONDOWN + MOUSEBUTTONUP sobre el mismo botón)
    - Actualiza color_actual según hover
    - Marca presionado = True solo cuando se completa un click
    
    Args:
        pantalla: Superficie de pygame (no se usa directamente, se pasa por consistencia)
        fuente: Fuente de pygame (no se usa, se pasa por consistencia)
        eventos: Lista de eventos del frame actual
        diccionario_botones: Diccionario con todos los botones del estado actual
    
    Returns:
        dict: Diccionario de botones actualizado (colores, rects, estado de click)
    """
    mouse_pos = pygame.mouse.get_pos()
    botones_actualizados = diccionario_botones.copy()
    claves_botones = list(botones_actualizados.keys())
    
    for i in range(len(claves_botones)):
        boton_id = claves_botones[i]
        boton_data = botones_actualizados[boton_id]
        
        rect = _crear_rectangulo_boton(boton_data)
        tiene_colision = rect.collidepoint(mouse_pos)
        
        # Inicializar estado de clic si no existe
        if 'mouse_presionado_aqui' not in boton_data:
            boton_data['mouse_presionado_aqui'] = False
        
        # Procesar eventos de mouse
        mouse_presionado_aqui = boton_data['mouse_presionado_aqui']
        fue_presionado = False
        
        for j in range(len(eventos)):
            evento = eventos[j]
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Click IZQUIERDO presionado SOBRE el botón
                if rect.collidepoint(evento.pos):
                    mouse_presionado_aqui = True
            
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                # Click IZQUIERDO SOLTADO SOBRE el botón y se había presionado aquí
                if rect.collidepoint(evento.pos) and mouse_presionado_aqui:
                    fue_presionado = True
                    mouse_presionado_aqui = False  # Resetear estado
        
        # Actualizar estado
        botones_actualizados[boton_id]['mouse_presionado_aqui'] = mouse_presionado_aqui
        
        # Determinar color actual (hover o normal)
        color_actual = (_calcular_color_hover(boton_data['color_normal']) 
                       if tiene_colision else boton_data['color_normal'])
        
        # Actualizar datos del botón
        botones_actualizados[boton_id]['rect'] = rect
        botones_actualizados[boton_id]['color_actual'] = color_actual
        botones_actualizados[boton_id]['presionado'] = fue_presionado  # Solo True si click completado
    
    return botones_actualizados

def dibujar_botones(pantalla, fuente, diccionario_botones):
    """
    🖼️ Dibuja todos los botones en pantalla.
    
    Características:
    - Usa color_actual si existe (calculado por procesar_botones)
    - Si no existe, lo calcula sobre la marcha (robusto para botones nuevos)
    - Bordes redondeados (radius=8)
    - Borde blanco de 2px
    - Texto centrado automáticamente
    
    Args:
        pantalla: Superficie de pygame donde dibujar
        fuente: Fuente para renderizar texto
        diccionario_botones: Diccionario con los botones a dibujar
    """
    claves_botones = list(diccionario_botones.keys())
    mouse_pos = pygame.mouse.get_pos()  # Para calcular hover en botones nuevos
    
    for i in range(len(claves_botones)):
        boton_id = claves_botones[i]
        boton_data = diccionario_botones[boton_id]
        
        # Crear rectángulo si no existe (por si acaso)
        if 'rect' not in boton_data:
            boton_data['rect'] = pygame.Rect(
                boton_data['x'], 
                boton_data['y'], 
                boton_data['ancho'], 
                boton_data['alto']
            )
        
        # --- DETERMINAR COLOR A DIBUJAR ---
        # Prioridad: 1) color_actual existente, 2) calcular nuevo
        if 'color_actual' in boton_data:
            color_a_dibujar = boton_data['color_actual']
        else:
            # Calcular color según hover (tolerante a botones sin procesar)
            tiene_colision = boton_data['rect'].collidepoint(mouse_pos)
            color_a_dibujar = obtener_color_boton_actual(boton_data, tiene_colision)
            # Guardar para futuros frames (optimización)
            boton_data['color_actual'] = color_a_dibujar
        # ------------------------------------
        
        # Dibujar cuerpo del botón (relleno)
        pygame.draw.rect(pantalla, color_a_dibujar, boton_data['rect'], border_radius=8)
        # Dibujar borde blanco
        pygame.draw.rect(pantalla, (255, 255, 255), boton_data['rect'], 2, border_radius=8)
        
        # Dibujar texto centrado
        texto_surface = fuente.render(boton_data['texto'], True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(center=boton_data['rect'].center)
        pantalla.blit(texto_surface, texto_rect)