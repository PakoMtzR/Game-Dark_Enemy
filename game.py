# Librerias
# ------------------------------------------------------- #
import pygame
from random import randint
from pyvideoplayer import Video
from network import Network
# ------------------------------------------------------- #

# Constantes
# ------------------------------------------------------- #
WIDTH, HEIGHT = 1000, 700
TITLE = "Dark Enemy (The Game)"
FPS = 80
# ------------------------------------------------------- #

# Lista de Colores
# ------------------------------------------------------- #
BLACK = (25, 25, 25)
ORANGE = (250, 120, 60)
GRAY = (101, 101, 101)
GREEN = (0, 225, 0)
RED = (239, 83, 80)
WHITE = (225, 225, 225)
# ------------------------------------------------------- #

# Configuracion Inicial
# ------------------------------------------------------- #
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill(BLACK)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
# ------------------------------------------------------- #

# Cargar Elementos Audiovisuales
# ------------------------------------------------------- #
# Cargando sonidos...
laser_sound = pygame.mixer.Sound("sounds/laser_sound1.ogg")
laser_hit_sound = pygame.mixer.Sound("sounds/laser_hit.ogg")
explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")

# Cargando video de la intro
video = Video("video/intro.mp4")
video.set_size((WIDTH, HEIGHT))

# Animacion Explosion
explosion_group = pygame.sprite.Group()
# ------------------------------------------------------- #

# Background - Mapa de Estrellas - Marcador de vidas 
# ------------------------------------------------------- #
# Generando mapa de estrellas
stars_list = []
num_stars = 60
star_radio = 2
star_speed = 0.4
for star in range(num_stars):
    pos_x = randint(0, WIDTH)
    pos_y = randint(0, HEIGHT)
    stars_list.append([pos_x, pos_y])

# Funcion para dibujar texto en la pantalla
def draw_text(surface, text, size, pos_x, pos_y, color):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (pos_x, pos_y)
    surface.blit(text_surface, text_rect)

