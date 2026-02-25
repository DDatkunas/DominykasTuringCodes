def main():
# We need to initialize the board first
# The board is a dictionary - where positions are keys and pieces are values
# Then we print a visual of an empty board
    board = {}
    print_board(board)

# We will use loops to ask for piece input
# Loop is necessary even while entering a single white piece in order to repeat a question if the input is invalid
    piece_count = 0
    while piece_count < 1:

    # We will strip whitespace and convert an input to lowercase, to make this program more useable        
        input_str = input("Enter a white piece and position (ex. pawn e4): ").strip().lower()
    # parse_piece_input function returns a tuple of (piece, position) if both the piece and position are valid
    # Otherwise, it returns "None"
        parts = parse_piece_input(input_str)
        
    # If both piece and position are valid, we can split the tuple 
    # and add that the color of the piece is white
        if parts is not None:
            piece, position = parts
            color = "white"
        # We add the piece to the board, print the message that the piece has been added
        # We also reprint the vizualition of the board and close the loop
        # Because the board is currently empty, we'll be able to add a piece to any valid position
            add_piece(board, piece, position, color)
            print(f"{color.title()} {piece} added!")
            print_board(board)
            piece_count += 1

    # If the piece and/or position is invalid, we print a message and ask for input again
        else:
            print("Invalid input, try again.")

# We make another loop for entering black pieces
    piece_count = 0
    while piece_count <= 16:
    
    # We can enter 16 black pieces at most, therefore, this condition closes the loop automatically
        if piece_count == 16:
            print("Maximum limit of black pieces reached!")
            print("Analyzing position...")
            break
        
        elif piece_count == 0:
            input_str = input("Enter a black piece and position (ex. pawn e5): ").strip().lower()
        elif piece_count > 0: 
            input_str = input("Enter a black piece and position (ex. pawn e5). Type 'done' to get results: ").strip().lower()

    # We can type a word "done" to stop the loop and skip to the results if at least 1 black piece is entered
        if input_str == "done":
            if piece_count < 1:
                print("You have to enter at least one black piece!")
                continue
            else:
                print("Analyzing position...")
                break

        parts = parse_piece_input(input_str)

    # If both piece and position are valid, we can split the tuple 
    # and add that the color of the piece is black
        if parts is not None:
            piece, position = parts
            color = "black"
        # Because the board is not empty, we need an extra check to see if the position is occupied by another pieces 
            if add_piece(board, piece, position, color):
                print(f"{color.title()} {piece} added!")
                print_board(board)
                piece_count += 1

    # Two possible error messages when entering black pieces - either position is occupied or input is invalid
            else:
                print("Position occupied by another piece, try again.")
        else: 
            print("Invalid input, try again.")
    
# To calculate which black pieces can a white piece capture, first we need a loop 
# which checks all pieces on the board, if it's a white piece 
    for white_pos, white_piece in board.items():
    # If the piece is white, we use get_capturable_pieces function to return a list of possible captures
        if white_piece.startswith("white"):
            captures = get_capturable_pieces(board, white_piece, white_pos)
        # Final print message depends on whether we get a list of capturable pieces
            if captures:
                print(f"The {white_piece} at {white_pos} can capture: {', '.join(sorted(captures))}.")
            else:
                print("No captures available on the board.")



def is_valid_piece(piece):
# I made a list of all valid pieces. If the entry is in the list, function returns as true
    valid_pieces = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    if piece in valid_pieces:
        return True
    else:
        return False

def is_valid_position(position):
# There 3 criteria for a valid position: length of string, a certain letter and a certain number
# If all 3 criteria are fulfilled, function returns as true
    if len(position) != 2:
        return False
    elif position[0] not in "abcdefgh":
        return False
    elif position[1] not in "12345678":
        return False
    else:
        return True

