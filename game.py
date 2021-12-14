from typing import List
import pygame
from score import ScoreScheme
from board import Board
from menu import MainMenu
from player import Player, Computer, Human
from tree import plot_tree


class Game:
    def __init__(self):
        pygame.init()
        self.w, self.h = 492, 499
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Connect-4')
        pygame.display.set_icon(pygame.image.load('res/Images/logo.png'))  # doesn't show in ubuntu
        self.font_path = 'res/Fonts/font_with_num.ttf'
        self.playing, self.running = False, True
        self.current_menu = MainMenu(self)
        self.scoring = None
        self.root = None

    def game_loop(self, work):
        players = List[Player]
        if work == 1:
            self.scoring = ScoreScheme('min_max', int(self.current_menu.choiceMenu.maxDepth))
            players = [Human(), Computer()]
        elif work == 2:
            self.scoring = ScoreScheme('alpha_beta', int(self.current_menu.choiceMenu.maxDepth))
            players = [Human(), Computer()]
        elif work == 3:
            self.scoring = ScoreScheme(None, None)
            players = [Human(), Human(True)]
        turn = 0
        game_board = Board(self.screen)

        while self.playing:
            self.screen.fill((255, 255, 255))
            self.draw_cols_lbls()
            game_board.display_game_board()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.playing = False
                    self.running = False

                if isinstance(players[turn], Human):
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_1:
                            players[turn].update_board(game_board, col=0)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_2:
                            players[turn].update_board(game_board, col=1)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_3:
                            players[turn].update_board(game_board, col=2)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_4:
                            players[turn].update_board(game_board, col=3)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_5:
                            players[turn].update_board(game_board, col=4)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_6:
                            players[turn].update_board(game_board, col=5)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_7:
                            players[turn].update_board(game_board, col=6)
                            turn = (turn + 1) % 2
                            print(self.scoring.calculate_heuristic(game_board))
                            break
                        elif e.key == pygame.K_ESCAPE:
                            self.playing = False
                        elif e.key == pygame.K_SPACE:
                            if self.root is not None:
                                plot_tree(self.root, self.scoring.max_depth)
                elif isinstance(players[turn], Computer):
                    self.root = self.scoring.score(game_board)
                    players[turn].update_board(game_board, self.root.branch())
                    turn = (turn + 1) % 2

            game_board.update_board()
            if work < 3:
                r, y = self.scoring.score_calc(game_board)
                self.draw_text('Red: ' + str(r) + '   Yellow: ' + str(y), 20, 200, 10)
                self.draw_text('Press SPACE to visualize the MIN-MAX Tree', 18, 5, 481)
            pygame.display.update()

    def draw_cols_lbls(self):
        for i in range(7):
            self.draw_text(str(i + 1), 20, 36 + (i * 70), 40)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_path, size)
        t_surface = font.render(text, True, (255, 0, 0))
        t_surface.get_rect().center = (x, y)
        self.screen.blit(t_surface, (x, y))
