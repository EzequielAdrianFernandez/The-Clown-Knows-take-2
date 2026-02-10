#menu_definiciones.py


# Definiciones de los fondos para cada estado del juego #
FONDOS = {
    "menu_principal": "imagenes/menu_principal.png",
    "seleccion_usuario": "imagenes/seleccion_usuario.png", 
    "crear_usuario": "imagenes/seleccion_usuario.png",
    "confirmar_creacion": "imagenes/seleccion_usuario.png",
    "juego_pregunta": "imagenes/juego_pregunta.png",
    "juego_resultado_ronda": "imagenes/juego_resultado_ronda.png",
    "juego_resultado_final": "imagenes/juego_resultado_final.png",
    "juego_pregunta_VoF": "imagenes/juego_pregunta.png",
    "juego_resultado_ronda_VoF": "imagenes/juego_resultado_ronda.png",
    "juego_resultado_final_VoF": "imagenes/juego_resultado_final.png",
    "opciones": "imagenes/opciones.png",
    "seleccion_dificultad_laberinto": "imagenes/seleccion_usuario.png",
    "laberinto_juego": "imagenes/juego_pregunta.png",
    "laberinto_resultado": "imagenes/juego_resultado_final.png",
    "tienda": "imagenes/tienda_medallas.png",
    "leaderboard": "imagenes/leaderboard.png"
}

# Definiciones de los menús del juego #
MENU_PRINCIPAL = {
    'boton_jugar': {'x': 205, 'y': 390-50, 'ancho': 210, 'alto': 50, 'texto': 'MULTIPLE CHOICE', 'color_normal': (70, 130, 180)},
    'boton_seleccion_usuario': {'x': 205, 'y': 460-50, 'ancho': 260, 'alto': 50, 'texto': 'SELECCIONAR USUARIO', 'color_normal': (70, 130, 180)},
    'boton_tienda': {'x': 205, 'y': 530-50, 'ancho': 280, 'alto': 50, 'texto': '🏪 TIENDA DE MEDALLAS', 'color_normal': (255, 215, 0)},
    'boton_jugar_VoF': {'x': 495, 'y': 390-50, 'ancho': 250, 'alto': 50, 'texto': 'VERDADERO O FALSO', 'color_normal': (100, 180, 100)},
    'boton_laberinto': {'x': 515, 'y': 460-50, 'ancho': 230, 'alto': 50, 'texto': 'LABERINTO ESPEJOS', 'color_normal': (180, 100, 180)}, 
    'boton_leaderboard': {'x': 530, 'y': 530-50, 'ancho': 210, 'alto': 50, 'texto': '🏆 LEADERBOARD', 'color_normal': (255, 215, 0)},
    'boton_opciones': {'x': 770, 'y': 20, 'ancho': 200, 'alto': 50, 'texto': 'OPCIONES', 'color_normal': (70, 130, 180)},
    'boton_salir': {'x': 400, 'y': 600, 'ancho': 200, 'alto': 50, 'texto': 'SALIR', 'color_normal': (180, 70, 70)},

}

