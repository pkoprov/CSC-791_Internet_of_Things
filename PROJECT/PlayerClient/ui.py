# This file contains the UI for the connect 4 game.
import math
import numpy as np
import pygame
import sys
import time

import connect4
import player_client

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SQUARESIZE = 100

ROW_COUNT = 6
COLUMN_COUNT = 7


class Connect4UI:

    def __init__(self) -> None:
        self.board = self.create_board()
        pygame.init()
        self.width = COLUMN_COUNT * SQUARESIZE
        self.height = (ROW_COUNT + 1) * SQUARESIZE
        self.size = (self.width, self.height)
        self.RADIUS = int(SQUARESIZE / 2 - 5)
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.display_message("Starting Game...")
        time.sleep(3.0)
        self.draw_board(self.board)
        pygame.display.update()

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def new_board(self, board):
        self.board = self.flip_board(board)

    def flip_board(self, board):
        return np.flip(board, 0)

    def display_message(self, message):
        print(message)
        pygame.draw.rect(self.screen, BLACK,
                         (0, 0, self.width, SQUARESIZE))
        font = pygame.font.Font(None, 70)
        text = font.render(message, True, YELLOW)
        text_rect = text.get_rect(center=(self.width / 2, 50))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def draw_board(self, board):
        global screen
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, (c * SQUARESIZE, r *
                                                     SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(
                    c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), self.RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (int(
                        c * SQUARESIZE + SQUARESIZE / 2), self.height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                       self.RADIUS)
                elif board[r][c] == -1:
                    pygame.draw.circle(self.screen, YELLOW, (int(
                        c * SQUARESIZE + SQUARESIZE / 2), self.height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                       self.RADIUS)
        pygame.display.update()

    def print_winner(self, winner):
        if winner == 1:
            print("Player 1 wins!!!")
            label = self.myfont.render("Player 1 wins!!", 1, YELLOW)
        elif winner == 2:
            print("Player 2 wins!!!")
            label = self.myfont.render("Player 2 wins!!", 1, YELLOW)
        else:
            print("It's a draw!!!")

    def update_board(self):
        gameOver = False
        myfont = pygame.font.SysFont("monospace", 75)
        self.draw_board(self.board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, BLACK,
                                 (0, 0, self.width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(
                    self.screen, RED, (posx, int(SQUARESIZE / 2)), self.RADIUS)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, BLACK,
                                 (0, 0, self.width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if self.is_valid_location(self.board, col):
                    row = self.get_next_open_row(self.board, col)
                    self.drop_piece(self.board, row, col, 1)
                    return col
        self.draw_board(self.board)
        return -1
