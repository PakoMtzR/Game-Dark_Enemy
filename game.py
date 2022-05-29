# Librerias
# ------------------------------------------------------- #
import pygame
from random import randint
# ------------------------------------------------------- #

# Constantes
# ------------------------------------------------------- #
WIDTH, HEIGHT = 1000, 700
TITLE = "Dark Enemy (The Game)"
FPS = 80
# ------------------------------------------------------- #

# Configuracion Inicial
# ------------------------------------------------------- #
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
# ------------------------------------------------------- #

# Lista de Colores
# ------------------------------------------------------- #
BLACK = (25, 25, 25)
ORANGE = (250, 120, 60)
GRAY = (101, 101, 101)
GREEN = (0, 225, 0)
RED = (239, 83, 80)
# ------------------------------------------------------- #

# Generando mapa de estrellas
# ------------------------------------------------------- #
stars_list = []
num_stars = 60
star_radio = 2
star_speed = 0.4
for star in range(num_stars):
    pos_x = randint(0, WIDTH)
    pos_y = randint(0, HEIGHT)
    stars_list.append([pos_x, pos_y])

def draw_background():  # Dibuja las estrellas en la pantalla
    SCREEN.fill(BLACK)
    for star in stars_list:
        pygame.draw.circle(SCREEN, GRAY, star, star_radio)
        star[0] += star_speed
        star[1] += star_speed

        if star[0] > WIDTH: star[0] = 0
        if star[1] > HEIGHT: star[1] = 0 
# ------------------------------------------------------- #

# Programacion del Jugador
# ------------------------------------------------------- #
class Player:
    def __init__(self, color):
        self.size = 70
        self.health = 5
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size, self.size)
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
    
    def draw_player(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
    
    def update_position(self):
        self.vel_x = 0
        self.vel_y = 0

        # Verificamos si no estan presionando dos teclas al mismo tiempo
        if self.left_pressed and not self.right_pressed:
            self.vel_x = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel_x = self.speed
        if self.up_pressed and not self.down_pressed:
            self.vel_y = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.vel_y = self.speed

        # Actualizamos la nueva posicion del jugador
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        
        # Jugador Encarcelado
        # Condiciones para que el jugador no salga de la pantalla
        if self.pos_x < 0:
            self.pos_x = 0
        if self.pos_x > (WIDTH - self.size):
            self.pos_x = (WIDTH - self.size)
        if self.pos_y < 0:
            self.pos_y = 0
        if self.pos_y > (HEIGHT - self.size):
            self.pos_y = (HEIGHT - self.size)

        # Generamos el jugador con las nuevas posiciones
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size, self.size)
# ------------------------------------------------------- #

# Programacion de los Laseres
# ------------------------------------------------------- #
laser_sound = pygame.mixer.Sound("sounds/laser_sound1.ogg")
my_lasers = []
enemy_lasers = []
max_lasers = 3

class Laser():
    def __init__(self):
        self.size_x = 10
        self.size_y = 30
        self.color = GREEN
        self.speed = 9
        self.pos_x = 0
        self.pos_y = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
    
    def update_position(self):
        self.pos_y -= self.speed
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size_x, self.size_y)


def draw_lasers(player):

    # Laseres del jugador
    for laser in my_lasers:
        laser.update_position()
        pygame.draw.rect(SCREEN, laser.color, laser.rect)

        # Si el laser se sale de la pantalla, se envia datos al servidor
        # y se elimina el laser de la lista
        if laser.pos_y < -laser.size_y:
            # SEND POSITION LASER TO SERVER
            print('pos_x:', laser.pos_x)
            my_lasers.remove(laser)
    
    # Laseres del enemigo
    for laser in enemy_lasers:
        laser.speed *= -1       # Los laseres se mueven de arriba-abajo
        laser.color = RED       # Cambiamos el color del laser a rojo para diferenciarlos de los nuestros
        laser.update_position()
        pygame.draw.rect(SCREEN, laser.color, laser.rect)

        # Si el laser choca con el jugador, pierde una vida y eliminamos el laser de la lista
        if ((laser.pos_y + laser.size_y >= player.pox_y) and (laser.pos_y + laser.size_y <= player.pos_y + player.size)) and ((laser.pos_x >= player.pos_x) and (laser.pos_x - laser.size_x <= player.pos_x + player.size)):
            player.health -= 1
            enemy_lasers.remove(laser)
            print(player.health)

        # Si el laser sale de la pantalla, se elimina de la lista
        if laser.pos_y > HEIGHT:
            #print('pos_x:', laser.pos_x)
            enemy_lasers.remove(laser)

# ------------------------------------------------------- #


# --------------------------------------------------------------------------------- #    
# Juego
def main_game():
    player = Player(ORANGE)
    
    run_game = True
    while run_game:   
        
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            # Evento de Salida (Cerrar el juego)
            if event.type == pygame.QUIT:
                run_game = False
            
            # Eventos de Teclado, movimiento del jugador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.left_pressed = True
                if event.key == pygame.K_d:
                    player.right_pressed = True
                if event.key == pygame.K_w:
                    player.up_pressed = True
                if event.key == pygame.K_s:
                    player.down_pressed = True
                if event.key == pygame.K_SPACE:
                    if len(my_lasers) < max_lasers:
                        laser = Laser()
                        laser.pos_x = player.pos_x + player.size/2 - laser.size_x/2
                        laser.pos_y = player.pos_y
                        my_lasers.append(laser)
                        laser_sound.play()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.left_pressed = False
                if event.key == pygame.K_d:
                    player.right_pressed = False
                if event.key == pygame.K_w:
                    player.up_pressed = False
                if event.key == pygame.K_s:
                    player.down_pressed = False
        
        # Actualiza la pantalla (Dibuja todos los elementos del juego)
        draw_background()
        draw_lasers(player)
        player.draw_player()
        player.update_position()
        pygame.display.flip()
        
    pygame.quit()   # Cerrar Juego


if __name__ == "__main__":
    main_game()