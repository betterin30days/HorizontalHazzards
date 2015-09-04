import pygame

class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, colorkey = None):
        '''Load image from x, y, x offset, y offset'''
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        if colorkey is not None:
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rectangles, colorkey = None):
        '''Load multiple images into a list, supply a list of rectangles'''
        return [self.image_at(rect, colorkey) for rect in rectangles]