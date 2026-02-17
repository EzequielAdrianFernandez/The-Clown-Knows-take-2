import random
import json
import csv
import time

from menu_definiciones import MENU_PRINCIPAL


# ============================================================================
# 📂 CARGA DE DATOS DESDE ARCHIVOS
# ============================================================================

def cargar_preguntas_desde_csv(ruta_csv):
    """
    📖 Carga las preguntas de Multiple Choice desde un archivo CSV.
    
    Estructura esperada del CSV:
        categoria, dificultad, pregunta, correcta, incorrecta1, incorrecta2, incorrecta3
    
    Estructura de salida:
        {
            "Categoría1": {
                "facil":  [ {pregunta, correcta, incorrectas}, ... ],
                "medio":  [ ... ],
                "dificil": [ ... ]
            },
            ...
        }
    
    Args:
        ruta_csv (str): Ruta al archivo CSV
    
    Returns:
        dict: Biblioteca de preguntas organizada por categoría → dificultad → lista
    """
    preguntas = {}
    
    with open(ruta_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        filas = list(reader)
        
        for i in range(len(filas)):
            fila = filas[i]
            categoria = fila['categoria']
            dificultad = fila['dificultad']
            
            # Si la categoría no existe, crearla con las 3 dificultades
            if categoria not in preguntas:
                preguntas[categoria] = {
                    'facil': [],
                    'medio': [],
                    'dificil': []
                }
            
            pregunta_data = {
                'preguntas': fila['pregunta'],
                'correcta': fila['correcta'],
                'incorrectas': [
                    fila['incorrecta1'],
                    fila['incorrecta2'], 
                    fila['incorrecta3']
                ]
            }
            
            preguntas[categoria][dificultad].append(pregunta_data)
    
    return preguntas


def cargar_preguntas_VoF_desde_csv(ruta_csv):
    """
    📖 Carga las preguntas de Verdadero o Falso desde un CSV.
    
    Estructura esperada del CSV:
        categoria, dificultad, pregunta, correcta, incorrecta
    
    La columna 'correcta' debe ser "verdadero" o "falso"
    
    Args:
        ruta_csv (str): Ruta al archivo CSV
    
    Returns:
        dict: Biblioteca de preguntas VoF (misma estructura que Multiple Choice)
    """
    preguntas = {}
    
    with open(ruta_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        filas = list(reader)
        
        for i in range(len(filas)):
            fila = filas[i]
            categoria = fila['categoria']
            dificultad = fila['dificultad']
            
            if categoria not in preguntas:
                preguntas[categoria] = {
                    'facil': [],
                    'medio': [],
                    'dificil': []
                }
            
            pregunta_data = {
                'preguntas': fila['pregunta'],
                'correcta': fila['correcta'],
                'incorrecta': fila['incorrecta']
            }
            
            preguntas[categoria][dificultad].append(pregunta_data)
    
    return preguntas


def cargar_configuraciones(ruta_json):
    """
    ⚙️ Carga las configuraciones desde un archivo JSON.
    
    Args:
        ruta_json (str): Ruta al archivo de configuración
    
    Returns:
        dict: Configuraciones del juego (sonido, mute, etc.)
    """
    with open(ruta_json, 'r', encoding='utf-8') as file:
        return json.load(file)


def cargar_usuarios(ruta_json):
    """
    👥 Carga los usuarios desde un archivo JSON.
    
    Si el archivo no existe, lo crea vacío.
    
    Args:
        ruta_json (str): Ruta a z_usuarios.json
    
    Returns:
        dict: Diccionario de usuarios (usuario_1, usuario_2, ...)
    """
    try:
        with open(ruta_json, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Primera ejecución: crear archivo vacío
        usuarios = {}
        guardar_json(ruta_json, usuarios)
        return usuarios


def guardar_json(ruta, datos):
    """
    💾 Guarda cualquier diccionario en formato JSON.
    
    Args:
        ruta (str): Ruta del archivo a guardar
        datos (dict): Datos a serializar
    """
    with open(ruta, 'w', encoding='utf-8') as file:
        json.dump(datos, file, indent=4, ensure_ascii=False)


# ============================================================================
# 🔄 CONFIGURACIÓN Y RESETEO
# ============================================================================

def reestablecer_configuraciones(config, ruta_config):
    """
    🧹 Restablece TODAS las configuraciones a sus valores iniciales.
    
    Se llama al comenzar una nueva partida.
    Evita que queden datos sucios de partidas anteriores.
    
    Args:
        config (dict): Diccionario de configuración a modificar
        ruta_config (str): Ruta para guardar los cambios
    """
    # Contadores básicos
    config["aciertos"] = 0
    config["aciertos_ronda"] = 0
    config["fallas"] = 0
    config["fallas_ronda"] = 0
    config["ronda"] = 1
    config["limite"] = 10  # 10 rondas por partida
    
    # Tickets
    config["tickets"] = 0
    config["tickets_conseguidos"] = 0
    config["tickets_ronda"] = 0
    
    # Estado de la pregunta
    config["ingreso"] = "no_ingreso"
    config["ingreso_filtrado"] = "ingreso_no_filtrado"
    config["valido"] = "no_valido"
    config["seguir_jugando"] = True
    config["mensaje"] = "sin_mensaje"
    config["contesto"] = False
    
    # Datos de pregunta
    config["total_preguntas"] = 0
    config["porcentaje_acierto"] = 0
    config["dificultad"] = "dificultad_no_establecida"
    config["verdadera"] = "verdadera_no_cambiada"
    config["respuestas"] = ["no_respuesta_1", "no_respuesta_2", "no_respuesta_3", "no_respuesta_4"]
    config["pregunta"] = "sin_pregunta"
    config["categoria"] = "sin_categoria"
    
    # Estadísticas de usuario (se actualizan al final)
    config["boletos_acumulados_partida"] = 0
    config["record_boletos_previo"] = 0
    config["boletos_ganados_partida"] = 0
    config["tiempo_partida"] = 0
    config["tiempo_promedio_usuario"] = 0
    config["nuevo_tiempo"] = 0
    
    guardar_json(ruta_config, config)


# ============================================================================
# 🎯 LÓGICA DE PREGUNTAS - MULTIPLE CHOICE
# ============================================================================

def determinar_dificultad_y_tickets(configuraciones, ronda):
    """
    📊 Asigna dificultad y tickets según el número de ronda (Multiple Choice).
    
    Reglas:
        Ronda 1-3 : Fácil   → 10 tickets
        Ronda 4-6 : Medio   → 30 tickets
        Ronda 7-10: Difícil → 50 tickets
    
    Args:
        configuraciones (dict): Configuración de la partida
        ronda (int): Número de ronda actual (1-10)
    """
    if ronda <= 3:
        configuraciones["dificultad"] = "facil"
        configuraciones["tickets_ronda"] = 10
    elif ronda <= 6:
        configuraciones["dificultad"] = "medio"
        configuraciones["tickets_ronda"] = 30
    else:
        configuraciones["dificultad"] = "dificil"
        configuraciones["tickets_ronda"] = 50


def seleccionar_pregunta(biblioteca, config):
    """
    🎲 Elige una pregunta aleatoria de la categoría y dificultad actual.
    
    Args:
        biblioteca (dict): Biblioteca de preguntas (de cargar_preguntas_desde_csv)
        config (dict): Configuración actual (contiene categoria y dificultad)
    
    Returns:
        bool: True si había preguntas disponibles, False si se acabaron
    """
    categorias_disponibles = list(biblioteca.keys())
    config["categoria"] = random.choice(categorias_disponibles)
    categoria = config["categoria"]

    dificultad = config["dificultad"]
    preguntas_disponibles = biblioteca[categoria][dificultad]
    
    if len(preguntas_disponibles) > 0:
        pregunta = random.choice(preguntas_disponibles)
        config["pregunta"] = pregunta
        config["verdadera"] = pregunta["correcta"]
        config["respuestas"] = pregunta["incorrectas"]
        return True
    return False


def remover_pregunta_usada(biblioteca_preguntas, biblioteca_configuraciones):
    """
    🗑️ Elimina la pregunta recién usada para no repetirla.
    
    Busca en la biblioteca la pregunta exacta (por el texto) y la elimina.
    
    Args:
        biblioteca_preguntas (dict): Biblioteca de preguntas
        biblioteca_configuraciones (dict): Configuración con la pregunta usada
    """
    categoria = biblioteca_configuraciones["categoria"]
    dificultad = biblioteca_configuraciones["dificultad"]
    pregunta_usada = biblioteca_configuraciones["pregunta"]
    
    if categoria in biblioteca_preguntas and dificultad in biblioteca_preguntas[categoria]:
        lista_preguntas = biblioteca_preguntas[categoria][dificultad]
        for i in range(len(lista_preguntas)):
            pregunta = lista_preguntas[i]
            if pregunta["preguntas"] == pregunta_usada["preguntas"]:
                lista_preguntas.pop(i)
                break  # Solo una pregunta por ronda


def randomizar_respuestas(config):
    """
    🔀 Mezcla las respuestas para que la correcta no esté siempre en la misma posición.
    
    Toma la respuesta correcta y las 3 incorrectas, las mezcla y guarda el orden.
    """
    verdadera = config["verdadera"]
    lista_temp = [verdadera] + config["respuestas"]
    random.shuffle(lista_temp)
    config["respuestas"] = lista_temp


def verificar_respuesta(config, opcion_seleccionada):
    """
    ✅ Verifica si la opción elegida por el jugador es correcta.
    
    Args:
        config (dict): Configuración con la pregunta activa
        opcion_seleccionada (int): Índice de la respuesta (0-3)
    """
    respuestas = config["respuestas"]
    verdadera = config["verdadera"]
    
    config["ingreso_filtrado"] = opcion_seleccionada
    config["valido"] = True
    
    if respuestas[opcion_seleccionada] == verdadera:
        config["mensaje"] = "¡Correcta!"
        config["aciertos_ronda"] = 1
        config["fallas_ronda"] = 0
    else:
        config["mensaje"] = "Incorrecta"
        config["aciertos_ronda"] = 0
        config["fallas_ronda"] = 1
        config["tickets_ronda"] = 0  # No gana tickets si falla

    config["contesto"] = True


# ============================================================================
# 💰 SISTEMA DE TICKETS
# ============================================================================

def acreditar_tickets_ronda(config):
    """
    💵 Suma los tickets ganados en la ronda al total de la partida.
    
    También acumula aciertos y fallas para el resultado final.
    """
    config["tickets_conseguidos"] += config["tickets_ronda"]
    config["aciertos"] += config["aciertos_ronda"]
    config["fallas"] += config["fallas_ronda"]


# ============================================================================
# 🎯 LÓGICA DE PREGUNTAS - VERDADERO O FALSO
# ============================================================================

def determinar_dificultad_y_tickets_VoF(configuraciones, ronda):
    """
    📊 Asigna dificultad y tickets para Verdadero/Falso (menos tickets que MC).
    
    Reglas:
        Ronda 1-3 : Fácil   → 5 tickets
        Ronda 4-6 : Medio   → 10 tickets
        Ronda 7-10: Difícil → 15 tickets
    """
    if ronda <= 3:
        configuraciones["dificultad"] = "facil"
        configuraciones["tickets_ronda"] = 5
    elif ronda <= 6:
        configuraciones["dificultad"] = "medio"
        configuraciones["tickets_ronda"] = 10
    else:
        configuraciones["dificultad"] = "dificil"
        configuraciones["tickets_ronda"] = 15


def seleccionar_pregunta_VoF(biblioteca, config):
    """
    🎲 Elige una pregunta de Verdadero/Falso.
    
    Args:
        biblioteca (dict): Biblioteca de preguntas VoF
        config (dict): Configuración actual
    
    Returns:
        bool: True si había preguntas disponibles
    """
    categorias_disponibles = list(biblioteca.keys())
    config["categoria"] = random.choice(categorias_disponibles)
    categoria = config["categoria"]

    dificultad = config["dificultad"]
    preguntas_disponibles = biblioteca[categoria][dificultad]
    
    if len(preguntas_disponibles) > 0:
        pregunta = random.choice(preguntas_disponibles)
        config["pregunta"] = pregunta
        config["verdadera"] = pregunta["correcta"]
        config["falsa"] = pregunta["incorrecta"]
        return True
    return False


def remover_pregunta_usada_VoF(biblioteca_preguntas, biblioteca_configuraciones):
    """
    🗑️ Elimina pregunta usada de Verdadero/Falso (misma lógica que Multiple Choice).
    """
    categoria = biblioteca_configuraciones["categoria"]
    dificultad = biblioteca_configuraciones["dificultad"]
    pregunta_usada = biblioteca_configuraciones["pregunta"]
    
    if categoria in biblioteca_preguntas and dificultad in biblioteca_preguntas[categoria]:
        lista_preguntas = biblioteca_preguntas[categoria][dificultad]
        for i in range(len(lista_preguntas)):
            pregunta = lista_preguntas[i]
            if pregunta["preguntas"] == pregunta_usada["preguntas"]:
                lista_preguntas.pop(i)
                break


def verificar_respuesta_VoF(config, opcion_seleccionada):
    """
    ✅ Verifica respuesta en Verdadero/Falso.
    
    Args:
        config (dict): Configuración con la pregunta
        opcion_seleccionada (str): "verdadero" o "falso"
    """
    config["ingreso_filtrado"] = opcion_seleccionada
    config["valido"] = True
    
    if opcion_seleccionada == config["verdadera"]:
        config["mensaje"] = "¡Correcta!"
        config["aciertos_ronda"] = 1
        config["fallas_ronda"] = 0
    else:
        config["mensaje"] = "Incorrecta"
        config["aciertos_ronda"] = 0
        config["fallas_ronda"] = 1
        config["tickets_ronda"] = 0

    config["contesto"] = True

# ============================================================================
# 👤 GESTIÓN DE USUARIOS Y ESTADÍSTICAS
# ============================================================================

def crear_usuario_nuevo(usuarios, slot_numero, nombre_usuario):
    """
    🆕 Crea un nuevo usuario en un SLOT ESPECÍFICO (1-10).
    
    Esta es la función ACTIVA para creación de usuarios.
    
    Args:
        usuarios (dict): Diccionario de usuarios
        slot_numero (int): Slot 1-10
        nombre_usuario (str): Nombre del jugador
    
    Returns:
        dict: Usuarios actualizados (con el nuevo)
    """
    usuario_id = f"usuario_{slot_numero}"
    
    if usuario_id in usuarios:
        print(f"❌ Slot {slot_numero} ya ocupado por: {usuarios[usuario_id]['nombre']}")
        return usuarios
    
    usuarios[usuario_id] = {
        "nombre": nombre_usuario,
        "record_boletos": 0,
        "total_boletos": 0,
        "partidas_jugadas": 0,
        "tiempo_promedio": 0,
        "medallas": ""
    }
    
    print(f"✅ Usuario creado: {nombre_usuario} en slot {slot_numero}")
    return usuarios


def crear_usuario_y_guardar(estado, menu_principal):
    """
    💾 Función COMPLETA para crear usuario y actualizar estado.
    
    Este es el ORQUESTADOR de la creación de usuarios.
    Se llama desde manejador_estados.py cuando el jugador confirma.
    
    Args:
        estado (dict): Estado completo del juego
        menu_principal (dict): Diccionario MENU_PRINCIPAL para volver
    
    Returns:
        dict: Estado actualizado con el nuevo usuario
    """
    # Validaciones
    if 'slot_seleccionado' not in estado or estado['slot_seleccionado'] is None:
        print("❌ Error: No hay slot seleccionado")
        return estado
    
    if 'nombre_nuevo_usuario' not in estado or not estado['nombre_nuevo_usuario']:
        print("❌ Error: Nombre de usuario vacío")
        return estado
    
    # Crear el usuario
    estado['usuarios'] = crear_usuario_nuevo(
        estado['usuarios'],
        estado['slot_seleccionado'],
        estado['nombre_nuevo_usuario']
    )
    
    # Persistencia
    guardar_json("z_usuarios.json", estado['usuarios'])
    
    # Selección automática
    usuario_id = f"usuario_{estado['slot_seleccionado']}"
    estado['usuario_actual'] = usuario_id
    
    # Volver al menú principal
    estado['estado_actual'] = "menu_principal"
    estado['diccionario_botones_actual'] = menu_principal
    
    # Limpiar datos temporales
    estado['nombre_nuevo_usuario'] = ""
    estado['slot_seleccionado'] = None
    
    print(f"✅ Usuario '{estado['usuarios'][usuario_id]['nombre']}' creado y seleccionado")
    return estado


def actualizar_estadisticas_usuario(usuarios, usuario_id, config):
    """
    📈 Actualiza TODAS las estadísticas de un usuario después de una partida.
    
    Qué actualiza:
    - total_boletos    → Suma los tickets ganados en esta partida
    - record_boletos   → Si es mayor que el anterior
    - tiempo_promedio  → Promedio ponderado con nuevas partidas
    - partidas_jugadas → +1
    - medallas        → Recalcula según logros
    
    Args:
        usuarios (dict): Diccionario de usuarios
        usuario_id (str): ID del usuario a actualizar
        config (dict): Configuración con resultados de la partida
    
    Raises:
        KeyError: Si el usuario no existe
    """
    if usuario_id not in usuarios:
        raise KeyError(f"❌ Usuario '{usuario_id}' no existe")
    
    usuario = usuarios[usuario_id]
    
    # 1. Tickets totales
    usuario["total_boletos"] += config["tickets_conseguidos"]
    
    # 2. Record personal
    if config["tickets_conseguidos"] > usuario["record_boletos"]:
        usuario["record_boletos"] = config["tickets_conseguidos"]
    
    # 3. Tiempo promedio (sin usar .get())
    try:
        tiempo_actual = obtener_tiempo_partida(config)
    except ValueError as e:
        print(f"⚠️  {e} - usando 0")
        tiempo_actual = 0
    
    partidas_anteriores = usuario["partidas_jugadas"]
    promedio_anterior = usuario["tiempo_promedio"]
    
    if partidas_anteriores > 0:
        tiempo_total_anterior = promedio_anterior * partidas_anteriores
        nuevo_tiempo_total = tiempo_total_anterior + tiempo_actual
        usuario["tiempo_promedio"] = nuevo_tiempo_total / (partidas_anteriores + 1)
    else:
        usuario["tiempo_promedio"] = tiempo_actual
    
    # 4. Partidas jugadas
    usuario["partidas_jugadas"] += 1
    
    # 5. Medallas (recalcular)
    usuario["medallas"] = calcular_medallas(usuario)
    
    # 6. Guardar cambios
    guardar_json("z_usuarios.json", usuarios)


def calcular_medallas(usuario):
    """
    🏅 Asigna emojis según logros del usuario.
    
    Reglas:
    - 🎮  → 10+ partidas
    - 🏆  → 25+ partidas  
    - 👑  → Record ≥ 100 tickets
    - 💰  → Total ≥ 500 tickets
    - ⚡  → Promedio < 60s Y 5+ partidas
    
    Args:
        usuario (dict): Datos del usuario
    
    Returns:
        str: String con todos los emojis concatenados (ej: "🎮🏆👑💰⚡")
    """
    medallas = []
    
    # Por partidas jugadas
    if usuario["partidas_jugadas"] >= 10:
        medallas.append("🎮")
    if usuario["partidas_jugadas"] >= 25:
        medallas.append("🏆")
    
    # Por tickets
    if usuario["record_boletos"] >= 100:
        medallas.append("👑")
    if usuario["total_boletos"] >= 500:
        medallas.append("💰")
    
    # Por velocidad
    if usuario["tiempo_promedio"] < 60 and usuario["partidas_jugadas"] >= 5:
        medallas.append("⚡")
    
    return "".join(medallas)


def formatear_tiempo(segundos):
    """
    ⏱️ Convierte segundos a formato legible para humanos.
    
    Ejemplos:
        45.3s    → "45.3 segundos"
        90.2s    → "1 minuto y 30.2 segundos"
        125.5s   → "2 minutos y 5.5 segundos"
    
    Args:
        segundos (float): Tiempo en segundos
    
    Returns:
        str: Tiempo formateado
    """
    if segundos < 60:
        return f"{segundos:.1f} segundos"
    else:
        minutos = int(segundos // 60)
        segundos_restantes = segundos % 60
        return f"{minutos} minuto{'s' if minutos > 1 else ''} y {segundos_restantes:.1f} segundos"


def obtener_tiempo_partida(config, valor_por_defecto=0):
    """
    ⏱️ Extrae el tiempo de partida de forma SEGURA y ROBUSTA.
    
    Reemplaza el uso de .get() con verificaciones explícitas.
    
    Args:
        config (dict): Configuración de la partida
        valor_por_defecto (float): Valor si no existe o es inválido
    
    Returns:
        float: Tiempo de partida en segundos
    
    Raises:
        ValueError: Si el tiempo existe pero no es un número válido
    """
    if 'tiempo_partida' not in config:
        print(f"⚠️  'tiempo_partida' no existe, usando: {valor_por_defecto}")
        return valor_por_defecto
    
    tiempo = config['tiempo_partida']
    
    if not isinstance(tiempo, (int, float)):
        raise ValueError(f"❌ 'tiempo_partida' debe ser número, recibido: {type(tiempo).__name__}")
    
    if tiempo < 0:
        raise ValueError(f"❌ 'tiempo_partida' no puede ser negativo: {tiempo}")
    
    return tiempo