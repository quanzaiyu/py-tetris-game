import pygame
from constants import *
from tetromino import Tetromino

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()  # 添加这一行
        self.game_over = False
        self.score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")

    def draw(self):
        self.screen.fill(BLACK)

        # 绘制游戏区域
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制当前方块
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                     ((self.current_piece.x + x) * BLOCK_SIZE,
                                      (self.current_piece.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制右侧区域背景
        pygame.draw.rect(self.screen, LIGHT_GRAY, (GRID_WIDTH * BLOCK_SIZE, 0, SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT))

        # 绘制分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))

        # 绘制下一个方块预告
        self.draw_next_piece()

        pygame.display.flip()

    def draw_next_piece(self):
        next_piece_x = GRID_WIDTH * BLOCK_SIZE + 50
        next_piece_y = 100
        font = pygame.font.Font(None, 30)
        next_text = font.render("Next:", True, BLACK)
        self.screen.blit(next_text, (next_piece_x, next_piece_y - 30))

        # 绘制下一个方块
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                     (next_piece_x + x * BLOCK_SIZE,
                                      next_piece_y + y * BLOCK_SIZE,
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))

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
        # 首先将当前方块添加到游戏网格中
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color

        # 清除已完成的行
        self.clear_lines()

        # 更新当前方块为下一个方块，并生成新的下一个方块
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()

        # 检查游戏是否结束
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.grid) if all(row)]
        for line in full_lines:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        self.score += len(full_lines) ** 2 * 100
