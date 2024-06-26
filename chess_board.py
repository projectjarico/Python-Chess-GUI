#Piece PNGs By en:User:Cburnett - File:Chess rdt45.svg, CC BY-SA 3.0, 
#https://commons.wikimedia.org/w/index.php?curid=20363786
"""This file creates the chess board including starting squares and pieces"""

import copy
import pygame
count = 1
HIGHLIGHT = (155,25,20)
WHITE = (220,220,220)
BLACK = (40,40,40)

name_of_squares = {}
l_o_s, l_o_p = [], []

def deep_copy_list(list_to_copy):
    """Makes a copy of the current board for use in board state calculations"""
    new_list = []
    for square in list_to_copy:
        new_square = copy.deepcopy(square)
        new_list.append(new_square)
    return new_list



def get_square_at(x, y, los=l_o_s):
    """Finds a square in a list based on the x and y coords"""
    for square in los:
        if name_of_squares[f"{square.name}"] == (x,y):
            return square


def create_board():
    """Creates 64 squares and 32 pieces
    Returns 2 lists l_o_s and l_o_p"""
    print("Creating board just this once")
    #3 lists for holding squares pieces and names
    # Naming the squares created below
    files = "abcdefgh"
    reversed_files = files[::-1]
    for file in reversed_files:
        ranks = list(range(1, 9))
        for rank in ranks:
            square_name = f"{file}{rank}"
            x = (ord("h")- ord(file)) * 100
            y = (rank - 1) * 100
            square_color = WHITE if (x + y)/100 % 2 == 0 else BLACK
            coords = (x, y)
            name_of_squares[square_name] = coords
            #creates 24 pieces
            #assigns each piece its square then appends all squares and pieces into their list
            for key, value in name_of_squares.items():
                if (x,y) == value:
                    square_name == key
                    break
            if y == 100:
                piece_color = "w"
                new_piece = ChessPiece(x, y, piece_color,"Pawn")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            elif y == 600:
                piece_color = "b"
                new_piece = ChessPiece(x, y, piece_color,"Pawn")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            elif x in (0,700) and y in (0,700):
                if y == 0:
                    piece_color = "w"
                else:
                    piece_color = "b"
                new_piece = ChessPiece(x, y, piece_color,"Rook")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            elif x in (100, 600) and y in (0, 700):
                if y == 0:
                    piece_color = "w"
                else:
                    piece_color = "b"
                new_piece = ChessPiece(x, y, piece_color,"Knight")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            elif x in (200, 500) and y in (0, 700):
                if y == 0:
                    piece_color = "w"
                else:
                    piece_color = "b"
                new_piece = ChessPiece(x, y, piece_color,"Bishop")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            elif x == 400 and  y in (0, 700):
                if y == 0:
                    piece_color = "w"
                else:
                    piece_color = "b"
                new_piece = ChessPiece(x, y, piece_color,"Queen")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            elif x == 300 and y in (0, 700):
                if y == 0:
                    piece_color = "w"
                else:
                    piece_color = "b"
                new_piece = ChessPiece(x, y, piece_color,"King")
                square = ChessSquare(square_color, square_name)
                square.place_piece(new_piece)
                l_o_p.append(new_piece)
                l_o_s.append(square)
            else:
                square = ChessSquare(square_color, square_name)
                l_o_s.append(square)
            
    return l_o_s, l_o_p

class ChessBoard:
    """This object represents the board and hold info about piece positions and game state"""
    def __init__(self):
        """Set the board"""
        self.height = 8
        self.width = 8
        #self.name_of_squares =
        self.l_o_s, self.l_o_p = create_board()


