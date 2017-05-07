#!/usr/bin/env python

# fix color of ball so no transparency
# create a scoreboard class with a rectangle so score can be cleared between each update
# scoreboard: http://cs.iupui.edu/~aharris/pygame/ch07/mpScore.py
# https://peak5390.wordpress.com/2013/01/21/balloon-ninja-adding-a-scoreboard/

import os, pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

size = width, height = 440, 440
speed = [1, 1]
white = 255, 255, 255
going = True

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

class Fist(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/fist.bmp', -1)
        self.punching = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        self.punching = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/ball.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = speed
        self.dizzy = 0

    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._fall()

    def _fall(self):
        global going
        newpos = self.rect.move(self.move)
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            speed[0] = -speed[0]
            newpos = self.rect.move(speed)
            self.image = pygame.transform.flip(self.image, 1, 0)
        if self.rect.top < self.area.top:
            speed[1] = -speed[1]
            newpos = self.rect.move(speed)
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos
        if self.rect.bottom > self.area.bottom:
            going = False

    def _spin(self):
        center = self.rect.center
        self.dizzy = self.dizzy + 72
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        newpos = self.rect.move(self.move)
        speed[1] = -speed[1] - 1
        newpos = self.rect.move(speed)
        self.image = pygame.transform.flip(self.image, 1, 0)
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

#class Scoreboard(pygame.sprite.Sprite):
#    def __init__(self):
#        pygame.sprite.Sprite.__init__(self)
        #self.score = 0
        #self.font = pygame.font.SysFont("None", 20)

#    def update(self):
#        self.text = "Score: %d" % (self.score)
#        self.image = self.font.render(self.text, 1, (255, 255, 0))
#        self.rect = self.image.get_rect()


def main():
    pygame.init()

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Volley ball')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(size)
    background = background.convert()
    background.fill(white)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    punch_sound = load_sound('sounds/spring.wav')
    ball = Ball()
    fist = Fist()
    #scoreboard = Scoreboard()
    #allsprites = pygame.sprite.RenderPlain((fist, ball, scoreboard))
    allsprites = pygame.sprite.RenderPlain((fist, ball))

    font = pygame.font.Font(None, 36)
    score = 0

    global going
    while going:
        clock.tick(60)

        #font = pygame.font.Font(None, 36)
        #text = font.render("Score {0}".format(score), 1, (10,10,10))
        #textpos = text.get_rect(centerx = background.get_width()/2)
        #background.blit(text, textpos)

        for event in pygame.event.get():
            if event.type != NOEVENT:
               print(event)
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_q:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(ball):
                    punch_sound.play()
                    ball.punched()
                    #scoreboard.score += 1
                    score += 1
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()
            #text = font.render("Score {0}".format(score-1), 1, (255,255,255))
            #textpos = text.get_rect(centerx = background.get_width()/2)
            #background.blit(text, textpos)

            #text = font.render("Score {0}".format(score), 1, (0,0,0))
            #textpos = text.get_rect(centerx = background.get_width()/2)
            #background.blit(text, textpos)

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
