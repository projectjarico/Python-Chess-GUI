import pygame
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

def get_square_at(x, y, squares):
    """find square from list of square and coords"""
    for square in squares:
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
        self.player_turn = "w"

        #self.clocks = ChessClock()
        #self.clocks.begin()

        self.main()

    def move_piece(self, x_pos, y_pos, piece, castle=False):
        """Remove piece from current square moves to new square"""
        piece.castle = False
        #Get the square the piece is currently on
        current_square = get_square_at(piece.x_pos, piece.y_pos, self.board.l_o_s)

        #Get the square where the piece is being move to
        new_square = get_square_at(x_pos, y_pos, self.board.l_o_s)

        #remove the piece from the square
        current_square.remove_piece()

        #Update the position of the piece
        piece.rect = pygame.Rect(x_pos, y_pos, 100, 100)
        piece.y_pos = y_pos
        piece.x_pos = x_pos

        #place the piece onto the new square
        if new_square.current_piece:
            new_square.capture_piece(self.board.l_o_p)
        new_square.place_piece(piece)



        #Reset selection and redraw the window
        self.reset_selection()
        if castle is False:
            self.player_turn = "b" if self.player_turn == "w" else "w"

    def add_boardstate(self):
        """indexs the most recent move into the transcript dictionary"""
        current_board = self.board.l_o_s[:]
        self.transcript[f"{self.move}"] = current_board
        self.move += 1    

    def reset_selection(self):
        """Removes highlight from squares and sets self.current piece to none"""
        for square in self.board.l_o_s:
            square.color = WHITE if ((square.x_pos / 100) + (square.y_pos / 100)) % 2 == 0 else BLACK
       
        #Updates the size of the piece image
        if self.current_piece:
            self.current_piece.piece_image = pygame.transform.scale(self.current_piece.piece_image, (65, 65))

            #Displays the piece on screen at original size
            win.blit(self.current_piece.piece_image, self.current_piece.rect)
        
        #Removes selection from piece
        self.current_piece = None

    def castle(self, square, mouse_x):
        """Special case for castling moves rook and king"""
        if mouse_x < self.current_piece.x_pos:
            castling_rook = get_square_at(self.current_piece.x_pos-300,self.current_piece.y_pos, self.board.l_o_s)
            self.move_piece(square.x_pos, square.y_pos, self.current_piece)
            self.move_piece(square.x_pos+100, square.y_pos, castling_rook.current_piece, castle=True)
        elif mouse_x > self.current_piece.x_pos:
            castling_rook = get_square_at(self.current_piece.x_pos+400,self.current_piece.y_pos, self.board.l_o_s)
            self.move_piece(square.x_pos, square.y_pos, self.current_piece)
            self.move_piece(square.x_pos-100, square.y_pos, castling_rook.current_piece, castle=True)

    def promotion(self, square):
        """Special case when a pawn reached the final rank"""
        """Recives user input in text form to decide promtion, defualts to queen"""
        choice = input("What piece would you like to promote? Enter 'Q', 'R', 'B', or 'K'")
        if choice.lower() == "q":
            self.current_piece.name = "Queen"
            self.current_piece.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG")
        elif choice.lower() == "r":
            self.current_piece.name = "Rook"
            self.current_piece.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG")
        elif choice.lower() == "b":
            self.current_piece.name = "Bishop"
            self.current_piece.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG")
        elif choice.lower() == "k":
            self.current_piece.name = "Knight"
            self.current_piece.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG")
        else:
            self.current_piece.name = "Queen"
            self.current_piece.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG")
        
        self.move_piece(square.x_pos, square.y_pos, self.current_piece)
        self.draw_window()


    def draw_window(self):
        """Draws the squares onto the blank template"""
        win.fill(PURPLE)
        for square in self.board.l_o_s:
            square.draw(win)
        for piece in self.board.l_o_p:
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
                        square = get_square_at(mouse_x, mouse_y, self.board.l_o_s)
                        if square.color == HIGHLIGHT:
                            #Special case for castling to move 2 pieces at the same time
                            if self.current_piece.name == "King" and abs(mouse_x-self.current_piece.x_pos) > 100:
                                self.castle(square, mouse_x)
                            
                            #Special case for promotion
                            elif self.current_piece.name == "Pawn" and square.y_pos in (0,700):
                                self.promotion(square)
                            
                            else:
                                self.move_piece(square.x_pos, square.y_pos, self.current_piece)
                        elif square.color != HIGHLIGHT:
                            self.reset_selection()
                    
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for piece in self.board.l_o_p:
                            if piece.rect.collidepoint(mouse_x, mouse_y):
                                if piece.color == self.player_turn:
                                    piece.piece_image = pygame.transform.scale(piece.piece_image, (105, 105))
                                    piece.highlight_moves(self.board.l_o_s, self.board.l_o_p)
                                    self.current_piece = piece
                                    self.draw_window()
                                    break


            self.draw_window()
            pygame.display.update()
        pygame.quit()


current_game = ChessGame()
current_game.draw_window()
