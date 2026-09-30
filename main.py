import pygame
import sys
import random

# ==============================================================================
# 1. MEMORIA Y CONFIGURACIÓN DE DATOS (ARQUITECTURA: DATOS)
# ==============================================================================
# Constantes de pantalla y rejilla
ANCHO_VENTANA = 600
ALTO_VENTANA = 400
TAMANO_BLOQUE = 20
VELOCIDAD = 10  # Tasa de refresco / Velocidad de movimiento

# Definición de paleta de colores en formato RGB
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# ==============================================================================
# 2. LÓGICA DEL JUEGO / CEREBRO (ARQUITECTURA: LÓGICA)
# ==============================================================================
class JuegoSerpiente:
    def __init__(self):
        """Inicializa la librería de Pygame, la ventana principal y los datos iniciales."""
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Juego de la Serpiente - UIDE")
        self.reloj = pygame.time.Clock()
        self.reiniciar_juego()

    def reiniciar_juego(self):
        """Restablece los datos del estado inicial de la partida."""
        self.direccion = "DERECHA"
        self.cabeza = [100, 60]  # Posición X, Y inicial alineada a la rejilla
        self.cuerpo = [[100, 60], [80, 60], [60, 60]]  # Posiciones iniciales del cuerpo
        self.puntuacion = 0
        self.generar_fruta()
        self.game_over = False

    def generar_fruta(self):
        """
        Genera coordenadas aleatorias alineadas perfectamente a la rejilla de 20px
        para evitar desacoples de posición entre serpiente y fruta.
        """
        x = random.randint(0, (ANCHO_VENTANA - TAMANO_BLOQUE) // TAMANO_BLOQUE) * TAMANO_BLOQUE
        y = random.randint(0, (ALTO_VENTANA - TAMANO_BLOQUE) // TAMANO_BLOQUE) * TAMANO_BLOQUE
        self.fruta = [x, y]

    def procesar_eventos(self):
        """CAPTURA DE EVENTOS Y ESTRUCTURAS CONDICIONALES DE CONTROL"""
        # BUCLE FOR: Recorre todos los eventos capturados por el teclado/pantalla
        for evento in pygame.event.get():
            # CONDICIONAL: Detecta si el usuario cierra la ventana
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # CONDICIONAL: Detecta si se presionó una tecla
            elif evento.type == pygame.KEYDOWN:
                # CONDICIONAL EVALUATIVO: Manejo de estado Game Over (Reiniciar juego)
                if self.game_over:
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_r:
                        self.reiniciar_juego()
                else:
                    # CONDICIONALES ANIDADOS Y LÓGICA BOOLEANA: Cambiar dirección impidiendo giros de 180°
                    if evento.key == pygame.K_UP and self.direccion != "ABAJO":
                        self.direccion = "ARRIBA"
                    elif evento.key == pygame.K_DOWN and self.direccion != "ARRIBA":
                        self.direccion = "ABAJO"
                    elif evento.key == pygame.K_LEFT and self.direccion != "DERECHA":
                        self.direccion = "IZQUIERDA"
                    elif evento.key == pygame.K_RIGHT and self.direccion != "IZQUIERDA":
                        self.direccion = "DERECHA"

    def actualizar_logica(self):
        """ACTUALIZACIÓN DE ESTADOS Y EVALUACIÓN DE CONDICIONALES DE COLISIÓN"""
        # CONDICIONAL DE PARADA: Si perdió, detiene el procesamiento de la lógica
        if self.game_over:
            return

        # CONDICIONALES DE MOVIMIENTO: Desplaza la coordenada de la cabeza según la dirección actual
        if self.direccion == "ARRIBA":
            self.cabeza[1] -= TAMANO_BLOQUE
        elif self.direccion == "ABAJO":
            self.cabeza[1] += TAMANO_BLOQUE
        elif self.direccion == "IZQUIERDA":
            self.cabeza[0] -= TAMANO_BLOQUE
        elif self.direccion == "DERECHA":
            self.cabeza[0] += TAMANO_BLOQUE

        # CONDICIONAL DE COLISIÓN 1: Verificación de límites de bordes/paredes
        if (self.cabeza[0] < 0 or self.cabeza[0] >= ANCHO_VENTANA or
            self.cabeza[1] < 0 or self.cabeza[1] >= ALTO_VENTANA):
            self.game_over = True
            return

        # CONDICIONAL DE COLISIÓN 2: Detección si la cabeza choca con su propio cuerpo
        if self.cabeza in self.cuerpo[1:]:
            self.game_over = True
            return

        # Insertar la nueva posición de la cabeza al inicio del arreglo del cuerpo
        self.cuerpo.insert(0, list(self.cabeza))

        # CONDICIONAL DE ALIMENTACIÓN: Detección si la cabeza coincide con la fruta
        if self.cabeza[0] == self.fruta[0] and self.cabeza[1] == self.fruta[1]:
            self.puntuacion += 10  # Incremento de puntuación
            self.generar_fruta()   # Generación de nueva fruta
        else:
            self.cuerpo.pop()      # Mantiene el tamaño removiendo la última cola

# ==============================================================================
# 3. INTERFAZ Y RENDERIZADO VISUAL (ARQUITECTURA: INTERFAZ)
# ==============================================================================
    def dibujar(self):
        """Maneja el renderizado visual de todos los elementos en pantalla."""
        self.pantalla.fill(NEGRO)  # Limpiar pantalla con color de fondo

        # CONDICIONAL DE RENDERIZADO: Elige qué renderizar según el estado del juego
        if not self.game_over:
            # BUCLE FOR: Recorre cada elemento del cuerpo para dibujarlo en pantalla
            for segmento in self.cuerpo:
                pygame.draw.rect(self.pantalla, VERDE, pygame.Rect(segmento[0], segmento[1], TAMANO_BLOQUE, TAMANO_BLOQUE))
            
            # Dibujar posición de la fruta
            pygame.draw.rect(self.pantalla, ROJO, pygame.Rect(self.fruta[0], self.fruta[1], TAMANO_BLOQUE, TAMANO_BLOQUE))

            # Dibujar el marcador de puntuación
            fuente = pygame.font.SysFont('Arial', 20)
            texto_puntos = fuente.render(f"Puntos: {self.puntuacion}", True, BLANCO)
            self.pantalla.blit(texto_puntos, (10, 10))
        else:
            # Pantalla visual de GAME OVER
            fuente_titulo = pygame.font.SysFont('Arial', 32, bold=True)
            fuente_sub = pygame.font.SysFont('Arial', 22)

            texto_go = fuente_titulo.render("GAME OVER", True, ROJO)
            texto_puntos = fuente_sub.render(f"Puntuación Final: {self.puntuacion}", True, BLANCO)
            texto_reiniciar = fuente_sub.render("Presiona ESPACIO o R para reiniciar", True, VERDE)

            self.pantalla.blit(texto_go, (ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2 - 60))
            self.pantalla.blit(texto_puntos, (ANCHO_VENTANA // 2 - 110, ALTO_VENTANA // 2 - 10))
            self.pantalla.blit(texto_reiniciar, (ANCHO_VENTANA // 2 - 170, ALTO_VENTANA // 2 + 40))

        pygame.display.flip()  # Refrescar pantalla

    def ejecutar(self):
        """BUCLE PRINCIPAL DEL JUEGO (GAME LOOP)"""
        # BUCLE WHILE INFINITO: Mantiene la aplicación activa actualizando fotogramas
        while True:
            self.procesar_eventos()
            self.actualizar_logica()
            self.dibujar()
            self.reloj.tick(VELOCIDAD)  # Controla los fotogramas por segundo (FPS)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    juego = JuegoSerpiente()
    juego.ejecutar()