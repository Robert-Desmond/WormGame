import pygame
import sys
import random

# Sets the game window title
pygame.init()
pygame.display.set_caption('Worm by Robert Desmond')

# Object class for the worm/player
class Worm(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (255, 194, 205)
        self.score = 0

    def get_position_head(self):
        return self.positions[0]


    def turn(self, point):
        if self.length > 1 and (point[0] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_position_head()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (255, 147, 172), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Object class for food
class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (152, 251, 152)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (80, 220, 100), r, 1)

# Draws the background grid for the game
def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (128, 96, 77), r)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (101, 67, 33), rr)

# Constant variables to set different aspects needed for the game window and directions for the player
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main Game Loop
def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    worm = Worm()
    food = Food()

    font = pygame.font.SysFont("consolas", 18)

    while (True):
        clock.tick(10)
        worm.handle_keys()
        draw_grid(surface)
        worm.move()
        if worm.get_position_head() == food.position:
            worm.length += 1
            worm.score += 1
            food.randomize_position()
        worm.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = font.render("Score: {0}".format(worm.score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()
