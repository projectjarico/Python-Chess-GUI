#Piece PNGs By en:User:Cburnett - File:Chess rdt45.svg, CC BY-SA 3.0, 
#https://commons.wikimedia.org/w/index.php?curid=20363786
"""This file creates the chess board including starting squares and pieces"""

import copy
import pygame
count = 1
HIGHLIGHT = (55,25,20)


WHITE = (200,200,200)
BLACK = (50,50,50)


def deep_copy_list(list_to_copy):
    """Makes a copy of the current board for use in board state calculations"""
    new_list = []
    for square in list_to_copy:
        new_square = copy.deepcopy(square)
        new_list.append(new_square)
    return new_list



def get_square_at(x, y, l_o_s):
    """Finds a square in a list based on the x and y coords"""
    for square in l_o_s:
        if square.x_pos == x and square.y_pos == y:
            return square

class ChessBoard:
    """This object represents the board and hold info about piece positions and game state"""
    def __init__(self):
        """Set the board"""
        self.height = 8
        self.width = 8
        self.l_o_s, self.l_o_p = self.create_board()


    def create_board(self):
        """Creates 64 squares and 32 pieces
        Returns 2 lists l_o_s and l_o_p"""
        #3 lists for holding squares pieces and names
        l_o_s, l_o_p, names_of_squares = [], [], []

        #names the squares created below
        files = "abcdefgh"
        files = list(files)
        for file in files:
            ranks = list(range(1,9))
            ranks.reverse()
            for rank in ranks:
                names_of_squares.append(f"{file}{rank}")

        for i in range(8):
            for j in range(8):
                x = i * 100
                y = j * 100
                square_color = WHITE if (i + j) % 2 == 0 else BLACK
                name = names_of_squares.pop()
                #creates 24 pieces
                #assigns each piece its square then appends all squares and pieces into their list
                if y == 100:
                    piece_color = "w"
                    new_piece = ChessPiece(x, y, piece_color,"Pawn")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif y == 600:
                    piece_color = "b"
                    new_piece = ChessPiece(x, y, piece_color,"Pawn")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x in (0,700) and y in (0,700):
                    if y == 0:
                        piece_color = "w"
                    else:
                        piece_color = "b"
                    new_piece = ChessPiece(x, y, piece_color,"Rook")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x in (100, 600) and y in (0, 700):
                    if y == 0:
                        piece_color = "w"
                    else:
                        piece_color = "b"
                    new_piece = ChessPiece(x, y, piece_color,"Knight")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x in (200, 500) and y in (0, 700):
                    if y == 0:
                        piece_color = "w"
                    else:
                        piece_color = "b"   
                    new_piece = ChessPiece(x, y, piece_color,"Bishop")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x == 400 and  y in (0, 700):
                    if y == 0:
                        piece_color = "w"
                    else:
                        piece_color = "b"
                    new_piece = ChessPiece(x, y, piece_color,"Queen")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x == 300 and y in (0, 700):
                    if y == 0:
                        piece_color = "w"
                    else:
                        piece_color = "b"
                    new_piece = ChessPiece(x, y, piece_color,"King")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                else:
                    square = ChessSquare(x, y, square_color, name)
                l_o_s.append(square)
                l_o_p.append(new_piece)
                #l_o_s.reverse()
        return l_o_s, l_o_p

class ChessSquare:
    """Represents a chess square and any relevent info about it"""
    def __init__(self, x, y, color, name, rect = True):
        """Creates a square as a Rect and puts it on our board"""
        self.color = color
        if rect:
            self.rect = pygame.Rect(x, y, 100, 100)
        self.name = name
        self.x_pos = x
        self.y_pos = y
        self.current_piece = None

    def draw(self, win):
        """displays the square on screen"""
        pygame.draw.rect(win, self.color, self.rect)

    def place_piece(self, piece):
        self.current_piece = piece

    def capture_piece(self, l_o_p):
        if self.current_piece:
            self.current_piece.rect = pygame.Rect(-100,-100,0,0)
            l_o_p.remove(self.current_piece)
        
        self.current_piece = None

    def remove_piece(self):
        if self.current_piece:
            self.current_piece = None

