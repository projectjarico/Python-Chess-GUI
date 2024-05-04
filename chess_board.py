#Piece PNGs By en:User:Cburnett - File:Chess rdt45.svg, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=20363786
"""This file creates the chess board including starting squares and pieces"""
import os
import pygame
import copy 
count = 1
HIGHLIGHT = (55,25,20)


WHITE = (200,200,200)
BLACK = (50,50,50)


def deep_copy_list(list_to_copy):
    new_list = []
    for square in list_to_copy:
        new_square = square.__deepcopy__()
        new_list.append(new_square)
    return new_list



def get_square_at(x, y, list_of_squares):
    for square in list_of_squares:
        if square.x_pos == x and square.y_pos == y:
            return square

class ChessBoard:
    """This object represents the board and hold info about piece positions and game state"""
    def __init__(self):
        """Set the board"""
        self.height = 8
        self.width = 8
        self.list_of_squares, self.list_of_pieces = self.create_board()


    def create_board(self):
    #Creates 64 squares
        list_of_squares, list_of_pieces, names_of_squares = [], [], []

        #names the squares created below
        files = "abcdefgh"
        files = list(files)
        for file in files:
            ranks = list(range(1,9))
            ranks.reverse()
            for rank in ranks: 
                names_of_squares.append(f"{file}{rank}")

        print(len(names_of_squares))

        for i in range(8):
            for j in range(8):
                x = i * 100
                y = j * 100
                square_color = WHITE if (i + j) % 2 == 0 else BLACK
                name = names_of_squares.pop()


            
                #creates 24 pieces
                #assigns each piece its square then appends all squares and pieces into their list
                if y == 100:
                    piece_color = "white"
                    new_piece = ChessPiece(x, y, piece_color,"Pawn")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif y == 600:
                    piece_color = "black"
                    new_piece = ChessPiece(x, y, piece_color,"Pawn")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif (x == 0 or x == 700) and (y == 0 or y == 700):
                    if y == 0:
                        piece_color = "white"
                    else:
                        piece_color = "black"
                    new_piece = ChessPiece(x, y, piece_color,"Rook")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif (x == 100 or x == 600) and (y == 0 or y == 700):
                    if y == 0:
                        piece_color = "white"
                    else:
                        piece_color = "black"            
                    new_piece = ChessPiece(x, y, piece_color,"Knight")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif (x == 200 or x == 500) and (y == 0 or y == 700):
                    if y == 0:
                        piece_color = "white"
                    else:
                        piece_color = "black"            
                    new_piece = ChessPiece(x, y, piece_color,"Bishop")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x == 400 and  (y == 0 or y == 700):
                    if y == 0:
                        piece_color = "white"
                    else:
                        piece_color = "black"            
                    new_piece = ChessPiece(x, y, piece_color,"Queen")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                elif x == 300 and (y == 0 or y == 700):
                    if y == 0:
                        piece_color = "white"
                    else:
                        piece_color = "black"            
                    new_piece = ChessPiece(x, y, piece_color,"King")
                    square = ChessSquare(x, y, square_color, name)
                    square.place_piece(new_piece)
                else:
                    square = ChessSquare(x, y, square_color, name)
                list_of_squares.append(square)
                list_of_pieces.append(new_piece)
                list_of_squares.reverse()
        return list_of_squares, list_of_pieces

