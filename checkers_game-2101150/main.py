
import pygame
from copy import deepcopy
from environment.game import Game
import math
FPS =60  
FONT = "Arial"
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (0,0,128) # Orange-red
WHITE = (255, 255, 204)  # Pale yellow
BLACK = (128,0,0)  # Dark gray
BLUE = (30, 144, 255)  # Dodger blue
GREY = (211, 211, 211)  # Light gray


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Welcom to checkers game')
RED = (255, 69, 0)  # Orange-red
WHITE = (255, 255, 204)  # Pale yellow

def minimax_alphabeta(position, depth, max_player, game, alpha, beta):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation =minimax_alphabeta(move, depth-1, False, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation =minimax_alphabeta(move, depth-1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break   
        return minEval, best_move

        


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
           # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
   


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    alpha = float('-inf')
    beta = float('inf')
    while run:
        clock.tick(FPS)
         
        if game.turn == WHITE:
            value, new_board =minimax_alphabeta(game.get_board(), 8, WHITE, game,alpha,beta)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()