class ChessPiece:
    """Represent a piece including its directional motion, color, and current position"""
    def __init__(self, x_pos, y_pos, piece_color, piece_name):
        self.count = 1
        self.name = piece_name
        self.color = piece_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        piece_color = "white"if self.color == "w" else "black"
        self.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{piece_color}_{self.name}.PNG")
        self.castle = True
        self.rect = pygame.Rect(x_pos, y_pos, 100, 100)

    def draw_piece(self, win):
        """Displays the piece inside the square"""
        piece_rect = self.piece_image.get_rect(center=self.rect.center)
        win.blit(self.piece_image, piece_rect)

    #We May not need this or its copy in square.
    #Global deep_copy_list is being used instead
    def __deepcopy__(self, memo):
        # Create a new instance of ChessPiece with copied attributes
        new_piece = ChessPiece(
            copy.deepcopy(self.x_pos, memo),
            copy.deepcopy(self.y_pos, memo),
            copy.deepcopy(self.color, memo),
            copy.deepcopy(self.name, memo))
        # Update the memo dictionary to track the newly created instance
        memo[id(self)] = new_piece
        return new_piece

    def check_castle(self, l_o_s, l_o_p, castling_moves):
        """Handles short castle checks"""
        #4 early checks before move highlight
        if not self.castle:
            return False
        rook_square = castling_moves[-1]

        if all(square.current_piece for square in castling_moves[:-1]):
            return False
        if not rook_square.current_piece:
            return False
        if rook_square.current_piece.name != "Rook" or not rook_square.current_piece.castle:
            return False
        
        #Highlights all enemy moves
        for square in l_o_s:
            if square.current_piece and square.current_piece.color != self.color:
                square.current_piece.highlight_moves(l_o_s, l_o_p, True)
        if all(square.color is not HIGHLIGHT for square in castling_moves[:-1]):
            return True

    def check_castling(self, l_o_s, l_o_p):
        """Checks king, rook, and castling squares for conditions, highlights"""

        short_castle_squares = (get_square_at(self.x_pos-100, self.y_pos, l_o_s),
                                get_square_at(self.x_pos-200, self.y_pos, l_o_s),
                                get_square_at(self.x_pos-300,self.y_pos,l_o_s))
        long_castle_squares = (get_square_at(self.x_pos+100, self.y_pos, l_o_s),
                                get_square_at(self.x_pos+200, self.y_pos, l_o_s),
                                get_square_at(self.x_pos+300,self.y_pos,l_o_s),
                                get_square_at(self.x_pos+400, self.y_pos, l_o_s))
        castle_short = self.check_castle(l_o_s, l_o_p, short_castle_squares)
        castle_long = self.check_castle(l_o_s, l_o_p, long_castle_squares)

        return castle_short, castle_long



    def highlight_moves(self, l_o_s, l_o_p, temp_boardstate = False):

        """Called when a chess piece is clicked highlight all the legal moves for the piece clicked"""
        count = 1
        if self.name == "Pawn":
            pawn_moves = [(100, 100),(-100, 100)] if self.color == "w" else [(100, -100),(-100, -100)]
            direction = 1 if self.color == "w" else -1
            # Check if the square in front of the pawn is empty and highlight it
            if temp_boardstate is False:
                square = get_square_at(self.x_pos, self.y_pos + direction * 100, l_o_s)     
                count += 1           
                check = self.test_boardstate(square, l_o_s, l_o_p)
                if check is not True and square and square.current_piece is None:
                    square.color = HIGHLIGHT


            #Check if the square two steps in front of the pawn is empty and highlight it
            if temp_boardstate is False:
                if self.y_pos == 100 or self.y_pos == 600:
                    if self.castle:
                        square = get_square_at(self.x_pos, self.y_pos + direction * 200, l_o_s)
                        check = self.test_boardstate(square, l_o_s, l_o_p)
                        if  square and square.current_piece is None and check != True:
                            square.color = HIGHLIGHT


            # Check if the diagonally forward squares have opponent's pieces and highlight them
            if temp_boardstate is False:
                for x, y in pawn_moves:
                    square = get_square_at(self.x_pos+x, self.y_pos+y, l_o_s)
                    if square and square.current_piece and square.current_piece.color != self.color:
                        check = self.test_boardstate(square, l_o_s, l_o_p)
                        if check is not True:
                            square.color = HIGHLIGHT

            else:
                #if enemy move is being considered it hightlights all possible moves
                square = get_square_at(self.x_pos - 100,
                                       self.y_pos + direction * 100, l_o_s)
                if square and square.current_piece and square.current_piece.color != self.color:
                    square.color = HIGHLIGHT
                square = get_square_at(self.x_pos + 100,
                                       self.y_pos + direction * 100, l_o_s)
                if square and square.current_piece and square.current_piece.color != self.color:
                    square.color = HIGHLIGHT

        if self.name == "Knight":
            list_of_knight_moves = [(200, 100),(200,-100),(-200,100),(-200,-100),
                                    (100,200),(-100,200),(100,-200),(-100,-200)]
            for x, y in list_of_knight_moves:
                square = get_square_at(self.x_pos+x, self.y_pos+y, l_o_s)

                if square:
                    if temp_boardstate is True:
                        square.color = HIGHLIGHT
                    else:
                        if square.current_piece:
                            if square.current_piece.color != self.color:
                                if temp_boardstate is False:
                                    check = self.test_boardstate(square, l_o_s, l_o_p)
                                if check is False:
                                    square.color = HIGHLIGHT
                        else:
                            if temp_boardstate is False:
                                check = self.test_boardstate(square, l_o_s, l_o_p)
                                if check is False:
                                    square.color = HIGHLIGHT

        if self.name == "Rook":
            #Uses a while loop to continue highlighting squares until it hits an obstacle
            rook_directions = [(0,1),(0,-1),(1,0),(-1,0)]
            for dr in rook_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], l_o_s, temp_boardstate, l_o_p)

        if self.name == "Bishop":
            #Uses a while loop to continue highlighting squares until it hits an obstacle
            biship_directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
            for dr in biship_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], l_o_s, temp_boardstate, l_o_p)

        if self.name == "Queen":
            #Uses a while loop to continue highlighting squares until it hits an obstacle
            king_and_queen_directions = [(1,1),(1,0),(1,-1),(-1,1),(-1,-1),(-1,0),(0,1),(0,-1)]
            for dr in king_and_queen_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], l_o_s, temp_boardstate, l_o_p)
        if self.name == "King":
            if temp_boardstate is False:
                castle_short, castle_long = self.check_castling(l_o_s, l_o_p)
                short_square = get_square_at(self.x_pos-200, self.y_pos, l_o_s)
                long_square = get_square_at(self.x_pos+200, self.y_pos, l_o_s)

                for square in l_o_s:
                    square_color = WHITE if (square.x_pos + square.y_pos)/100 % 2 == 0 else BLACK
                    square.color = square_color

                if castle_short is True:
                    short_square.color = HIGHLIGHT
                if castle_long is True:
                    long_square.color = HIGHLIGHT


            #Uses a while loop to continue highlighting squares until it hits an obstacle
            king_and_queen_directions = [(1,1),(1,0),(1,-1),(-1,1),(-1,-1),(-1,0),(0,1),(0,-1)]
            for dr in king_and_queen_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], l_o_s, temp_boardstate, l_o_p)

    def hightlight_squares_in_direction(self, dx, dy, l_o_s, temp_boardstate, l_o_p):
        """Highlights unobstructed moves for bishop, rook, and queen""" 

        x, y = self.x_pos, self.y_pos
        distance = 100
        while True:

            #finds destination square 
            x_new, y_new = x + distance * dx, y + distance * dy
            distance += 100
            square = get_square_at(x_new, y_new, l_o_s)
            #check if temp_board state
            if temp_boardstate is False:
                #breaks if move is impossible
                if square is None:
                    break

                if square.current_piece and square.current_piece.color == self.color:
                    break


                #runs test to see if move would leave you in check
                else:
                    check = self.test_boardstate(square, l_o_s, l_o_p) 

                if square.current_piece is None and check is False:
                    square.color = HIGHLIGHT
                    if self.name == "King":
                        break

                elif square.current_piece and square.current_piece.color != self.color:
                    if check is False:
                        square.color = HIGHLIGHT
                        break
                else:
                    continue

            #highlights squares while calculating enemy moves
            if temp_boardstate is True:
                
                if square is None:
                    break
                elif square.current_piece is None:
                    square.color = HIGHLIGHT
                    if self.name == "King":
                        break
                elif square.current_piece.color == self.color:
                    break
                elif square and square.current_piece.color != self.color:
                    square.color = HIGHLIGHT
                    break

        
    def test_boardstate(self, square, l_o_s, l_o_p):
        """test new board state for check condition by iterating over enemy pieces
        saves the board as it is precheck and resets all highlighted square"""
        current_boardstate = deep_copy_list(l_o_s)
        current_pieces = deep_copy_list(l_o_p)

        #place all pieces onto their squares
        #So current boardstate has pieces on it
        for piece in current_pieces:
            new_square = get_square_at(piece.x_pos, piece.y_pos, current_boardstate)
            new_square.place_piece(piece)

        #Get the square the piece is currently on
        current_square = get_square_at(self.x_pos, self.y_pos, current_boardstate)
        temp_piece = current_square.current_piece

        #Removes enemy piece
        if current_square.current_piece: 
            current_square.capture_piece(current_pieces)

        temp_square = get_square_at(square.x_pos, square.y_pos,current_boardstate)
        temp_square.place_piece(temp_piece)

        #removes any highlighted squares
        for temp_square in current_boardstate:
            temp_square.color = WHITE if ((temp_square.x_pos / 100) + (temp_square.y_pos / 100)) % 2 == 0 else BLACK

        #Update the position of the piece
        temp_piece.rect = pygame.Rect(temp_piece.x_pos, temp_piece.y_pos, 100, 100)
        temp_piece.y_pos = square.y_pos
        temp_piece.x_pos = square.x_pos



        #Highlight all enemy moves
        list_of_enemy_moves = []
        for square in current_boardstate:

            if square.current_piece != None and square.current_piece.color != self.color:
                #Highlights all possible enemy moves
                square.current_piece.highlight_moves(current_boardstate, current_pieces, True)
               
                for square in current_boardstate:
                    if square.color == HIGHLIGHT and square not in list_of_enemy_moves:
                        list_of_enemy_moves.append(square)
                        # Remove duplicates
                        list_of_enemy_moves = list(set(list_of_enemy_moves))             



        #Gets position of friendly king
        for square in current_boardstate:
            if square.current_piece and square.current_piece.name == "King" and square.current_piece.color == self.color:
                kings_square = square
        if self.name == "King":
            kings_square = get_square_at(self.x_pos,self.y_pos, l_o_s)


        #destroys the temp piece
        temp_piece.rect = pygame.Rect(1000, 1000, 100, 100)


        #tests if the square is highlighted if so it returns in_check = True
        if kings_square in list_of_enemy_moves:
            return True
        else:
            return False
