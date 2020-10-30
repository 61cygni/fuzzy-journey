# 
# Displays a picture of smiling indian soldiers, and then overlays with
# moving circles that expose a picture below of a pile of bodies.
#
# Unfortunately, the currently implementation is pretty slow limiting
# the size of the circles and the number that can move around. This is
# largely due to the alpha channel. 
#
#
import pygame
import math
import time
import random

from pygame import mixer
from pygame import gfxdraw


# 2D Gauss function from https://en.wikipedia.org/wiki/Gaussian_function#Two-dimensional_Gaussian_function
# A - Amplitude
# xo, yo - the center
# sigx, sigy - x and y spreads of the blob

def my_gauss2d(x, y, A, xo, yo, sigx, sigy): 
  x_num = math.pow((x - xo), 2)
  y_num = math.pow((y - yo), 2)
  x_den = 2 * math.pow(sigx, 2)
  y_den = 2 * math.pow(sigy, 2)
  return A * math.exp(- ( (x_num / x_den) + (y_num / y_den) ) ) 

def create_puff(width, height):
  puff = pygame.Surface((width, height))

  xo = width / 2
  yo = height / 2

  sigx = width / 6
  sigy = height / 6

  for x in range(0, width):
    for y in range(0, height):
      opacity = my_gauss2d(x, y, 2, xo, yo, sigx, sigy)
      alpha = (255*opacity)
      if alpha > 255 : 
        alpha = 255

      puff.set_at((x, y), (255, 255, 255, alpha))

  return puff

class Puff:
    """A Gaussian Puff"""

    def __init__(self, width, height, surface):

      self.w = width
      self.h = height

      self.xinc = random.choice([  -3,  3 ]) 
      self.yinc = random.choice([  -3,  3 ]) 

      self.surface = surface

      self.puff = create_puff(self.w, self.h)

      self.init_pos()


    def init_pos(self):
      self.x = int((self.surface.get_width () - self.w) * random.random())
      self.y = int((self.surface.get_height() - self.h) * random.random())

    def move_pos(self):

        if self.x + 3 >= (self.surface.get_width() - self.w):
            self.xinc = -3 

        if self.x <= 3:
            self.xinc =  3 
            self.x = 3

        if self.y + 3 >= (self.surface.get_height() - self.h):
            self.yinc = -3 

        if self.y <= 3:
            self.yinc = 3 
            self.y = 3 

        self.x += self.xinc
        self.y += self.yinc

        #print("POS %d %d" % (self.x, self.y))

def create_background(width, height):
    image = pygame.image.load("indiantroops.jpg")

    background = pygame.Surface((width, height))
    background.blit(image, (0,0))

    return background


def is_trying_to_quit(event):
        pressed_keys = pygame.key.get_pressed()
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        x_button = event.type == pygame.QUIT
        altF4 = alt_pressed and event.type == pygame.KEYDOWN and event.key == pygame.K_F4
        escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        return x_button or altF4 or escape

  
def do_gauss_demo(surface, darkbg, puff):

        subsurface = darkbg.subsurface(puff.x, puff.y, puff.w, puff.h)

        for x in range(0, puff.w):
            for y in range(0, puff.h):
                alpha = puff.puff.get_at((x,y))[3]
                pixel = subsurface.get_at((x,y))
                pixel[3] = alpha 
                subsurface.set_at((x,y), pixel)

        surface.blit(subsurface, (puff.x, puff.y))               


def run_demos(width, height, fps):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        background = create_background(width, height)
        clock = pygame.time.Clock()

        music_bool = True

        puffs = []
        locs  = []

        mixer.init()
        mixer.music.load("LoFi-loop.mp3")
        mixer.music.set_volume(0.0)

        # generate initial puff list

        for i in range(0,4):
            #size = int(random.random()*200) + 200 
            size = 250 
            puffs.append(Puff(size, size, screen))

        random.shuffle(puffs)    

        # Start playing the song
        mixer.music.play()

        darkbg = pygame.image.load("bodies.jpg")
        darkbg = darkbg.convert_alpha()

        while True:
                for event in pygame.event.get():
                        if is_trying_to_quit(event):
                            return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                            music_bool = not music_bool 
                            if not music_bool:
                                mixer.music.set_volume(0.0)
                            else:
                                mixer.music.set_volume(0.4)
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                            size = int(random.random()*200) 
                            puffs.append(Puff(size, size, screen))
                            size = int(random.random()*20) 
                            puffs.append(Puff(size, size, screen))
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            puffs.pop(0)
                            
                screen.blit(background, (0, 0))
                for puff in puffs:
                    do_gauss_demo(screen, darkbg, puff)
                    puff.move_pos()
                pygame.display.flip()
                clock.tick(fps)

run_demos(800, 550, 20)