class ChessSquare:
    """Represents a chess square and any relevent info about it"""
    def __init__(self, color, name, rect = True):
        """Creates a square as a Rect and puts it on our board"""
        self.color = color
        self.name = name
        self.current_piece = None
        if rect:
            (x,y) = self.get_coords()
            self.rect = pygame.Rect(x, y, 100, 100)

    def get_coords(self):
        """Returns pygames x,y coords for this square"""
        return name_of_squares[f"{self.name}"]


    def draw(self, win):
        """displays the square on screen"""
        pygame.draw.rect(win, self.color, self.rect)

    def place_piece(self, piece):
        """Places passed piece onto this square"""
        self.current_piece = piece
        new_coords = self.get_coords()
        piece.rect = pygame.Rect(new_coords[0], new_coords[1], 100, 100)
        piece.coords = new_coords

    def capture_piece(self):
        """Removes the piece from this square and places it off the board"""
        if self.current_piece:
            self.current_piece.rect = pygame.Rect(-100,-100,0,0)
            self.current_piece.coords = (1000, 1000)
        self.remove_piece()
    def __deepcopy__(self, memo):
        # Create a new instance of ChessPiece with copied attributes
        new_piece = ChessSquare(
            copy.deepcopy(self.color, memo),
            copy.deepcopy(self.name, memo))
        # Update the memo dictionary to track the newly created instance
        memo[id(self)] = new_piece
        return new_piece
    def remove_piece(self):
        """removes  the piece on this square"""
        if self.current_piece:
            self.current_piece = None