class ChessSquare:
    """Represents a chess square and any relevent info about it"""
    def __init__(self, x, y, color, name, rect = True):
        self.color = color
        if rect:
            self.rect = pygame.Rect(x, y, 100, 100)
        self.name = name
        self.x_pos = x
        self.y_pos = y
        self.current_piece = None

    def __deepcopy__(self):
        # Create a new instance of ChessSquare without copying the rect attribute
        new_square = ChessSquare(self.x_pos, self.y_pos, self.color, True)
        return new_square        

    def draw(self, win):
        """displays the square on screen"""
        pygame.draw.rect(win, self.color, self.rect)

    def place_piece(self, piece):
        self.current_piece = piece

    def capture_piece(self, list_of_pieces):
        if self.current_piece:
            self.current_piece.rect = pygame.Rect(-100,-100,0,0)
            list_of_pieces.remove(self.current_piece)
        
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
        self.piece_image = pygame.image.load(f"c:\\Users\\Jack\\Chess\\{self.color}_{self.name}.PNG")
        self.rect = pygame.Rect(x_pos, y_pos, 100, 100)

    def draw_piece(self, win, scale_factor = 1.5):
        """Displays the piece inside the square"""
        piece_rect = self.piece_image.get_rect(center=self.rect.center)
        win.blit(self.piece_image, piece_rect)

    def __deepcopy__(self):
        # Create a new instance of ChessPiece
        new_piece = ChessPiece(self.x_pos, self.y_pos, self.color, self.name)
        return new_piece  


    def highlight_moves(self, list_of_squares, list_of_pieces, temp_boardstate = False):

        """Called when a chess piece is clicked highlight all the legal moves for the piece clicked"""
        count = 1
        if self.name == "Pawn":
            direction = 1 if self.color == "white" else -1
            # Check if the square in front of the pawn is empty and highlight it
            if temp_boardstate == False:
                square = get_square_at(self.x_pos, self.y_pos + direction * 100, list_of_squares)     
                count += 1           
                check = self.test_boardstate(square, list_of_squares, list_of_pieces)
                if check != True and square and square.current_piece is None:
                    square.color = HIGHLIGHT
 

            #Check if the square two steps in front of the pawn is empty and highlight it
            if temp_boardstate == False:
                if self.y_pos == 100 or self.y_pos == 600:
                    square = get_square_at(self.x_pos, self.y_pos + direction * 200, list_of_squares)
                count += 1
                     
                check = self.test_boardstate(square, list_of_squares, list_of_pieces)
                if  square and square.current_piece is None and check != True:
                    square.color = HIGHLIGHT


            # Check if the diagonally forward squares have opponent's pieces and highlight them
            if temp_boardstate == False:
                #if player move is being considered it checks the legality of the move
                square1 = get_square_at(self.x_pos - 100, self.y_pos + direction * 100, list_of_squares)
                square2 = get_square_at(self.x_pos + 100, self.y_pos + direction * 100, list_of_squares)
                if square1 and square1.current_piece and square1.current_piece.color != self.color:
                    print("Oops #1")
                    check = self.test_boardstate(square1, list_of_squares, list_of_pieces)            
                    if check != True:
                        square.color = HIGHLIGHT
                        
                if square and square2.current_piece and square2.current_piece.color != self.color:
                    print("Oops #2")
                    check = self.test_boardstate(square1, list_of_squares, list_of_pieces)            
                    if check != True:
                        square.color = HIGHLIGHT

            else:
                #if enemy move is being considered it hightlights all possible moves
                square = get_square_at(self.x_pos - 100, self.y_pos + direction * 100, list_of_squares)      
                if square and square.current_piece and square.current_piece.color != self.color:
                    square.color = HIGHLIGHT
                square = get_square_at(self.x_pos + 100, self.y_pos + direction * 100, list_of_squares)
                if square and square.current_piece and square.current_piece.color != self.color:
                    square.color = HIGHLIGHT


        if self.name == "Rook":
            """Uses a while loop to continue highlighting squares until it hits an obstacle"""
            self.hightlight_squares_in_direction(0, 1, list_of_squares, temp_boardstate, list_of_pieces) #Up
            self.hightlight_squares_in_direction(0, -1, list_of_squares, temp_boardstate, list_of_pieces) #Down
            self.hightlight_squares_in_direction(-1, 0, list_of_squares, temp_boardstate, list_of_pieces) #Left
            self.hightlight_squares_in_direction(1, 0, list_of_squares, temp_boardstate, list_of_pieces) #Right

        if self.name == "Bishop":
            "Uses a while loop to continue highlighting squares until it hits an obstacle"
            self.hightlight_squares_in_direction(1, 1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(1, -1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(-1, 1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(-1, -1, list_of_squares, temp_boardstate, list_of_pieces)

        if self.name == "Queen":
            "Uses a while loop to continue highlighting squares until it hits an obstacle"
            self.hightlight_squares_in_direction(1, 1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(1, -1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(-1, 1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(-1, -1, list_of_squares, temp_boardstate, list_of_pieces)            
            self.hightlight_squares_in_direction(0, 1, list_of_squares, temp_boardstate, list_of_pieces) 
            self.hightlight_squares_in_direction(0, -1, list_of_squares, temp_boardstate, list_of_pieces) 
            self.hightlight_squares_in_direction(-1, 0, list_of_squares, temp_boardstate, list_of_pieces) 
            self.hightlight_squares_in_direction(1, 0, list_of_squares, temp_boardstate, list_of_pieces) 

        if self.name == "King":
            "Uses a while loop to continue highlighting squares until it hits an obstacle"
            self.hightlight_squares_in_direction(1, 1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(1, -1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(-1, 1, list_of_squares, temp_boardstate, list_of_pieces)
            self.hightlight_squares_in_direction(-1, -1, list_of_squares, temp_boardstate, list_of_pieces)            
            self.hightlight_squares_in_direction(0, 1, list_of_squares, temp_boardstate, list_of_pieces) 
            self.hightlight_squares_in_direction(0, -1, list_of_squares, temp_boardstate, list_of_pieces) 
            self.hightlight_squares_in_direction(-1, 0, list_of_squares, temp_boardstate, list_of_pieces) 
            self.hightlight_squares_in_direction(1, 0, list_of_squares, temp_boardstate, list_of_pieces) 

    def hightlight_squares_in_direction(self, dx, dy, list_of_squares, temp_boardstate, list_of_pieces):
        """Highlights unobstructed moves for bishop, rook, and queen""" 

        x, y = self.x_pos, self.y_pos
        distance = 100
        while True:

            #finds destination square 
            x_new, y_new = x + distance * dx, y + distance * dy
            distance += 100
            square = get_square_at(x_new, y_new, list_of_squares)
            #check if temp_board state
            if temp_boardstate == False:
                #breaks if move is impossible
                if square is None:
                    break

                elif square.current_piece and square.current_piece.color == self.color:
                    break

                elif square.current_piece and square.current_piece.color == self.color:
                    break

                #runs test to see if move would leave you in check
                else:
                    check = self.test_boardstate(square, list_of_squares, list_of_pieces)

                if square.current_piece is None and check == False:
                    square.color = HIGHLIGHT
                    if self.name == "King":
                        break                

                elif square.current_piece and square.current_piece.color != self.color and check == False:
                    square.color = HIGHLIGHT
                    break
                else:
                    continue

            #highlights squares while calculating enemy moves
            if temp_boardstate == True:
                
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
        
    def test_boardstate(self, square, list_of_squares, list_of_pieces):
        #test new board state for check condition by iterating over enemy pieces
        #saves the board as it is precheck and resets all highlighted square       
        current_boardstate = deep_copy_list(list_of_squares)
        current_pieces = deep_copy_list(list_of_pieces)

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


        print(square.x_pos, square.y_pos)
        temp_square = get_square_at(square.x_pos, square.y_pos,current_boardstate)
        temp_square.place_piece(temp_piece)


        #Testing post capture
        print("Testing boardstate",f"{temp_piece.name}", temp_square.x_pos, temp_square.y_pos)
        test_square = get_square_at(300, 600, current_boardstate)
        if test_square == temp_square:
            print("Testing move to e7")



        #removes any highlighted squares
        for temp_square in current_boardstate:
            temp_square.color = WHITE if ((temp_square.x_pos / 100) + (temp_square.y_pos / 100)) % 2 == 0 else BLACK
        


        #Update the position of the piece
        temp_piece.rect = pygame.Rect(temp_piece.x_pos, temp_piece.y_pos, 100, 100)
        temp_piece.y_pos = square.y_pos
        temp_piece.x_pos = square.x_pos



        #Highlight all enemy moves
        list_of_enemy_moves = []
        test_square = get_square_at(300, 600, current_boardstate)
        if test_square.current_piece:
            print(test_square.current_piece.name)
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
        for square in list_of_squares:
            if square.current_piece and square.current_piece.name == "King" and square.current_piece.color == self.color:
                my_king = square.current_piece

        #gets square king is on
        kings_square = get_square_at(my_king.x_pos, my_king.y_pos, current_boardstate)


        #destroys the temp piece
        temp_piece.rect = pygame.Rect(1000, 1000, 100, 100)


        #tests if the square is highlighted if so it returns in_check = True
        print(len(list_of_enemy_moves))
        if kings_square in list_of_enemy_moves:
            return True
        else:
            return False        