def parse_piece_input(input_str):
# First we make a variable that splits an input string into parts
# If we get anything else than 2 parts, the input is invalid
    parts = input_str.split()
    if len(parts) != 2:
        return None

# Only after checking the length of "parts" variable we can split it into piece and position
    piece, position = parts

# We run validity checks for both the piece and position
# We both are valid, we return a tuple
    if is_valid_piece(piece) and is_valid_position(position):
        return (piece, position)
    else:
        return None

def add_piece(board, piece, position, color): 
    if not is_valid_piece(piece) or not is_valid_position(position):
        return False
    
# We need to check if the position is occupied. If it is, function returns as false     
    if position in board:
        return False
    
# If the position is empty, we add the piece to the board 
# with the color name, which gets assigned in the main function
# Because later on we will check which black pieces can a white piece captures, adding a color name is necessary
    else:
        board[position] = f"{color} {piece}"
        return True

def get_pawn_captures(position, board):
# We will return a list of all position where a white pawn can capture a black piece
# First of all, we make a variable "captures" which is currently an empty list
    captures = []
    
# We need to make separate variables for column and row of the position of this white pawn
    if not is_valid_position(position):
        return []
    col = position[0]
    row = position[1]

# Then we have make variables of the position that this pawn can target
# t_row stands for target row
    target_row = int(row) + 1

# To calculate target columns, we convert the letter to a unicode number, add or subtract 1
# And reconvert it to a character   
    target_left_col = chr(ord(col) - 1)
    target_right_col = chr(ord(col) + 1)

# A pawn has 2 possible target positions
# To check for both, we make a "for" loop and add each target column to a target row
    for target_col in [target_left_col, target_right_col]:
        target_pos = f"{target_col}{target_row}"
    # If we found a capturable piece we add the position to a "captures" list
    # We also have to check if the target position is valid
        if is_valid_position(target_pos) and target_pos in board:
            captures.append(target_pos)

# We return the list of possible captures
    return captures

def get_rook_captures(position, board):
    captures = []
    
    if not is_valid_position(position):
        return []
    col = position[0]
    row = position[1]

# A rook can move only in one direction. We make a list of possible 1 square moves as a tuple (col, row)
    moves = [(1, 0), (-1, 0), 
             (0, 1), (0, -1)]

# Because the rook can move in multiple squares, we need to make a nested loop which will check
# for a target in the next square in the same direction
    for move in moves:
    # Before the begin the nested loop, we set target column the row to be the same as the starting position
        target_col = ord(col)
        target_row = int(row)
    # We use "while" loop because we want the loop to continue as long as the position is valid
    # Or as long as our program finds the target
        while True:
            target_col += move[0]
            target_row += move[1]
            target_pos = f"{chr(target_col)}{target_row}"
            if not is_valid_position(target_pos):
                break
        # If the program finds the target, we want the loop to break because the rook can't jump over pieces
            elif target_pos in board:
                captures.append(target_pos)
                break
    
    return captures

def get_knight_captures(position, board):
    captures = []
    
    if not is_valid_position(position):
        return []
    col = position[0]
    row = position[1]

# We make a list of moves as a tuple (col, row)    
    moves = [(1, 2), (1, -2),
             (-1, 2), (-1, -2),
             (2, 1), (2, -1),
             (-2, 1), (-2, -1)]
    
# We make a loop which checks if there is a target in one of the 8 squares a knight can move in
    for move in moves:
        target_col = chr(ord(col) + move[0])
        target_row = int(row) + move[1]
        target_pos = f"{target_col}{target_row}"
        if is_valid_position(target_pos) and target_pos in board:
            captures.append(target_pos)
    
    return captures

def get_bishop_captures(position, board):
# Code is exactly the same as in get_rook_captures, only moves list is different
    captures = []

    if not is_valid_position(position):
        return []
    col = position[0]
    row = position[1]

    moves = [(1, 1), (1, -1), 
             (-1, 1), (-1, -1)]
    
    for move in moves:
        target_col = ord(col)
        target_row = int(row)
        while True:
            target_col += move[0]
            target_row += move[1]
            target_pos = f"{chr(target_col)}{target_row}"
            if not is_valid_position(target_pos):
                break
            elif target_pos in board:
                captures.append(target_pos)
                break
    
    return captures

