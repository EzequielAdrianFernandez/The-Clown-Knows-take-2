import pygame
import os
from logica_juego import guardar_json

def musica_inicializar():
    """Inicializa el sistema de audio de pygame"""
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"❌ Error al inicializar el sistema de audio: {e}")

def musica_cargar_y_reproducir(nombre_archivo, volumen=0.5):
    """
    Carga y reproduce una música automáticamente.
    """
    # Primero intentar con .mp3
    ruta_mp3 = f"musica/{nombre_archivo}.mp3"
    ruta_wav = f"musica/{nombre_archivo}.wav"
    
    if os.path.exists(ruta_mp3):
        ruta = ruta_mp3
    elif os.path.exists(ruta_wav):
        ruta = ruta_wav
    else:
        print(f"❌ No se encontró: {nombre_archivo}.mp3 ni {nombre_archivo}.wav")
        return False
    
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play(-1)  # SIEMPRE reproducir
        pygame.mixer.music.set_volume(volumen)
        print(f"🎵 Música cargada: {os.path.basename(ruta)}")
        return True
    except Exception as e:
        print(f"❌ Error al cargar {ruta}: {e}")
        return False

def musica_actualizar_volumen(volumen):
    try:
        pygame.mixer.music.set_volume(volumen)
    except Exception as e:
        print(f"❌ Error al actualizar volumen: {e}")

def guardar_configuracion_audio(configuraciones, estado_audio):
    """
    Guarda la configuración de audio en el JSON.
    SOLO mute y volumen.
    """
    configuraciones["audio_mute"] = estado_audio["mute"]
    configuraciones["audio_volumen"] = estado_audio["volumen"]
    
    guardar_json("z_configuraciones.json", configuraciones)
    print(f"💾 Audio guardado: mute={estado_audio['mute']}, vol={estado_audio['volumen']}")

def toggle_mute_con_guardado(estado):
    """
    Alterna mute y guarda la configuración.
    ÚNICA función de control de audio.
    """
    nuevo_estado = estado.copy()
    nuevo_estado['musica_mute'] = not nuevo_estado['musica_mute']
    
    # Aplicar mute
    if nuevo_estado['musica_mute']:
        musica_actualizar_volumen(0.0)
        print("🔇 MUTE activado")
    else:
        musica_actualizar_volumen(nuevo_estado['musica_volumen'])
        print("🔊 UNMUTE activado")
    
    # Guardar configuración
    estado_audio = {
        "mute": nuevo_estado['musica_mute'],
        "volumen": nuevo_estado['musica_volumen']
    }
    guardar_configuracion_audio(nuevo_estado['configuraciones'], estado_audio)
    
    return nuevo_estado

def musica_actualizar_completo(eventos, estado_juego, forzar_actualizacion=False):
    """
    Función simplificada - ya no responde a teclas
    """
    # Ya no hay control por tecla M aquí
    # Solo actualiza si se fuerza
    if forzar_actualizacion:
        from manejador_estados import actualizar_musica_segun_estado
        estado_juego = actualizar_musica_segun_estado(estado_juego)
    
    return estado_juego

def dibujar_musica_pantalla(pantalla, fuente, estado_juego, ALTO_PANTALLA):
    """
    Dibuja información de música en pantalla.
    SOLO muestra estado de mute.
    """
    mute_texto = "🔇 SILENCIADO" if estado_juego['musica_mute'] else "🔊 SONANDO"
    musica_texto = estado_juego['musica_actual'].upper()
    
    # Texto de estado de música
    texto_musica = fuente.render(
        f"Música: {musica_texto}", 
        True, (200, 200, 255)
    )
    pantalla.blit(texto_musica, (10, ALTO_PANTALLA - 60))
    
    # Texto de controles (SOLO M)
    texto_controles = fuente.render(
        f"{mute_texto} | Control: M (silenciar/sonar)", 
        True, (200, 200, 200)
    )
    pantalla.blit(texto_controles, (10, ALTO_PANTALLA - 30))