# Menús para el modo Selección de Usuario #
MENU_SELECCION_USUARIO = {
    'boton_usuario_1': {'x': 100, 'y': 175, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 1', 'color_normal': (70, 130, 180)},
    'boton_usuario_2': {'x': 270, 'y': 175, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 2', 'color_normal': (70, 130, 180)},
    'boton_usuario_3': {'x': 440, 'y': 175, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 3', 'color_normal': (70, 130, 180)},
    'boton_usuario_4': {'x': 610, 'y': 175, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 4', 'color_normal': (70, 130, 180)},
    'boton_usuario_5': {'x': 780, 'y': 175, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 5', 'color_normal': (70, 130, 180)},
    'boton_usuario_6': {'x': 100, 'y': 350, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 6', 'color_normal': (70, 130, 180)},
    'boton_usuario_7': {'x': 270, 'y': 350, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 7', 'color_normal': (70, 130, 180)},
    'boton_usuario_8': {'x': 440, 'y': 350, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 8', 'color_normal': (70, 130, 180)},
    'boton_usuario_9': {'x': 610, 'y': 350, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 9', 'color_normal': (70, 130, 180)},
    'boton_usuario_10': {'x': 780, 'y': 350, 'ancho': 150, 'alto': 50, 'texto': 'Usuario 10', 'color_normal': (70, 130, 180)},
    'boton_volver': {'x': 400, 'y': 550, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER', 'color_normal': (180, 70, 70)}
}

MENU_CREAR_USUARIO = {
    'boton_confirmar': {'x': 400, 'y': 400, 'ancho': 200, 'alto': 50, 'texto': 'CONFIRMAR', 'color_normal': (100, 180, 100)},
    'boton_volver': {'x': 400, 'y': 470, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER', 'color_normal': (180, 70, 70)}
}

MENU_CONFIRMAR_CREACION = {
    'boton_crear': {'x': 300, 'y': 350, 'ancho': 200, 'alto': 50, 'texto': 'CREAR USUARIO', 'color_normal': (100, 180, 100)},
    'boton_cancelar': {'x': 500, 'y': 350, 'ancho': 200, 'alto': 50, 'texto': 'CANCELAR', 'color_normal': (180, 70, 70)}
}

# Menús para el modo Opciones #
MENU_OPCIONES = {
    'boton_sonido': {'x': 400, 'y': 200, 'ancho': 200, 'alto': 50, 'texto': 'SONIDO: ON', 'color_normal': (100, 180, 100)},
    'boton_dificultad': {'x': 400, 'y': 270, 'ancho': 200, 'alto': 50, 'texto': 'DIFICULTAD', 'color_normal': (70, 130, 180)},
    'boton_video': {'x': 400, 'y': 340, 'ancho': 200, 'alto': 50, 'texto': 'VIDEO', 'color_normal': (70, 130, 180)},
    'boton_volver': {'x': 400, 'y': 410, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER', 'color_normal': (180, 70, 70)}
}

# Menús para el modo Multiple Choice #
MENU_JUEGO_PREGUNTA = {
    'boton_opcion_1': {'x': 300, 'y': 400, 'ancho': 400, 'alto': 50, 'texto': 'OPCION 1', 'color_normal': (70, 130, 180)},
    'boton_opcion_2': {'x': 300, 'y': 470, 'ancho': 400, 'alto': 50, 'texto': 'OPCION 2', 'color_normal': (70, 130, 180)},
    'boton_opcion_3': {'x': 300, 'y': 540, 'ancho': 400, 'alto': 50, 'texto': 'OPCION 3', 'color_normal': (70, 130, 180)},
    'boton_opcion_4': {'x': 300, 'y': 610, 'ancho': 400, 'alto': 50, 'texto': 'OPCION 4', 'color_normal': (70, 130, 180)},
    'boton_salir_juego': {'x': 20, 'y': 20, 'ancho': 250, 'alto': 40, 'texto': 'VOLVER AL MENÚ', 'color_normal': (180, 70, 70)}
}

MENU_RESULTADO_RONDA = {
    'boton_continuar': {'x': 400, 'y': 500, 'ancho': 200, 'alto': 50, 'texto': 'CONTINUAR', 'color_normal': (100, 180, 100)},
    'boton_salir': {'x': 400, 'y': 570, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER AL MENÚ', 'color_normal': (180, 70, 70)}
}

MENU_RESULTADO_FINAL = {
    'boton_menu_principal': {'x': 350, 'y': 500, 'ancho': 300, 'alto': 50, 'texto': 'VOLVER AL MENÚ', 'color_normal': (70, 130, 180)}
}

# Menús para el modo Verdadero o Falso #
MENU_JUEGO_PREGUNTA_VoF = {
    'boton_verdadero': {'x': 300, 'y': 400, 'ancho': 400, 'alto': 50, 'texto': 'VERDADERO', 'color_normal': (100, 180, 100)},
    'boton_falso': {'x': 300, 'y': 470, 'ancho': 400, 'alto': 50, 'texto': 'FALSO', 'color_normal': (180, 70, 70)},
    'boton_salir_juego': {'x': 20, 'y': 20, 'ancho': 250, 'alto': 40, 'texto': 'VOLVER AL MENÚ', 'color_normal': (180, 70, 70)}
}

MENU_RESULTADO_RONDA_VoF = {
    'boton_continuar': {'x': 400, 'y': 500, 'ancho': 200, 'alto': 50, 'texto': 'CONTINUAR', 'color_normal': (100, 180, 100)},
    'boton_salir': {'x': 400, 'y': 570, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER AL MENÚ', 'color_normal': (180, 70, 70)}
}

MENU_RESULTADO_FINAL_VoF = {
    'boton_menu_principal': {'x': 350, 'y': 500, 'ancho': 300, 'alto': 50, 'texto': 'VOLVER AL MENÚ', 'color_normal': (70, 130, 180)},
}

# Menús para el modo Laberinto de Espejos #
MENU_LABERINTO_JUEGO = {
    'boton_salir_juego': {'x': 20, 'y': 20, 'ancho': 210, 'alto': 40, 'texto': 'VOLVER AL MENÚ', 'color_normal': (180, 70, 70)    }
}

MENU_LABERINTO_RESULTADO = {
    'boton_menu_principal': {'x': 350, 'y': 500, 'ancho': 300, 'alto': 50, 'texto': 'VOLVER AL MENÚ', 'color_normal': (70, 130, 180)}
}

MENU_SELECCION_MODO_LABERINTO = {
    'boton_modo_normal': {'x': 400, 'y': 250, 'ancho': 200, 'alto': 50, 'texto': 'MODO NORMAL (10x15)', 'color_normal': (70, 130, 180)},
    'boton_modo_personalizado': {'x': 400, 'y': 320, 'ancho': 200, 'alto': 50, 'texto': 'MODO PERSONALIZADO', 'color_normal': (100, 180, 100)},
    'boton_volver': {'x': 400, 'y': 390, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER', 'color_normal': (180, 70, 70)}
}

MENU_SELECCION_DIFICULTAD_LABERINTO = {
    'boton_facil': {'x': 400, 'y': 200, 'ancho': 200, 'alto': 50, 'texto': 'FÁCIL (10x15)', 'color_normal': (70, 130, 180)},
    'boton_medio': {'x': 400, 'y': 270, 'ancho': 200, 'alto': 50, 'texto': 'MEDIO (10x18)', 'color_normal': (100, 180, 100)},
    'boton_dificil': {'x': 400, 'y': 340, 'ancho': 200, 'alto': 50, 'texto': 'DIFÍCIL (12x18)', 'color_normal': (180, 180, 70)},
    'boton_deathrow': {'x': 392, 'y': 410, 'ancho': 215, 'alto': 50, 'texto': 'DEATHROW (12x22)', 'color_normal': (180, 70, 70)},
    'boton_volver': {'x': 400, 'y': 480, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER', 'color_normal': (180, 70, 70)}
}

# Menú para la tienda de medallas #
MENU_TIENDA = {
    'boton_volver': {
        'x': 700, 
        'y': 650, 
        'ancho': 200, 
        'alto': 50, 
        'texto': 'VOLVER', 
        'color_normal': (180, 70, 70)
    }
}

# Menú para el leaderboard #
MENU_LEADERBOARD = {
    'boton_volver': {'x': 400, 'y': 600, 'ancho': 200, 'alto': 50, 'texto': 'VOLVER AL MENÚ', 'color_normal': (180, 70, 70)}
}