def get_queen_captures(position, board):
# Code is exactly the same as in get_rook_captures, only moves list is different
    captures = []

    if not is_valid_position(position):
        return []
    col = position[0]
    row = position[1]

    moves = [(1, 1), (1, -1), 
             (-1, 1), (-1, -1),
             (1, 0), (-1, 0), 
             (0, 1), (0, -1)]
    
    for move in moves:
        target_col = ord(col)
        target_row = int(row)
        while True:
            target_col += move[0]
            target_row += move[1]
            target_pos = f"{chr(target_col)}{target_row}"
            if not is_valid_position(target_pos):
                break
            elif target_pos in board:
                captures.append(target_pos)
                break
    
    return captures

def get_king_captures(position, board):
# Code is exactly the same as in get_knight_captures, only moves list is different
    captures = []
    
    if not is_valid_position(position):
        return []
    col = position[0]
    row = position[1]
    
    moves = [(1, 1), (1, 0),
             (1, -1), (0, 1),
             (0, -1), (-1, 1),
             (-1, 0), (-1, -1)]
    
    for move in moves:
        target_col = chr(ord(col) + move[0])
        target_row = int(row) + move[1]
        target_pos = f"{target_col}{target_row}"
        if is_valid_position(target_pos) and target_pos in board:
            captures.append(target_pos)
    
    return captures

def get_capturable_pieces(board, white_piece, white_pos):
# First, we need a dictionary with all of the white pieces as keys and all capture functions as values
# It lets us call the relevant captures function for a specific white piece
    white_pieces = {
        "white pawn": get_pawn_captures,
        "white knight": get_knight_captures,
        "white bishop": get_bishop_captures,
        "white rook": get_rook_captures,
        "white queen": get_queen_captures,
        "white king": get_king_captures
    }

    attacking_piece = white_pieces.get(white_piece)
    if attacking_piece:
    # Then we get a list of positions on the board, the attacking piece can target
        targets = attacking_piece(white_pos, board)
        if targets:
            capturable_pieces = []
        # We create a loop to check target position in the list
        # The we find which black piece is being targetted
        # And return a list
            for target_pos in targets:
                target_piece = board[target_pos].replace("black ", "")
                capturable_pieces.append(f"{target_piece} at {target_pos}")
            return capturable_pieces

def print_board(board):
# We make a dictionary with pieces as keys and symbols as values
# Because our add_piece function outputs as f"{color} {piece}"
# We can make a single dictionary and not a dictionary of dictionaries as in optional task
    symbols = {
        "white pawn": "♙", "white rook": "♖", "white knight": "♘",
        "white bishop": "♗", "white queen": "♕", "white king": "♔",
        "black pawn": "♟", "black rook": "♜", "black knight": "♞",
        "black bishop": "♝", "black queen": "♛", "black king": "♚"
    }

    print("\n")
# We start printing cells from 8 in a descending order, as are cells organized in a real chess board
    for row in range(8, 0, -1):
    # We create a variable "cell" which will first print a number of the row
        cell = f"{row} |"
        for col in "abcdefgh":
        # We begin the nested loop by creating a variable of position name
            position = f"{col}{row}"
        # If the position is in board, we add a symbol of the piece
        # And add it to our "cell" variable
            if position in board:
                piece = board[position]
                symbol = symbols[piece]
                cell += symbol + " |"
        # If the position is empty, it just adds a visualization of an empty cell
            else:
                cell += "__|"
    # After all of the columns in the row have been checked, we print entire row
        print(cell)
    print("   a  b  c  d  e  f  g  h\n")

main()