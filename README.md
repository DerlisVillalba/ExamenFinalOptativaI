## Ani Ho'a Pelota

Ani Ho'a Pelota es un juego desarrollado en Python utilizando la biblioteca Pygame. El objetivo del juego es romper bloques con una pelota controlada por una barra.

## Requisitos

- Python 3.x
- Pygame

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/ani-hoa-pelota.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd ani-hoa-pelota
    ```
3. Instala las dependencias:
    ```bash
    pip install pygame
    ```

## Ejecución

Para ejecutar el juego, simplemente ejecuta el archivo principal:
```bash
python main.py
```

## Controles del Juego

- Mueve la barra con las flechas izquierda y derecha del teclado.
- Presiona "ENTER" para iniciar el juego desde la pantalla de inicio.
- Presiona "ESPACIO" para pausar el juego.
- Presiona "ENTER" para reiniciar el juego cuando pierdes o ganas.

## Estructura del Código

### Importación de Bibliotecas

```python
import pygame
import sys
import random
import pickle
```

### Inicialización y Configuración

```python
pygame.init()
ANCHO, ALTO = 800, 600
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
GRADIENTE_INICIAL = [(0, 0, 255), (0, 255, 255)]
```

### Configuración de la Pantalla y Recursos

```python
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ani Ho'a Pelota")
```

### Fuentes y Sonidos

```python
fuente_grande = pygame.font.SysFont("Arial", 60)
fuente_pequena = pygame.font.SysFont("Arial", 36)

sonido_pelota = pygame.mixer.Sound("pelota.wav")
sonido_perder = pygame.mixer.Sound("perder.wav")
sonido_romper = pygame.mixer.Sound("romper.mp3")
pygame.mixer.music.load("musica_fondo.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
```

### Variables de Estado del Juego

```python
INICIO = 0
JUGANDO = 1
PAUSA = 2
PERDIDO = 3
GANADO = 4
estado = INICIO

puntuacion = 0
vidas = 3
nivel = 1
velocidad_base = 5
incremento_velocidad = 1
```

### Clases Principales

#### Clase Barra

```python
class Barra(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(imagen_barra, (150, 30))
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
```

#### Clase Bola

```python
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(imagen_pelota, (25, 25))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
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
```

#### Clase Bloque

```python
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = random.choice(COLORES_BLOQUES)
        self.image = pygame.Surface((75, 30))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
```

## Bucle Principal del Juego

El bucle principal del juego gestiona el estado del juego, actualiza los sprites y gestiona los eventos del usuario.

```python
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if estado == INICIO and evento.key == pygame.K_RETURN:
                estado = JUGANDO
            elif estado == PAUSA and evento.key == pygame.K_SPACE:
                estado = JUGANDO
            elif estado == PERDIDO and evento.key == pygame.K_RETURN:
                estado = INICIO
            elif estado == GANADO and evento.key == pygame.K_RETURN:
                estado = INICIO

    if estado == INICIO:
        boton_inicio, boton_salir = dibujar_pantalla_inicio()
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_inicio.collidepoint(evento.pos):
                    estado = JUGANDO
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
    elif estado == JUGANDO:
        pantalla.fill(NEGRO)
        # Actualizar y dibujar todos los sprites del juego
    elif estado == PAUSA:
        dibujar_pantalla_pausa()
    elif estado == PERDIDO:
        dibujar_pantalla_perdido()
    elif estado == GANADO:
        dibujar_pantalla_ganado()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
```

## Conclusión

El juego "Ani Ho'a Pelota" está estructurado para manejar diferentes estados de juego y actualizar los elementos de la pantalla en consecuencia. La interacción del usuario se gestiona a través de eventos de teclado y ratón, proporcionando una experiencia de juego fluida y reactiva.
