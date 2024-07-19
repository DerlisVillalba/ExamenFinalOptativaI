import pygame
import sys
import random
import pickle

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO, ALTO = 800, 600
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
GRADIENTE_INICIAL = [(0, 0, 255), (0, 255, 255)]

# Lista de colores para los bloques
COLORES_BLOQUES = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ani Ho'a Pelota")

# Fuentes
fuente_grande = pygame.font.SysFont("Arial", 60)
fuente_pequena = pygame.font.SysFont("Arial", 36)

# Sonidos
sonido_pelota = pygame.mixer.Sound("pelota.wav")
sonido_perder = pygame.mixer.Sound("perder.wav")
sonido_romper = pygame.mixer.Sound("romper.mp3")
pygame.mixer.music.load("musica_fondo.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Estado del juego
INICIO = 0
JUGANDO = 1
PAUSA = 2
PERDIDO = 3
GANADO = 4
estado = INICIO

# Variables de juego
puntuacion = 0
vidas = 3
nivel = 1
velocidad_base = 5
incremento_velocidad = 1

# Cargar imágenes
imagen_barra = pygame.image.load("barra.png").convert_alpha()
imagen_pelota = pygame.image.load("pelota_futbol.png").convert_alpha()

# Funciones para guardar y cargar puntuaciones
def guardar_puntuaciones(puntuaciones):
    with open("puntuaciones.pkl", "wb") as archivo:
        pickle.dump(puntuaciones, archivo)

def cargar_puntuaciones():
    try:
        with open("puntuaciones.pkl", "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return []

puntuaciones = cargar_puntuaciones()


# Clases
class Barra(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(imagen_barra, (150, 30))  # Ajustar tamaño si es necesario
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO // 2 - self.rect.width // 2
        self.rect.y = ALTO - 40
        self.velocidad_x = 0

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

class Bola(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(imagen_pelota, (25, 25))  # Ajustar tamaño si es necesario
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Crear máscara para colisiones precisas
        self.rect.x = ANCHO // 2 - self.rect.width // 2
        self.rect.y = ALTO // 2 - self.rect.height // 2
        self.velocidad_x = velocidad_base
        self.velocidad_y = -velocidad_base

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = random.choice(COLORES_BLOQUES)
        self.image = pygame.Surface((75, 30))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def crear_bloques(nivel):
    bloques = pygame.sprite.Group()
    for fila in range(5 + nivel):
        for columna in range(10):
            bloque = Bloque(10 + columna * 78, 10 + fila * 35)
            bloques.add(bloque)
    return bloques

def dibujar_gradiente(superficie, color1, color2):
    for y in range(ALTO):
        color = (
            color1[0] + (color2[0] - color1[0]) * y // ALTO,
            color1[1] + (color2[1] - color1[1]) * y // ALTO,
            color1[2] + (color2[2] - color1[2]) * y // ALTO
        )
        pygame.draw.line(superficie, color, (0, y), (ANCHO, y))

def dibujar_boton(texto, fuente, color, x, y, ancho, alto):
    superficie_boton = pygame.Surface((ancho, alto))
    superficie_boton.fill(color)
    texto_boton = fuente.render(texto, True, BLANCO)
    pantalla.blit(superficie_boton, (x, y))
    pantalla.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))
    return pygame.Rect(x, y, ancho, alto)

def dibujar_pantalla_inicio():
    dibujar_gradiente(pantalla, *GRADIENTE_INICIAL)
    texto_inicio = fuente_grande.render("ANI HO'A PELOTA", True, BLANCO)
    pantalla.blit(texto_inicio, (ANCHO // 2 - texto_inicio.get_width() // 2, ALTO // 4 - texto_inicio.get_height() // 2))
    boton_inicio = dibujar_boton("Iniciar Juego", fuente_pequena, ROJO, ANCHO // 2 - 100, ALTO // 2, 200, 50)
    boton_salir = dibujar_boton("Salir", fuente_pequena, ROJO, ANCHO // 2 - 100, ALTO // 2 + 60, 200, 50)
    texto_sub = fuente_pequena.render("o puedes presionar ENTER para iniciar el juego", True, BLANCO)
    pantalla.blit(texto_sub, (ANCHO // 2 - texto_sub.get_width() // 2, ALTO // 2 + 130))
    texto_puntuaciones = fuente_pequena.render("Top 5 Puntuaciones Altas:", True, BLANCO)
    pantalla.blit(texto_puntuaciones, (10, 10))
    for i, punt in enumerate(puntuaciones):
        texto = fuente_pequena.render(f"{i+1}. {punt}", True, BLANCO)
        pantalla.blit(texto, (10, 40 + i * 30))
        
    return boton_inicio, boton_salir

def dibujar_pantalla_pausa():
    texto_pausa = fuente_grande.render("PAUSA", True, BLANCO)
    pantalla.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 2 - texto_pausa.get_height() // 2))
    texto_sub = fuente_pequena.render("Presiona P para continuar", True, BLANCO)
    pantalla.blit(texto_sub, (ANCHO // 2 - texto_sub.get_width() // 2, ALTO // 2 + texto_pausa.get_height() // 2 + 20))
    boton_salir_pausa = dibujar_boton("Salir", fuente_pequena, ROJO, ANCHO // 2 - 100, ALTO // 2 + texto_pausa.get_height() // 2 + texto_sub.get_height() + 40, 200, 50)
    return boton_salir_pausa

def dibujar_pantalla_fin(juego_ganado):
    if juego_ganado:
        texto_fin = fuente_grande.render("¡GANASTE!", True, VERDE)
    else:
        texto_fin = fuente_grande.render("PERDISTE", True, ROJO)
    pantalla.blit(texto_fin, (ANCHO // 2 - texto_fin.get_width() // 2, ALTO // 2 - texto_fin.get_height() // 2))
    texto_puntaje = fuente_pequena.render(f"Puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(texto_puntaje, (ANCHO // 2 - texto_puntaje.get_width() // 2, ALTO // 2 + texto_fin.get_height() // 2))
    texto_sub = fuente_pequena.render("Presiona ENTER para volver al menu", True, BLANCO)
    pantalla.blit(texto_sub, (ANCHO // 2 - texto_sub.get_width() // 2, ALTO // 2 + texto_fin.get_height() // 2 + 40))

def dibujar_rectangulo_transparente(superficie, color, x, y, ancho, alto, alpha):
    """Dibuja un rectángulo semitransparente."""
    rect_surf = pygame.Surface((ancho, alto))
    rect_surf.set_alpha(alpha)
    rect_surf.fill(color)
    superficie.blit(rect_surf, (x, y))

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
barra = Barra()
bola = Bola()
todos_los_sprites.add(barra)
todos_los_sprites.add(bola)
bloques = crear_bloques(nivel)
todos_los_sprites.add(bloques)

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                barra.velocidad_x = -10
            if evento.key == pygame.K_RIGHT:
                barra.velocidad_x = 10
            if evento.key == pygame.K_p:
                if estado == JUGANDO:
                    estado = PAUSA
                elif estado == PAUSA:
                    estado = JUGANDO
            if evento.key == pygame.K_RETURN:
                if estado == INICIO:
                    estado = JUGANDO
                elif estado in (PERDIDO, GANADO):
                    estado = INICIO
                    puntuacion = 0
                    vidas = 3
                    nivel = 1
                    velocidad_base = 5
                    todos_los_sprites.empty()
                    barra = Barra()
                    bola = Bola()
                    todos_los_sprites.add(barra)
                    todos_los_sprites.add(bola)
                    bloques = crear_bloques(nivel)
                    todos_los_sprites.add(bloques)
                    puntuaciones = cargar_puntuaciones()
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT and barra.velocidad_x < 0:
                barra.velocidad_x = 0
            if evento.key == pygame.K_RIGHT and barra.velocidad_x > 0:
                barra.velocidad_x = 0
        if evento.type == pygame.MOUSEBUTTONDOWN and estado == INICIO:
            if boton_inicio.collidepoint(evento.pos):
                estado = JUGANDO
            if boton_salir.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN and estado == PAUSA:
            if boton_salir_pausa.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    pantalla.fill(NEGRO)
    if estado == INICIO:
        boton_inicio, boton_salir = dibujar_pantalla_inicio()
    elif estado == JUGANDO:
        todos_los_sprites.update()
        if pygame.sprite.collide_mask(bola, barra):
            bola.velocidad_y *= -1
        bloques_rotos = pygame.sprite.spritecollide(bola, bloques, True)
        if bloques_rotos:
            sonido_romper.play()
            bola.velocidad_y *= -1
            puntuacion += len(bloques_rotos) * 10
            if not bloques:
                nivel += 1
                vidas += 1  # Añadir una vida extra al pasar de nivel
                
                if nivel > 3:  # Si se completa el nivel 3, se gana el juego
                    estado = GANADO
                    puntuaciones.append(puntuacion)
                    puntuaciones.sort(reverse=True)
                    puntuaciones = puntuaciones[:5]  # Mantener solo las 5 mejores puntuaciones
                    guardar_puntuaciones(puntuaciones)
                else:
                    bloques = crear_bloques(nivel)
                    todos_los_sprites.add(bloques)
                    velocidad_base += incremento_velocidad
                    bola.rect.x = ANCHO // 2 - bola.rect.width // 2
                    bola.rect.y = 10 + (5 + nivel) * 35 + 10  # Posicionar la bola debajo de los bloques
                    bola.velocidad_x = velocidad_base if bola.velocidad_x > 0 else -velocidad_base
                    bola.velocidad_y = -velocidad_base
        if bola.rect.bottom >= ALTO:
            vidas -= 1
            sonido_perder.play()
            if vidas == 0:
                estado = PERDIDO
                puntuaciones.append(puntuacion)
                puntuaciones.sort(reverse=True)
                puntuaciones = puntuaciones[:5]  # Mantener solo las 5 mejores puntuaciones
                guardar_puntuaciones(puntuaciones)
            else:
                bola.rect.x = ANCHO // 2 - bola.rect.width // 2
                bola.rect.y = ALTO // 2 - bola.rect.height // 2
                bola.velocidad_x = velocidad_base
                bola.velocidad_y = -velocidad_base
        todos_los_sprites.draw(pantalla)
        
        # Dibujar fondo semitransparente para los textos
        dibujar_rectangulo_transparente(pantalla, NEGRO, 0, 0, 150, 40, 128)
        dibujar_rectangulo_transparente(pantalla, NEGRO, ANCHO - 150, 0, 150, 40, 128)
        dibujar_rectangulo_transparente(pantalla, NEGRO, ANCHO // 2 - 60, 0, 120, 40, 128)
        
        # Dibujar los textos
        texto_puntuacion = fuente_pequena.render(f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntuacion, (5, 5))
        
        texto_vidas = fuente_pequena.render(f"Vidas: {vidas}", True, BLANCO)
        pantalla.blit(texto_vidas, (ANCHO - 145, 5))
        
        texto_nivel = fuente_pequena.render(f"Nivel: {nivel}", True, BLANCO)
        pantalla.blit(texto_nivel, (ANCHO // 2 - 40, 5))
    elif estado == PAUSA:
        boton_salir_pausa = dibujar_pantalla_pausa()
    elif estado in (PERDIDO, GANADO):
        dibujar_pantalla_fin(estado == GANADO)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)
