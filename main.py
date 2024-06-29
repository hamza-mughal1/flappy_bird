import pygame
import random
import sys

pygame.init()



class Bird:
    def __init__(self, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.x = win_width//2
        self.y = win_height//2
        self.width = 20
        self.height = 20
        self.velocity = 0
        self.acceleration = -FPS/100000
        self.color = (255,0,0)

    def draw(self, win):
        if self.y >= self.win_height or self.y < 0:
            return True
        self.y -= self.velocity
        self.velocity += self.acceleration
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def jump(self):
        self.velocity = FPS/800




class Pipe:
    def __init__(self, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.width = 100
        self.color = (0,255,0)
        self.pipes = []
        self.speed = 0.5
        self.gap = 200
        self.variants = [(self.win_height/4,(self.win_height/4)+self.gap),
                         (self.win_height/2,(self.win_height/2)+self.gap),
                         ((self.win_height/2)+(self.win_height/8),(self.win_height/2)+(self.win_height/8)+self.gap),
                         ((self.win_height/2)+(self.win_height/4),(self.win_height/2)+(self.win_height/4)+self.gap)]
        self.score = 0
        self.score_increase = True
        self.pipe_number = 0 

    def draw_pipe(self, win, bird):
        variant = self.variants[random.randint(0,3)]
        if len(self.pipes) == 0:
            self.pipes.append([self.win_width, 0, self.width, variant[0], variant[1]])
            self.pipe_number += 1
        elif (self.win_width - self.pipes[-1][0]) > self.width * 3:
            self.pipes.append([self.win_width, 0, self.width, variant[0], variant[1]])
            self.score_increase = True
            self.pipe_number += 1
            

        for i in self.pipes:
            rect1 = pygame.Rect(i[0], i[1], i[2], i[3])
            rect2 = pygame.Rect(i[0], i[4], i[2], self.win_height)
            rect3 =  pygame.Rect(bird.x, bird.y, bird.width, bird.height)
            if rect1.colliderect(rect3) or rect2.colliderect(rect3):
                return True
            pygame.draw.rect(win, self.color,rect1)
            pygame.draw.rect(win, self.color,rect2)
            i[0] -= self.speed

        if self.pipes[0][0] < -(self.width+10):
            self.pipes.pop(0)

        if (self.pipe_number>=3) and self.score_increase:
            self.score += 1
            self.score_increase = False

    def draw_score(self, win):
        font = pygame.font.Font(None, 26)
        text_surface = font.render(str(self.score), True, (255,0,0))
        win.blit(text_surface, (self.win_width//2, 50))

def ending(score, width, height, win):
    font = pygame.font.Font(None, 100)
    text_surface = font.render(str(score), True, (255,0,0))
    while True:
        win.fill((255,255,255))
        win.blit(text_surface, ((width//2)-50, (height//2)-50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
                
        pygame.display.update()



width, height = 1100, 900
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("flappy bird")
clock = pygame.time.Clock()
FPS = 1000

bird = Bird(width, height)
pipes = Pipe(width, height)

run = True
end = False
while run:
    clock.tick(FPS)
    win.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    
    if bird.draw(win) or pipes.draw_pipe(win, bird) :
        run = False
        end = True
    pipes.draw_score(win)

    pygame.display.update()

if end:
    ending(pipes.score, width, height, win)

pygame.quit()