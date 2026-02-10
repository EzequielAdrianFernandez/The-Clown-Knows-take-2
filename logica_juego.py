import random
import json
import csv
import time

def cargar_preguntas_desde_csv(ruta_csv):
    """Carga las preguntas desde CSV a la estructura del juego"""
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
                'incorrectas': [
                    fila['incorrecta1'],
                    fila['incorrecta2'], 
                    fila['incorrecta3']
                ]
            }
            
            preguntas[categoria][dificultad].append(pregunta_data)
    
    return preguntas

def cargar_configuraciones(ruta_json):
    """Carga las configuraciones desde JSON"""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        return json.load(file)

def cargar_usuarios(ruta_json):
    """Carga los usuarios desde JSON"""
    try:
        with open(ruta_json, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno vacío
        usuarios = {}
        guardar_json(ruta_json, usuarios)
        return usuarios

def guardar_json(ruta, datos):
    """Guarda datos en archivo JSON"""
    with open(ruta, 'w', encoding='utf-8') as file:
        json.dump(datos, file, indent=4, ensure_ascii=False)

def reestablecer_configuraciones(config, ruta_config):
    """Restablece configuraciones a valores iniciales"""
    config["aciertos"] = 0
    config["aciertos_ronda"] = 0
    config["fallas"] = 0
    config["fallas_ronda"] = 0
    config["ronda"] = 1
    config["tickets"] = 0
    config["tickets_conseguidos"] = 0
    config["tickets_ronda"] = 0
    config["limite"] = 10
    config["ingreso"] = "no_ingreso"
    config["ingreso_filtrado"] = "ingreso_no_filtrado"
    config["valido"] = "no_valido"
    config["seguir_jugando"] = True
    config["mensaje"] = "sin_mensaje"
    config["total_preguntas"] = 0
    config["porcentaje_acierto"] = 0
    config["dificultad"] = "dificultad_no_establecida"
    config["verdadera"] = "verdadera_no_cambiada"
    config["respuestas"] = ["no_respuesta_1", "no_respuesta_2", "no_respuesta_3", "no_respuesta_4"]
    config["pregunta"] = "sin_pregunta"
    config["categoria"] = "sin_categoria"
    config["contesto"] = False
    config["boletos_acumulados_partida"] = 0
    config["record_boletos_previo"] = 0
    config["boletos_ganados_partida"] = 0
    config["tiempo_partida"] = 0
    config["tiempo_promedio_usuario"] = 0
    config["nuevo_tiempo"] = 0
    
    guardar_json(ruta_config, config)

def determinar_dificultad_y_tickets(configuraciones, ronda):
    """Determina la dificultad y tickets según la ronda"""
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
    """Selecciona una pregunta aleatoria según categoría y dificultad"""
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
    """Remueve la pregunta usada del diccionario - Multiple Choice"""
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

def remover_pregunta_usada_VoF(biblioteca_preguntas, biblioteca_configuraciones):
    """Remueve la pregunta usada del diccionario - Verdadero o Falso"""
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

def randomizar_respuestas(config):
    """Mezcla las respuestas aleatoriamente"""
    verdadera = config["verdadera"]
    lista_temp = [verdadera] + config["respuestas"]
    random.shuffle(lista_temp)
    config["respuestas"] = lista_temp

def verificar_respuesta(config, opcion_seleccionada):
    """Verifica si la respuesta seleccionada es correcta"""
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
        config["tickets_ronda"] = 0

    config["contesto"] = True

def acreditar_tickets_ronda(config):
    """Acredita los tickets ganados en la ronda"""
    config["tickets_conseguidos"] += config["tickets_ronda"]
    config["aciertos"] += config["aciertos_ronda"]
    config["fallas"] += config["fallas_ronda"]

def crear_nuevo_usuario(usuarios, nombre_usuario):
    """Crea un nuevo usuario en el sistema"""
    # Encontrar el próximo ID disponible
    proximo_id = 1
    for usuario_id in usuarios.keys():
        if usuario_id.startswith('usuario_'):
            try:
                id_num = int(usuario_id.split('_')[1])
                if id_num >= proximo_id:
                    proximo_id = id_num + 1
            except ValueError:
                continue
    
    nuevo_id = f"usuario_{proximo_id}"
    
    # Crear estructura del nuevo usuario
    usuarios[nuevo_id] = {
        "nombre": nombre_usuario,
        "record_boletos": 0,
        "total_boletos": 0,
        "partidas_jugadas": 0,
        "tiempo_promedio": 0,
        "medallas": ""
    }
    
    guardar_json("z_usuarios.json", usuarios)
    return nuevo_id

def actualizar_estadisticas_usuario(usuarios, usuario_id, config):
    """Actualiza las estadísticas del usuario después de una partida"""
    if usuario_id in usuarios:
        usuario = usuarios[usuario_id]
        
        # Actualizar tickets totales
        usuario["total_boletos"] += config["tickets_conseguidos"]
        
        # Actualizar record si es mayor
        if config["tickets_conseguidos"] > usuario["record_boletos"]:
            usuario["record_boletos"] = config["tickets_conseguidos"]
        
        # Actualizar tiempo promedio
        tiempo_actual = config.get("tiempo_partida", 0)###################################################################MARCADOR DE GET
        partidas_anteriores = usuario["partidas_jugadas"]
        promedio_anterior = usuario["tiempo_promedio"]
        
        if partidas_anteriores > 0:
            tiempo_total_anterior = promedio_anterior * partidas_anteriores
            nuevo_tiempo_total = tiempo_total_anterior + tiempo_actual
            usuario["tiempo_promedio"] = nuevo_tiempo_total / (partidas_anteriores + 1)
        else:
            usuario["tiempo_promedio"] = tiempo_actual
        
        # Incrementar partidas jugadas
        usuario["partidas_jugadas"] += 1
        
        # Asignar medallas basadas en logros
        usuario["medallas"] = calcular_medallas(usuario)
        
        guardar_json("z_usuarios.json", usuarios)

def calcular_medallas(usuario):
    """Calcula las medallas del usuario basado en sus logros"""
    medallas = []
    
    # Medalla por partidas jugadas
    if usuario["partidas_jugadas"] >= 10:
        medallas.append("🎮")  # Jugador experimentado
    if usuario["partidas_jugadas"] >= 25:
        medallas.append("🏆")  # Jugador veterano
    
    # Medalla por tickets
    if usuario["record_boletos"] >= 100:
        medallas.append("👑")  # Rey del juego
    if usuario["total_boletos"] >= 500:
        medallas.append("💰")  # Rico
    
    # Medalla por tiempo
    if usuario["tiempo_promedio"] < 60 and usuario["partidas_jugadas"] >= 5:
        medallas.append("⚡")  # Veloz
    
    # Medalla por precisión (si tuviéramos ese dato)
    
    return "".join(medallas)

def formatear_tiempo(segundos):
    """Formatea el tiempo en segundos a un string legible"""
    if segundos < 60:
        return f"{segundos:.1f} segundos"
    else:
        minutos = int(segundos // 60)
        segundos_restantes = segundos % 60
        return f"{minutos} minuto{'s' if minutos > 1 else ''} y {segundos_restantes:.1f} segundos"

##############VoF##############

def cargar_preguntas_desde_csv(ruta_csv):
    """Carga las preguntas desde CSV a la estructura del juego - Múltiple Choice"""
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
                'incorrectas': [
                    fila['incorrecta1'],
                    fila['incorrecta2'], 
                    fila['incorrecta3']
                ]
            }
            
            preguntas[categoria][dificultad].append(pregunta_data)
    
    return preguntas

def cargar_preguntas_VoF_desde_csv(ruta_csv):
    """Carga las preguntas de Verdadero o Falso desde CSV"""
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

def determinar_dificultad_y_tickets(configuraciones, ronda):
    """Determina la dificultad y tickets según la ronda - Multiple Choice"""
    if ronda <= 3:
        configuraciones["dificultad"] = "facil"
        configuraciones["tickets_ronda"] = 10
    elif ronda <= 6:
        configuraciones["dificultad"] = "medio"
        configuraciones["tickets_ronda"] = 30
    else:
        configuraciones["dificultad"] = "dificil"
        configuraciones["tickets_ronda"] = 50

def determinar_dificultad_y_tickets_VoF(configuraciones, ronda):
    """Determina la dificultad y tickets según la ronda - Verdadero o Falso"""
    if ronda <= 3:
        configuraciones["dificultad"] = "facil"
        configuraciones["tickets_ronda"] = 5  # Menos tickets que multiple choice
    elif ronda <= 6:
        configuraciones["dificultad"] = "medio"
        configuraciones["tickets_ronda"] = 10
    else:
        configuraciones["dificultad"] = "dificil"
        configuraciones["tickets_ronda"] = 15

def seleccionar_pregunta(biblioteca, config):
    """Selecciona una pregunta aleatoria según categoría y dificultad - Multiple Choice"""
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

def seleccionar_pregunta_VoF(biblioteca, config):
    """Selecciona una pregunta aleatoria para Verdadero o Falso"""
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

def randomizar_respuestas(config):
    """Mezcla las respuestas aleatoriamente - Multiple Choice"""
    verdadera = config["verdadera"]
    lista_temp = [verdadera] + config["respuestas"]
    random.shuffle(lista_temp)
    config["respuestas"] = lista_temp

def verificar_respuesta(config, opcion_seleccionada):
    """Verifica si la respuesta seleccionada es correcta - Multiple Choice"""
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
        config["tickets_ronda"] = 0

    config["contesto"] = True

def verificar_respuesta_VoF(config, opcion_seleccionada):
    """Verifica si la respuesta seleccionada es correcta - Verdadero o Falso"""
    config["ingreso_filtrado"] = opcion_seleccionada
    config["valido"] = True
    
    # opcion_seleccionada será "verdadero" o "falso"
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

