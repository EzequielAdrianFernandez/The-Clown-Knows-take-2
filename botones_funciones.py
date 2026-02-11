import pygame

def _calcular_color_hover(color_normal):
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

def procesar_botones(pantalla, fuente, eventos, diccionario_botones):
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
                # Si se presiona el botón SOBRE este botón
                if rect.collidepoint(evento.pos):
                    mouse_presionado_aqui = True
            
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                # Si se suelta el botón SOBRE este botón Y se había presionado aquí
                if rect.collidepoint(evento.pos) and mouse_presionado_aqui:
                    fue_presionado = True
                    mouse_presionado_aqui = False  # Resetear
        
        # Actualizar estado
        botones_actualizados[boton_id]['mouse_presionado_aqui'] = mouse_presionado_aqui
        
        # Determinar color actual
        color_actual = (_calcular_color_hover(boton_data['color_normal']) if tiene_colision else boton_data['color_normal'])
        
        # Actualizar estado del botón
        botones_actualizados[boton_id]['rect'] = rect
        botones_actualizados[boton_id]['color_actual'] = color_actual
        botones_actualizados[boton_id]['presionado'] = fue_presionado  # Solo True si fue_presionado
    
    return botones_actualizados

def dibujar_botones(pantalla, fuente, diccionario_botones):
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
        
        # Safety check para color
        color_a_dibujar = boton_data.get('color_actual', boton_data.get('color_normal', (100, 100, 100)))###################################################################MARCADOR DE GET
        
        # Dibujar botón
        pygame.draw.rect(pantalla, color_a_dibujar, boton_data['rect'], border_radius=8)
        pygame.draw.rect(pantalla, (255, 255, 255), boton_data['rect'], 2, border_radius=8)
        
        texto_surface = fuente.render(boton_data['texto'], True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(center=boton_data['rect'].center)
        pantalla.blit(texto_surface, texto_rect)
