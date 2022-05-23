# Librerias
import pygame

# Constantes
WIDTH, HEIGHT = 1000, 700
TITLE = "Dark Enemy (The Game)"
FPS = 80

# Configuracion de pygame
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Colores
BLACK = (25, 25, 25)
ORANGE = (250, 120, 60)

# Clase Jugador
class Player:
    def __init__(self, color):
        self.size = 70
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
    
    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self, width, height):
        self.vel_x = 0
        self.vel_y = 0

        if self.left_pressed and not self.right_pressed:
            self.vel_x = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel_x = self.speed
        if self.up_pressed and not self.down_pressed:
            self.vel_y = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.vel_y = self.speed

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        
        # Jugador Encarcelado
        if self.pos_x < 0:
            self.pos_x = 0
        if self.pos_x > (width - self.size):
            self.pos_x = (width - self.size)
        if self.pos_y < 0:
            self.pos_y = 0
        if self.pos_y > (height - self.size):
            self.pos_y = (height - self.size)

        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size, self.size)


def draw_window(player):
    SCREEN.fill(BLACK)
    player.draw_player(SCREEN)
    pygame.display.update()


# Juego
def main():
    run_game = True
    player = Player(ORANGE)

    while run_game:
        
        clock.tick(FPS)     # Correr juego a # FPS

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
                '''
                if event.key == pygame.K_SPACE:
                    laser = _laser.Laser()
                    laser.pos_x = player.pos_x + player.size/2 - laser.size_x/2
                    laser.pos_y = player.pos_y
                    laser_list.append(laser)
                    laser_sound.play()
                '''
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.left_pressed = False
                if event.key == pygame.K_d:
                    player.right_pressed = False
                if event.key == pygame.K_w:
                    player.up_pressed = False
                if event.key == pygame.K_s:
                    player.down_pressed = False
        
        draw_window(player)

    pygame.quit()


if __name__ == "__main__":
    main()