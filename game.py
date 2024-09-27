import pygame
from constants import *
from tetromino import Tetromino

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")

    def draw(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                     ((self.current_piece.x + x) * BLOCK_SIZE,
                                      (self.current_piece.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))

        pygame.display.flip()

    def move_piece(self, dx, dy):
        self.current_piece.move(dx, dy)
        if self.check_collision():
            self.current_piece.move(-dx, -dy)
            if dy > 0:
                self.lock_piece()

    def rotate_piece(self):
        self.current_piece.rotate()
        if self.check_collision():
            self.current_piece.rotate()
            self.current_piece.rotate()
            self.current_piece.rotate()

    def check_collision(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (self.current_piece.x + x < 0 or
                        self.current_piece.x + x >= GRID_WIDTH or
                        self.current_piece.y + y >= GRID_HEIGHT or
                        self.grid[self.current_piece.y + y][self.current_piece.x + x]):
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = Tetromino()
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.grid) if all(row)]
        for line in full_lines:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        self.score += len(full_lines) ** 2 * 100
