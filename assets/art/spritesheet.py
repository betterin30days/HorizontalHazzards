import pygame

class Spritesheet(object):
    sheet = None
    frames = None
    row = None
    width = 0
    height = 0
    animations = None
    def __init__(self, filename, frames, row, width, height, colorkey = None):
        self.animations = []
        self.sheet = pygame.image.load(filename).convert()
        self.frames = frames
        self.row = row - 1
        self.width = width
        self.height = height
        for frame, image in enumerate(range(0,self.frames)):
            self.animations.append(self.image_at(
                (frame*self.width, self.row*self.height, self.width, self.height),
                colorkey))

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