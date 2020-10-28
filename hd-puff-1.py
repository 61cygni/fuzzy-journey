# Experiment with high resolution 
import pygame
import math
import time
import random

# 2D Guass funxction from https://en.wikipedia.org/wiki/Gaussian_function#Two-dimensional_Gaussian_function
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
      opacity = my_gauss2d(x, y, 1, xo, yo, sigx, sigy)
      alpha = (255*opacity)

      puff.set_at((x, y), (255, 255, 255, alpha))

  return puff

class Puff:
    """A Gaussian Puff"""

    def __init__(self, width, height, surface):

      self.w = width
      self.h = height

      self.xinc = random.choice([ -2, -1, -1, 1,  1, 2]) 
      self.yinc = random.choice([ -2, -1, -1, 1,  1, 2]) 

      self.surface = surface

      self.puff = create_puff(self.w, self.h)

      self.init_pos()


    def init_pos(self):
      self.x = int(self.surface.get_width () * random.random())
      self.y = int(self.surface.get_height() * random.random())

    def move_pos(self):
        if self.x >= (self.surface.get_width() - self.w):
            self.xinc *= -1 
        elif self.x <= 0:
            self.xinc *= -1 

        if self.y >= (self.surface.get_height() - self.h):
            self.yinc *= -1 
        elif self.y <= 0:
            self.yinc *= -1 

        self.x += self.xinc
        self.y += self.yinc

        #print ("%d %d" % (self.x, self.y))


def my_gauss(a, b, c, x):
  return a * math.exp(- (math.pow((x-b), 2) / (2 * math.pow(c, 2))))


def create_background(width, height):
  start_color = pygame.Color(0, 0, 0)
  end_color   = pygame.Color(255, 0, 0)

  background = pygame.Surface((width, height))

  for y in range(0, height):
    for x in range(0, width):
      plot_color = start_color.lerp(end_color, x/width)
      background.set_at((x, y), plot_color)

  return background


def is_trying_to_quit(event):
        pressed_keys = pygame.key.get_pressed()
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        x_button = event.type == pygame.QUIT
        altF4 = alt_pressed and event.type == pygame.KEYDOWN and event.key == pygame.K_F4
        escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        return x_button or altF4 or escape

  
def do_gauss_demo(surface, puff):
        
        # Draw a rectangle
        surface.blit(puff.puff, (puff.x, puff.y))


def run_demos(width, height, fps):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        background = create_background(width, height)
        clock = pygame.time.Clock()

        puffs = []
        locs  = []

        for i in range(0,100):
            size = int(random.random()*200) 
            puffs.append(Puff(size, size, screen))

        for i in range(0,100):
            size = int(random.random()*20) 
            puffs.append(Puff(size, size, screen))

        while True:
                for event in pygame.event.get():
                        if is_trying_to_quit(event):
                                return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                demos = demos[1:]
                screen.blit(background, (0, 0))
                for puff in puffs:
                    do_gauss_demo(screen, puff)
                    puff.move_pos()
                pygame.display.flip()
                clock.tick(fps)

run_demos(1200, 768, 60)
