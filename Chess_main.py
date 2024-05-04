import os
import pygame
from chess_board import ChessPiece
from chess_board import ChessSquare
from chess_board import ChessBoard

names_of_squares = []




WHITE = (200,200,200)
BLACK = (50,50,50)
PURPLE = (55,25,255)
HIGHLIGHT = (55,25,20)
FPS = 60
white_square = pygame.image.load(r"c:\Users\Jack\Chess\white_square.PNG")
white_square = pygame.transform.scale(white_square,(100,100))
black_square = pygame.image.load(r"c:\Users\Jack\Chess\black_square.PNG")
black_square = pygame.transform.scale(black_square,(100,100))

width, height = 800, 800
win = pygame.display.set_mode((width, height))

def get_square_at(x, y, list):
    for square in list:
        if square.rect.collidepoint(x,y):
            return square


         


class ChessGame:
    """This object creates then manages a game of chess"""
    def __init__(self):
        """create the game, set the board and player clocks. Then start the clocks. """
        self.board = ChessBoard()
        self.current_piece = None
        self.transcript = {}
        self.move = 0
        self.add_boardstate()    

        #self.clocks = ChessClock()
        #self.clocks.begin()


        self.main()

    def move_piece(self, x_pos, y_pos, piece):
        """Remove piece from current square moves to new square"""
        #Get the square the piece is currently on
        current_square = get_square_at(piece.x_pos, piece.y_pos, self.board.list_of_squares)

        #Get the square where the piece is being move to
        new_square = get_square_at(x_pos, y_pos, self.board.list_of_squares)

        #remove the piece from the square
        current_square.remove_piece()

        #Update the position of the piece
        piece.rect = pygame.Rect(x_pos, y_pos, 100, 100)
        piece.y_pos = y_pos
        piece.x_pos = x_pos

        #place the piece onto the new square
        if new_square.current_piece:
            new_square.capture_piece(self.board.list_of_pieces)
        new_square.place_piece(piece)



        #Reset selection and redraw the window
        self.reset_selection()
        self.draw_window


    def add_boardstate(self):
        """indexs the most recent move into the transcript dictionary"""
        current_board = self.board.list_of_squares[:]
        self.transcript[f"{self.move}"] = current_board
        self.move += 1

        

    def reset_selection(self):
        for square in self.board.list_of_squares:
            square.color = WHITE if ((square.x_pos / 100) + (square.y_pos / 100)) % 2 == 0 else BLACK
        
        #Updates the size of the piece image
        self.current_piece.piece_image = pygame.transform.scale(self.current_piece.piece_image, (65, 65))

        #Displays the piece on screen at original size
        win.blit(self.current_piece.piece_image, self.current_piece.rect)
        
        #Removes selection from piece
        self.current_piece = None


    def draw_window(self):
        """Draws the squares onto the blank template"""
        win.fill(PURPLE)
        for square in self.board.list_of_squares:
            square.draw(win)
        for piece in self.board.list_of_pieces:
            piece.draw_piece(win)


    def main(self):
        """Open the game window"""
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_piece:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        square = get_square_at(mouse_x, mouse_y, self.board.list_of_squares)
                        if square.color == HIGHLIGHT:
                            self.move_piece(square.x_pos, square.y_pos, self.current_piece)
                        elif square.color != HIGHLIGHT:
                            self.reset_selection()
                    
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for piece in self.board.list_of_pieces:
                            if piece.rect.collidepoint(mouse_x, mouse_y):
                                piece.piece_image = pygame.transform.scale(piece.piece_image, (105, 105))
                                piece.highlight_moves(self.board.list_of_squares, self.board.list_of_pieces)
                                self.current_piece = piece

                                self.draw_window()                    


            self.draw_window()
            pygame.display.update()
        pygame.quit()


current_game = ChessGame()
current_game.draw_window()




if __name__ == "__Chess_main__":
    main()
