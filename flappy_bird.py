import pygame, sys, math
from random import randrange as randH
from pygame.locals import *

# Start pygame
pygame.init()

# Set up resolution
windowObj = pygame.display.set_mode((640, 480))
fpsTimer = pygame.time.Clock()
maxFPS = 30

# Ground Elevation (pixels)
groundLevel = 400

# Global colors
birdColor = pygame.Color('#222222')
backgroundColor = pygame.Color('#abcdef')
groundColor = pygame.Color('#993333')
fontColor = pygame.Color('#FFFFFF')

fontObj = pygame.font.SysFont("aria",14)


# Class for pipe obstacles
class Pipes:
    height = 0
    width = 60
    gap = 150
    pos = 600
    replaced = False
    scored = False

    # Randomize pipe location
    def __init__(self):
        self.height = randH(210, groundLevel - 10)

    # Moves the pipes along the ground, checks if they're off the screen
    def move(self, movement):
        self.pos += movement
        if (self.pos + self.width < 0):
            return False  # Return false if we moved off the screen
        return True

    # Handles drawing the pipes to the screen
    def draw(self, surface):
        pygame.draw.rect(surface, groundColor, (self.pos, self.height, self.width, groundLevel - self.height))
        pygame.draw.rect(surface, groundColor, (self.pos, 0, self.width, self.height - self.gap))


# Class for the player
class Bird:
    pos = (0, 0)
    radius = 20

    def __init__(self, newPos):
        self.pos = newPos

    # Handles drawing the bird to the screen
    def draw(self, surface):
        intPos = (int(math.floor(self.pos[0])), int(math.floor(self.pos[1])))

        pygame.draw.circle(surface, birdColor, intPos, self.radius)

    # Attempt to move the bird, make sure we aren't hitting the ground
    def move(self, movement):
        posX, posY = self.pos
        movX, movY = movement

        if ((posY + movY + self.radius) < groundLevel):
            self.pos = (posX + movX, posY + movY)
            return True  # Return if we successfuly moved
        self.pos = (posX, groundLevel - self.radius)
        return False

    # Test for collision with the given pipe
    def collision(self, pipe):
        posX, posY = self.pos
        collideWidth = (pipe.pos < posX + self.radius and posX - self.radius < pipe.pos + pipe.width)
        collideTop = (pipe.height - pipe.gap > posY - self.radius)
        collideBottom = (posY + self.radius > pipe.height)
        if (collideWidth and (collideTop or collideBottom)):
            return True
        return False


# Setting up initial values
bird = Bird((windowObj.get_width() / 4, windowObj.get_height() / 2))
pipes = [Pipes()]
gravity = 1
velocity = 0
score = 0
highScore = 0


# Called to reset the game when you lose
def resetGame():
    global score
    global highScore
    if (score > highScore):
        highScore = score
    score = 0
    global velocity
    velocity = 0
    global pipes
    del pipes[:]
    pipes = [Pipes()]
    global bird
    bird.pos = ((windowObj.get_width() / 4, windowObj.get_height() / 2))


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    return


# Main game loop
while True:

    windowObj.fill(backgroundColor)

    # Check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_ESCAPE):
                pause()
            # If the player hits a key, set velocity upward
            velocity = -20

    # Add acceleration from gravity
    velocity += gravity

    if (not bird.move((0, velocity))):
        resetGame()
        velocity = 0
    for pipe in pipes:
        if not pipe.replaced and pipe.pos < windowObj.get_width() / 2:
            pipes[len(pipes):] = [Pipes()]
            pipe.replaced = True
        pipe.draw(windowObj)
        if (bird.collision(pipe)):
            windowObj.fill(pygame.Color('#230056'))
            resetGame()
        if (not pipe.scored and pipe.pos + pipe.width < bird.pos[0]):
            score += 1
            pipe.scored = True
        if (not pipe.move(-10)):
            del pipe

    # Draw stuff
    scoreSurface = fontObj.render('Score: ' + str(score) + ' High: ' + str(highScore), False, fontColor)
    scoreRect = scoreSurface.get_rect()
    scoreRect.topleft = (windowObj.get_height() / 2, 10)
    windowObj.blit(scoreSurface, scoreRect)
    pygame.draw.rect(windowObj, groundColor, (0, groundLevel, windowObj.get_width(), windowObj.get_height()))

    bird.draw(windowObj)

    pygame.display.update()
    fpsTimer.tick(maxFPS)
