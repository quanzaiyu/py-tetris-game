import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # 秒

    while not game.game_over:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()

        if fall_time / 1000 > fall_speed:
            game.move_piece(0, 1)
            fall_time = 0

        game.draw()

    print(f"游戏结束! 最终得分: {game.score}")
    pygame.quit()

if __name__ == "__main__":
    main()