# Pantalla de inicio
def show_go_screen(msg):
    if msg == "intro":
        draw_text(SCREEN, "Dark Enemy >:D", 60, WIDTH//2, HEIGHT//4, WHITE)
    if msg == "win":
        draw_text(SCREEN, "YOU WON!", 60, WIDTH//2, HEIGHT//4, GREEN)
    if msg == "lost":
        draw_text(SCREEN, "YOU LOST!", 60, WIDTH//2, HEIGHT//4, RED)    
    
    draw_text(SCREEN, "Press R for a New Match", 30, WIDTH//2, HEIGHT//2, WHITE)

    pygame.display.flip()
    waiting = True
    run_game = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return not run_game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return run_game

# Background
def draw_background(player):  # Dibuja las estrellas en la pantalla
    SCREEN.fill(BLACK)
    for star in stars_list:
        pygame.draw.circle(SCREEN, GRAY, star, star_radio)
        star[0] += star_speed
        star[1] += star_speed

        if star[0] > WIDTH: star[0] = 0
        if star[1] > HEIGHT: star[1] = 0 

    # Dibuja las vidas que tiene el jugador
    draw_text(SCREEN, "Health: " + str(player.health), 30, 60, 5, WHITE)
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
    
    def __del__(self):
        print("jugador eliminado")

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

# Programacion de la explosion
# ------------------------------------------------------- #
class Explosion(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1,6):
			img = pygame.image.load(f"img/exp{num}.png")
			img = pygame.transform.scale(img, (scale, scale))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()
# ------------------------------------------------------- #

# Programacion de los Laseres
# ------------------------------------------------------- #
my_lasers = []
enemy_lasers = []
max_lasers = 3

class Laser():
    def __init__(self):
        self.size_x = 10
        self.size_y = 30
        self.color = GREEN
        self.speed = 9
        self.direction = -1     # (-1 se mueve de abajo-arriba) (1 de arriba-abajo)
        self.pos_x = 0
        self.pos_y = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        # laser_sound.play()

    def update_position(self):
        self.pos_y += self.speed * self.direction
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size_x, self.size_y)


def draw_lasers(player:object, network:object):

    # Laseres del jugador
    for laser in my_lasers:
        laser.update_position()
        pygame.draw.rect(SCREEN, laser.color, laser.rect)

        # Si el laser se sale de la pantalla, se envia datos al servidor
        # y se elimina el laser de la lista
        if laser.pos_y < -laser.size_y:
            # SEND POSITION LASER TO SERVER
            laser_pos_x_send = WIDTH - laser.pos_x - laser.size_x
            # ------------------------- Temporal -------------------------
            network.send(str(int(laser_pos_x_send)))

            # print('pos_x:', laser.pos_x, 'sending ->', laser_pos_x_send)
            #laser_enemy = Laser()
            #laser_enemy.pos_x = laser_pos_x_send
            #laser_enemy.pos_y = 0
            #enemy_lasers.append(laser_enemy)
            # ------------------------- Temporal -------------------------
            my_lasers.remove(laser)
    
    # Laseres del enemigo
    for laser in enemy_lasers:
        laser.direction = 1     # Los laseres se mueven de arriba-abajo
        laser.color = RED       # Cambiamos el color del laser a rojo para diferenciarlos de los nuestros
        laser.update_position()
        pygame.draw.rect(SCREEN, laser.color, laser.rect)

        # Si el laser choca con el jugador, pierde una vida y eliminamos el laser de la lista
        if ((laser.pos_y + laser.size_y >= player.pos_y) and (laser.pos_y + laser.size_y <= player.pos_y + player.size)) and ((laser.pos_x >= player.pos_x) and (laser.pos_x - laser.size_x <= player.pos_x + player.size)):
            
            player.health -= 1  # Bajar vida

            # Animacion de explosion
            if player.health > 0:
                laser_hit_sound.play()
                explosion = Explosion(player.pos_x + player.size//2, player.pos_y, 50)
                explosion_group.add(explosion)
            else:
                explosion_sound.play()
                explosion = Explosion(player.pos_x + player.size//2, player.pos_y, 300)
                explosion_group.add(explosion)

            enemy_lasers.remove(laser)  # Remover laser enemigo de memoria
            # print('Health:', player.health)

        # Si el laser sale de la pantalla, se elimina de la lista
        if laser.pos_y > HEIGHT:
            enemy_lasers.remove(laser)
# ------------------------------------------------------- #

# --------------------------------------------------------------------------------- #    
# Intro
def intro():
    run_intro = True

    while run_intro:
        video.draw(SCREEN, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                video.close()
                main_game()

            if event.type == pygame.QUIT:
                run_intro = False
        
    pygame.quit()   # Cerrar Juego            

# --------------------------------------------------------------------------------- #    
# Juego
def main_game():
    network = Network()

    game_over = True
    run_game = True
    player = Player(ORANGE)
    show = "intro"
    

    while run_game:
        if game_over:
            game_over = False

            # Limpiamos los elementos del juego
            del player
            player = Player(ORANGE)
            my_lasers.clear()
            enemy_lasers.clear()

            if show == "lost":
                run_game = show_go_screen("lost")
            if show == "win":
                run_game = show_go_screen("win")
            if show == "intro":
                run_game = show_go_screen("intro")

        # Eventos
        for event in pygame.event.get():
            # Evento de Salida (Cerrar el juego)
            if event.type == pygame.QUIT:
                run_game = False
            
            # Eventos de Teclado, movimiento del jugador y disparos
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
        
        # Si el jugador pierde todas sus vidas, se termina el juego
        if player.health == 0:
            game_over = True
            show = "lost"
            network.send("dead")

        # Actualiza la pantalla (Dibuja todos los elementos del juego)
        draw_background(player)

        status = network.update()

        # Si gana se acaba el juego
        if status[0] == "win":
            game_over = True
            show = "win"
        else:
            new_laser_pos_x = int(status[1])
            if new_laser_pos_x < -1:
                pass
            else:
                laser_enemy = Laser()
                laser_enemy.pos_x = new_laser_pos_x
                laser_enemy.pos_y = 0
                enemy_lasers.append(laser_enemy)

        draw_lasers(player, network)
        player.update_position()
        player.draw_player()
        explosion_group.draw(SCREEN)
        explosion_group.update()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()   # Cerrar Juego


if __name__ == "__main__":
    intro()