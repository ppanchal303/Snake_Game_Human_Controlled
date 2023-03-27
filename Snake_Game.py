#######################################################
# Project: Snake Game                                 #
# Author: Pranav Panchal                              #
# Date: 11/09/2022                                    # 
#######################################################                               
# This is a snake game engine which take human inputs #
#######################################################

import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
# from IPython.display import clear_output

pygame.init()

# game window variables
WIDTH = 400
HEIGHT = 400

BLOCK = 20
SPEED = 10

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 105, 97)
GREEN = (119, 221, 119)
GRAY = (90, 102, 117)

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

Point = namedtuple("Point", "x, y")

clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self, WIDTH = 400, HEIGHT = 400):
        self.width = WIDTH
        self.height = HEIGHT
        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game!!!")
        self.clock = pygame.time.Clock()
        self.reset()

    # reset and re-initialise the game state
    def reset(self):  
        self.head = Point(self.width/2, self.height/2)
        self.snakebody = [self.head,
                          Point(self.head.x-BLOCK, self.head.y),
                          Point(self.head.x-(2*BLOCK), self.head.y)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.gen_food()

    # generate food at a random location on map, if random location is within snakebody -> recall gen_food() again
    def gen_food(self):
        x = random.randint(0, (self.width - BLOCK) // BLOCK) * BLOCK
        y = random.randint(0, (self.width - BLOCK) // BLOCK) * BLOCK
        self.food = Point(x, y)
        if self.food in self.snakebody:
            self.gen_food()
        
    def game_step(self):
        # collect user input
        for event in pygame.event.get():
            # if game quit
            if event.type == pygame.QUIT:
                # pygame.quit()
                # quit()
                done = True
            # which direction key presed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move in the current direction
        self.move()
        self.snakebody.insert(0, self.head)

        # checks whether game is finished(over)
        done = False
        if self.is_collision():
            done = True
            return done, self.score

        # check new step resulted in eating food (YES -> increase score, get reward, gen_food()) |#| (NO -> move and shift the tail)
        if self.head == self.food:
            self.score += 1
            self.gen_food()
        else:
            self.snakebody.pop()

        self.draw_game()
        self.clock.tick(SPEED)

        return done, self.score
    
    def move(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK
        elif self.direction == Direction.LEFT:
            x -= BLOCK
        elif self.direction == Direction.UP:
            # print(new_direction)
            y -= BLOCK
        elif self.direction == Direction.DOWN:
            y += BLOCK

        self.head = Point(x, y)
        return self.head

    def is_collision(self, pt = None):
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x > self.width - BLOCK or pt.y < 0 or pt.y > self.height - BLOCK:
            return True
        elif self.head in self.snakebody[1:]:
            return True          

    def draw_game(self):
        self.WIN.fill(BLACK)

        # drawing the grid
        for x in np.arange(BLOCK, WIDTH, BLOCK):
            pygame.draw.line(self.WIN, GRAY, (x, 0), (x, HEIGHT))
        for y in np.arange(BLOCK, HEIGHT, BLOCK):
            pygame.draw.line(self.WIN, GRAY, (0, y), (WIDTH, y))

        # drawing the snake body
        for item in self.snakebody:
            pygame.draw.rect(self.WIN, RED, (item.x, item.y, BLOCK, BLOCK))

        # display food
        pygame.draw.rect(self.WIN, GREEN, (self.food.x, self.food.y, BLOCK, BLOCK))

        # display score
        pygame.font.init()
        font = pygame.font.Font('arial.ttf', 19)
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.WIN.blit(text, [0, 0])
        pygame.display.flip()

def main():
    s = SnakeGame()
    
    while True:
        done, score = s.game_step()

        if done:
            print(f"Final score: {score}")
            pygame.quit()
            quit()
            break

if __name__ == "__main__":
    main()