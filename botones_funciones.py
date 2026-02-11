import pygame

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def _calcular_color_hover(color_normal):
    """Calcula el color cuando el mouse está sobre el botón"""
    r, g, b = color_normal
    brillo = (0.299 * r + 0.587 * g + 0.114 * b)
    es_oscuro = brillo < 128
    factor = 1.4 if es_oscuro else 0.7
    
    r_hover = min(255, int(r * factor)) if es_oscuro else max(0, int(r * factor))
    g_hover = min(255, int(g * factor)) if es_oscuro else max(0, int(g * factor))
    b_hover = min(255, int(b * factor)) if es_oscuro else max(0, int(b * factor))
    
    return (r_hover, g_hover, b_hover)


def _crear_rectangulo_boton(boton_data):
    """Crea el rectángulo para un botón si no existe"""
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
    Obtiene el color actual del botón basado en su estado.
    
    ✨ Sin try/except, break, 'in', múltiples return
    ✨ Supone que color_normal SIEMPRE existe
    
    Args:
        boton_data (dict): Datos del botón (con color_normal garantizado)
        tiene_colision (bool): Si el mouse está sobre el botón
    
    Returns:
        tuple: Color RGB (r, g, b)
    """
    color_base = boton_data['color_normal']
    color_hover = _calcular_color_hover(color_base)
    
    return color_hover if tiene_colision else color_base


# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def procesar_botones(pantalla, fuente, eventos, diccionario_botones):
    """Procesa interacciones de botones y actualiza su estado"""
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
                if rect.collidepoint(evento.pos):
                    mouse_presionado_aqui = True
            
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if rect.collidepoint(evento.pos) and mouse_presionado_aqui:
                    fue_presionado = True
                    mouse_presionado_aqui = False
        
        # Obtener color con nueva función
        color_actual = obtener_color_boton_actual(boton_data, tiene_colision)
        
        # Actualizar estado del botón
        botones_actualizados[boton_id]['mouse_presionado_aqui'] = mouse_presionado_aqui
        botones_actualizados[boton_id]['rect'] = rect
        botones_actualizados[boton_id]['color_actual'] = color_actual
        botones_actualizados[boton_id]['presionado'] = fue_presionado
    
    return botones_actualizados


def dibujar_botones(pantalla, fuente, diccionario_botones):
    """Dibuja todos los botones en pantalla"""
    claves_botones = list(diccionario_botones.keys())
    
    for i in range(len(claves_botones)):
        boton_id = claves_botones[i]
        boton_data = diccionario_botones[boton_id]
        
        # Crear rectángulo si no existe
        if 'rect' not in boton_data:
            boton_data['rect'] = pygame.Rect(
                boton_data['x'], 
                boton_data['y'], 
                boton_data['ancho'], 
                boton_data['alto']
            )
        
        # Color garantizado por procesar_botones()
        color_a_dibujar = boton_data['color_actual']
        
        # Dibujar botón
        pygame.draw.rect(pantalla, color_a_dibujar, boton_data['rect'], border_radius=8)
        pygame.draw.rect(pantalla, (255, 255, 255), boton_data['rect'], 2, border_radius=8)
        
        # Dibujar texto
        texto_surface = fuente.render(boton_data['texto'], True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(center=boton_data['rect'].center)
        pantalla.blit(texto_surface, texto_rect)

def inicializar_botones_laberinto(diccionario_botones):
        """
        Garantiza estructura completa de botones para el menú de resultado.
        Sin try/except, break, 'in', múltiples return
        """
        claves_botones = list(diccionario_botones.keys())
        
        for i in range(len(claves_botones)):
            boton_id = claves_botones[i]
            boton_data = diccionario_botones[boton_id]
            
            diccionario_botones[boton_id] = {
                **boton_data,
                'rect': boton_data.get('rect') or pygame.Rect(
                    boton_data['x'], boton_data['y'],
                    boton_data['ancho'], boton_data['alto']
                ),
                'color_actual': boton_data.get('color_actual', boton_data['color_normal']),
                'mouse_presionado_aqui': boton_data.get('mouse_presionado_aqui', False),
                'presionado': boton_data.get('presionado', False)
            }
        
        return diccionario_botones