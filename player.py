from pygame import Rect, draw

# Clase Jugador
class Player:
    def __init__(self, pos_x, pos_y):
        self.size = 70
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        # self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size, self.size)
        self.rect = Rect(self.pos_x, self.pos_y, self.size, self.size)
        self.color = (250, 120, 60)
        self.vel_x = 0
        self.vel_y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
    
    def draw_player(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect)
        draw.rect(screen, self.color, self.rect)
    
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

        """ 
        # Jugador Encarcelado
        if self.pos_x <= 0:
            self.pos_x = 1
        if self.pos_x >= (width - self.size):
            self.pos_x = (width - self.size) - 1
        if self.pos_y <= 0:
            self.pos_y = 1
        if self.pos_y >= (height - self.size):
            self.pos_y = (height - self.size) - 1
        """

        # Teletransportar jugador
        if self.pos_x <= 0:
            self.pos_x = (width - self.size) - 1
        if self.pos_x >= (width - self.size):
            self.pos_x = 1
        if self.pos_y <= 0:
            self.pos_y = (height - self.size) - 1
        if self.pos_y >= (height - self.size):
            self.pos_y = 1
        
        # self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), self.size, self.size)
        self.rect = Rect(int(self.pos_x), int(self.pos_y), self.size, self.size)