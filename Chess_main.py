import pygame
from chess_board import ChessBoard
from chess_board import l_o_s, l_o_p, name_of_squares


WHITE = (220,220,220)
BLACK = (40,40,40)
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
        self.en_pessent = False
        self.add_boardstate()
        self.player_turn = "w"

        #self.clocks = ChessClock()
        #self.clocks.begin()

        self.main()

    def move_piece(self, x_pos, y_pos, piece, castle=False):
        """Remove piece from current square moves to new square"""
        piece.castle = False
        coords = piece.coords
        #Get the square the piece is currently on
        current_square = get_square_at(coords[0], coords[1], self.board.l_o_s)

        #Get the square where the piece is being move to
        new_square = get_square_at(x_pos, y_pos, self.board.l_o_s)
        new_square_coords = name_of_squares[f"{new_square.name}"]

        #remove the piece from the square
        current_square.remove_piece()

        #If enemy piece on square capture it then place new piece
        if new_square.current_piece:
            new_square.capture_piece()
        new_square.place_piece(piece)

        #Update the position of the piece
        piece.rect = pygame.Rect(new_square_coords[0], new_square_coords[1], 100, 100)
        piece.coords = new_square_coords

        if piece.name == "Pawn" and (coords[1]-new_square_coords[1]) in (200,-200):
            direction = -1 if self.player_turn == "w" else 1
            en_pessent_square = get_square_at(new_square_coords[0], (new_square_coords[1]+(direction*100)), l_o_s)
            self.en_pessent = en_pessent_square
        else:
            self.en_pessent = False
        #place the piece onto the new square
        print(f"Moving {piece} to {new_square.name}")


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
            square_x, square_y = square.get_coords()
            square.color = WHITE if ((square_x / 100) + (square_y / 100)) % 2 == 0 else BLACK
        #Updates the size of the piece image
        if self.current_piece:
            self.current_piece.image = pygame.transform.scale(self.current_piece.image, (65, 65))
            #Displays the piece on screen at original size
            win.blit(self.current_piece.image, self.current_piece.rect)
        #Removes selection from piece
        self.current_piece = None

    def castle(self, square, mouse_x):
        """Special case for castling moves rook and king"""
        coords = self.current_piece.coords
        sx, sy = name_of_squares[f"{square.name}"]
        if mouse_x < coords[0]:
            castling_rook = get_square_at(coords[0]-300,coords[1], self.board.l_o_s)
            self.move_piece(sx, sy, self.current_piece)
            self.move_piece(sx+100, sy, castling_rook.current_piece, castle=True)
        elif mouse_x > coords[0]:
            castling_rook = get_square_at(coords[0]+400,coords[1], self.board.l_o_s)
            self.move_piece(sx, sy, self.current_piece)
            self.move_piece(sx-100, sy, castling_rook.current_piece, castle=True)

    def promotion(self, square):
        """Special case when a pawn reached the final rank
        Recives user input in text form to decide promtion, defualts to queen"""
        sx, sy = name_of_squares[f"{square.name}"]
        choice = input("What piece would you like to promote? Enter 'Q', 'R', 'B', or 'K'")
        if choice.lower() == "q":
            self.current_piece.name = "Queen"
            color = "white" if self.current_piece.color == "w" else "black"
            new_image = f"c:\\Users\\Jack\\Chess\\{color}_{self.current_piece.name}.PNG"
            self.current_piece.image = pygame.image.load(new_image)
        elif choice.lower() == "r":
            self.current_piece.name = "Rook"
            new_image = f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG"
            self.current_piece.image = pygame.image.load(new_image)
        elif choice.lower() == "b":
            self.current_piece.name = "Bishop"
            new_image = f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG"
            self.current_piece.image = pygame.image.load(new_image)
        elif choice.lower() == "k":
            self.current_piece.name = "Knight"
            new_image = f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG"
            self.current_piece.image = pygame.image.load(new_image)
        else:
            self.current_piece.name = "Queen"
            new_image = f"c:\\Users\\Jack\\Chess\\{self.current_piece.color}_{self.current_piece.name}.PNG"
            self.current_piece.image = pygame.image.load(new_image)
        
        self.move_piece(sx, sy, self.current_piece)
        self.draw_window()

    def take_en_pessent(self, square):
        """Places pawn on the passed square and removes the en_pessentable pawn"""
        sx, sy = name_of_squares[f"{square.name}"]
        direction = -1 if self.player_turn == "w" else 1
        square.place_piece(self.current_piece)
        en_pessent_square = get_square_at(sx, sy+(direction*100),l_o_s)
        print(square.name)
        print(en_pessent_square.name)
        en_pessent_square.capture_piece()
        self.move_piece(sx, sy, self.current_piece)

    def draw_window(self):
        """Draws the squares onto the blank template"""
        win.fill(PURPLE)
        for square in l_o_s:
            square.draw(win)
        for piece in l_o_p:
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
                        piece_coords = self.current_piece.coords
                        coords = name_of_squares[f"{square.name}"]
                        if square.color == HIGHLIGHT:
                            #Special case for castling to move 2 pieces at the same time
                            if self.current_piece.name == "King" and self.current_piece.castle:
                                castling_squares = self.current_piece.get_castling_squares()
                                if square in castling_squares:
                                    self.castle(square, mouse_x)
                            
                            #Special case for promotion
                            elif self.current_piece.name == "Pawn" and coords[1] in (0,700):
                                self.promotion(square)

                            #Special case for en_pessent
                            elif self.en_pessent and self.current_piece.name == "Pawn" and not square.current_piece and coords[0] != piece_coords[0]:
                                self.take_en_pessent(square)
                            else:
                                self.move_piece(coords[0], coords[1], self.current_piece)
                        elif square.color != HIGHLIGHT:
                            self.reset_selection()
                    
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for piece in self.board.l_o_p:
                            if piece.rect.collidepoint(mouse_x, mouse_y):
                                if piece.color == self.player_turn:
                                    piece.image = pygame.transform.scale(piece.image, (105, 105))
                                    piece.highlight_moves(l_o_s, l_o_p, False, self.en_pessent)
                                    self.current_piece = piece
                                    self.draw_window()
                                    break


            self.draw_window()
            pygame.display.update()
        pygame.quit()


current_game = ChessGame()
