#import pygame
#import random

from random import randint
from pygame import draw


class Stars():
    def __init__(self, num_stars, width, height):
        self.color = (101, 101, 101)    # Color gris
        self.radio = 2
        self.speed = 0.4
        self.win_width = width
        self.win_height = height

        # Generando mapa de estrellas
        self.stars_list = []
        for star in range(num_stars):
            #pos_x = random.randint(0, width)
            #pos_y = random.randint(0, height)
            pos_x = randint(0, width)
            pos_y = randint(0, height)
            self.stars_list.append([pos_x, pos_y])


    def draw_stars(self, screen):
        for star in self.stars_list:
            #pygame.draw.circle(screen, self.color, star, self.radio)
            draw.circle(screen, self.color, star, self.radio)
            star[0] += self.speed
            star[1] += self.speed

            if star[0] > self.win_width:
                star[0] = 0
            if star[1] > self.win_height:
                star[1] = 0    