class ChessPiece:
    """Represent a piece including its directional motion, color, and current position"""
    def __init__(self, x_pos, y_pos, piece_color, piece_name):
        self.count = 1
        self.name = piece_name
        self.color = piece_color
        self.coords = (x_pos, y_pos)
        piece_color = "white"if self.color == "w" else "black"
        self.image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{piece_color}_{self.name}.PNG")
        self.castle = True
        self.rect = pygame.Rect(x_pos, y_pos, 100, 100)

    def draw_piece(self, win):
        """Displays the piece inside the square"""
        piece_rect = self.image.get_rect(center=self.rect.center)
        win.blit(self.image, piece_rect)

    #We May not need this or its copy in square.
    #Global deep_copy_list is being used instead
    def __deepcopy__(self, memo):
        # Create a new instance of ChessPiece with copied attributes
        x, y = self.coords
        new_piece = ChessPiece(
            copy.deepcopy(x, memo),
            copy.deepcopy(y, memo),
            copy.deepcopy(self.color, memo),
            copy.deepcopy(self.name, memo))
        # Update the memo dictionary to track the newly created instance
        memo[id(self)] = new_piece
        return new_piece

    def get_castling_squares(self):
        if self.color == "w":
            short_square = get_square_at(100, 0, l_o_s)
            long_square = get_square_at(500, 0, l_o_s)
            castling_squares = (short_square, long_square)
        else:
            short_square = get_square_at(100, 700, l_o_s)
            long_square = get_square_at(500, 700, l_o_s)
            castling_squares = (short_square, long_square)

        return castling_squares

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

        short_castle_squares = (get_square_at(self.coords[0]-100, self.coords[1], l_o_s),
                                get_square_at(self.coords[0]-200, self.coords[1], l_o_s),
                                get_square_at(self.coords[0]-300,self.coords[1],l_o_s))
        long_castle_squares = (get_square_at(self.coords[0]+100, self.coords[1], l_o_s),
                                get_square_at(self.coords[0]+200, self.coords[1], l_o_s),
                                get_square_at(self.coords[0]+300,self.coords[1],l_o_s),
                                get_square_at(self.coords[0]+400, self.coords[1], l_o_s))
        castle_short = self.check_castle(l_o_s, l_o_p, short_castle_squares)
        castle_long = self.check_castle(l_o_s, l_o_p, long_castle_squares)

        return castle_short, castle_long



    def highlight_moves(self, los=l_o_s, lop=l_o_p, temp_boardstate = False, en_pesent=False):
        """Called when a chess piece is clicked highlight all the legal moves for the piece clicked"""
        dx, dy = self.coords
        if self.name == "Pawn":
            pawn_moves = [(100, 100),(-100, 100)] if self.color == "w" else [(100, -100),(-100, -100)]
            direction = 1 if self.color == "w" else -1
            if temp_boardstate is False:
                #if pawn is on starting square and has not moved highlight 2 squares ahead
                if dy == 100 or dy == 600 and self.castle:
                    square = get_square_at(dx, dy + direction * 200, los)
                    check = self.test_boardstate(square)
                    if square and square.current_piece is None and check is not True:
                        square.color = HIGHLIGHT
                
                #Highlight the first square ahead as well
                square = get_square_at(dx, dy + (direction * 100), los)
                check = self.test_boardstate(square)
                if check is not True and square and square.current_piece is None:
                    square.color = HIGHLIGHT


            # Check if the diagonally forward squares have opponent's pieces and highlight them
            if temp_boardstate is False:
                if en_pesent:
                    for x, y in pawn_moves:
                        square = get_square_at (dx+x, dy+y)
                        if square and square == en_pesent:
                            check = self.test_boardstate(square)
                            if check is not True:
                                en_pesent.color = HIGHLIGHT
                for x, y in pawn_moves:
                    square = get_square_at(dx+x, dy+y, los)
                    if square and square.current_piece and square.current_piece.color != self.color:
                        check = self.test_boardstate(square)
                        if check is not True:
                            square.color = HIGHLIGHT
            else:
                #if enemy move is being considered it hightlights all possible moves
                square = get_square_at(dx - 100,
                                       dy + direction * 100, los)
                if square:
                    square.color = HIGHLIGHT
                square = get_square_at(dx + 100,
                                       dy + direction * 100, los)
                if square:
                    square.color = HIGHLIGHT

        if self.name == "Knight":
            dx, dy = self.coords
            list_of_knight_moves = [(200, 100),(200,-100),(-200,100),(-200,-100),
                                    (100,200),(-100,200),(100,-200),(-100,-200)]
            for x, y in list_of_knight_moves:
                square = get_square_at(dx+x, dy+y, los)
                if square:
                    if temp_boardstate is True:
                        if square.current_piece is None:
                            square.color = HIGHLIGHT
                        elif square.current_piece.color != self.color:
                            square.color = HIGHLIGHT
                    else:
                        if square.current_piece:
                            if square.current_piece.color != self.color:
                                if temp_boardstate is False:
                                    check = self.test_boardstate(square)
                                if check is False:
                                    square.color = HIGHLIGHT
                        else:
                            if temp_boardstate is False:
                                check = self.test_boardstate(square)
                                if check is False:
                                    square.color = HIGHLIGHT

        if self.name == "Rook":
            #Uses a while loop to continue highlighting squares until it hits an obstacle
            rook_directions = [(0,1),(0,-1),(1,0),(-1,0)]
            for dr in rook_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], los, temp_boardstate)

        if self.name == "Bishop":
            #Uses a while loop to continue highlighting squares until it hits an obstacle
            biship_directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
            for dr in biship_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], los, temp_boardstate)

        if self.name == "Queen":
            #Uses a while loop to continue highlighting squares until it hits an obstacle
            king_and_queen_directions = [(1,1),(1,0),(1,-1),(-1,1),(-1,-1),(-1,0),(0,1),(0,-1)]
            for dr in king_and_queen_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], los, temp_boardstate)
        if self.name == "King":
            if temp_boardstate is False:
                castle_short, castle_long = self.check_castling(los, lop)
                short_square = get_square_at(dx-200, dy, los)
                long_square = get_square_at(dx+200, dy, los)

                for square in los:
                    sx, sy = name_of_squares[f"{square.name}"]
                    square_color = WHITE if (sx + sy)/100 % 2 == 0 else BLACK
                    square.color = square_color

                if castle_short is True:
                    short_square.color = HIGHLIGHT
                if castle_long is True:
                    long_square.color = HIGHLIGHT


            #Uses a while loop to continue highlighting squares until it hits an obstacle
            king_and_queen_directions = [(1,1),(1,0),(1,-1),(-1,1),(-1,-1),(-1,0),(0,1),(0,-1)]
            for dr in king_and_queen_directions:
                self.hightlight_squares_in_direction(dr[0], dr[1], los, temp_boardstate)

    def hightlight_squares_in_direction(self, dx, dy, los, temp_boardstate):
        """Highlights unobstructed moves for bishop, rook, and queen""" 

        x, y = self.coords
        distance = 100
        while True:

            #finds destination square
            x_new, y_new = x + distance * dx, y + distance * dy
            distance += 100
            square = get_square_at(x_new, y_new, los)
            #check if temp_board state
            if temp_boardstate is False:
                #breaks if move is impossible
                if square is None:
                    break

                if square.current_piece and square.current_piece.color == self.color:
                    break


                #runs test to see if move would leave you in check
                else:
                    check = self.test_boardstate(square)

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

        
    def test_boardstate(self, square):
        """test new board state for check condition by iterating over enemy pieces
        saves the board as it is precheck and resets all highlighted square"""
        for bishop_square in l_o_s:
            if bishop_square.name == "d7":
                if bishop_square.current_piece:
                    print("Piece on d7:",bishop_square.current_piece.name)
        for pieces in l_o_p:
            if pieces.name == "Bishop":
                print(pieces.name, pieces.color)
                print(pieces.coords)
        current_boardstate = deep_copy_list(l_o_s)
        current_pieces = deep_copy_list(l_o_p)
        #place all pieces onto their squares
        #So current boardstate has pieces on it
        for piece in current_pieces:
            x,y = piece.coords            
            print(f"{piece.name} getting placed at {x}, {y}")
            x,y = piece.coords
            my_square = get_square_at(x, y, current_boardstate)
            if my_square:
                my_square.place_piece(piece)
        for bishop_square in current_boardstate:
            if bishop_square.name == "d7":
                if bishop_square.current_piece:
                    print("Piece on d7:",bishop_square.current_piece.name)
        if self.name == "Queen":
            print(f"Follows is a board state test for Queen to {square.name}")

        sx, sy = self.coords
        destination_x, destination_y = name_of_squares[f"{square.name}"]
        #Get the square the piece is currently on
        current_square = get_square_at(sx, sy, current_boardstate)
        temp_piece = current_square.current_piece

        #Very importantly remove the piece from its current square
        current_square.remove_piece()

        #gets the temp. destination square
        temp_square = get_square_at(destination_x, destination_y,current_boardstate)
        temp_square.place_piece(temp_piece)

        #Removes enemy piece from destination square
        if temp_square.current_piece:
            temp_square.capture_piece()

        #Update the position of the piece
        temp_piece.coords = (destination_x, destination_y)
        temp_piece.rect = pygame.Rect(destination_x, destination_y, 100, 100)

        #place the temp. piece onto the temp. destination square.
        temp_square.place_piece(temp_piece)

        print(temp_square.current_piece.name)
        for square in current_boardstate:
            if square.name == "e8":
                print(square.color)
        #removes any highlighted squares
        for colored_square in current_boardstate:
            cx, cy = name_of_squares[f"{colored_square.name}"]
            temp_square.color = WHITE if ((cx / 100) + (cy / 100)) % 2 == 0 else BLACK

        #Highlight all enemy moves
        list_of_enemy_moves = []
        for square in current_boardstate:

            if square.current_piece is not None and square.current_piece.color != self.color:
                #Highlights all possible enemy moves
                square.current_piece.highlight_moves(current_boardstate, current_pieces, True)

                #examine the results of highlight moves    
                for square in current_boardstate:
                    if square.color == HIGHLIGHT and square not in list_of_enemy_moves:
                        list_of_enemy_moves.append(square)

        for square in current_boardstate:
            if square.current_piece and square.current_piece.name == "King" and square.current_piece.color == self.color:
                kings_square = square


        #destroys the temp piece
        #No reason I think?
        temp_piece.rect = pygame.Rect(1000, 1000, 100, 100)

        print(kings_square.name, kings_square.color)
        #tests if the square is highlighted if so it returns in_check = True
        if kings_square in list_of_enemy_moves:
            return True
        else:
            return False
