
from pygame import Rect, draw

class Laser():
    def __init__(self):
        self.size_x = 10
        self.size_y = 30
        self.color = (0, 225, 0)
        self.speed = 9
        self.pos_x = 0
        self.pos_y = 0
        self.rect = Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
    
    def draw_laser(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect)
        self.rect = Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        draw.rect(screen, self.color, self.rect)
    
    def update(self):
        self.pos_y -= self.speed
        self.rect = Rect(int(self.pos_x), int(self.pos_y), self.size_x, self.size_y)
