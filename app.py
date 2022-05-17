# Librerias
import pygame, sys
import stars_animation as _stars
import player as _player
# Constantes
WIDTH, HEIGHT = 800, 600
TITLE = "Dark Enemy (The Game)"

# Configuracion de pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Creamos al jugador y lo posicionamos en el centro de la ventana
player = _player.Player(WIDTH/2, HEIGHT/2)

# Creamos el mapa de estrellas (background)
stars = _stars.Stars(60, WIDTH, HEIGHT)

# Juego
while True:

    for event in pygame.event.get():

        # Evento de Salida (Cerrar el juego)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left_pressed = False
            if event.key == pygame.K_d:
                player.right_pressed = False
            if event.key == pygame.K_w:
                player.up_pressed = False
            if event.key == pygame.K_s:
                player.down_pressed = False
        
    # Zona de Dibujo
    screen.fill((25, 25, 25))  
    stars.draw_stars(screen)
    player.draw_player(screen)
    #pygame.draw.rect(screen, (225,225,225), (10,10, 12,20))

    # Actualizar
    player.update(WIDTH, HEIGHT)         # Actulizar la posicion del jugador
    pygame.display.flip()   # Actualizar la pantalla

    clock.tick(80)          # 80 FPS