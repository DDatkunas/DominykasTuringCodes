def main():
    """
    In this task the user inputs a single white chess piece 
    and up to 16 black pieces.

    The program shows which black pieces can 
    a white piece capture.
    """

    board = {}
    print_board(board)
    
    # White piece input
    piece_count = 0
    while piece_count < 1:
        input_str = input("Enter a white piece and position (ex. pawn e4): ").strip().lower()

        parts = parse_piece_input(input_str)
        
        if parts is not None:
            piece, position = parts
            color = "white"
            add_piece(board, piece, position, color)
            print(f"{color.title()} {piece} added!")
            print_board(board)
            piece_count += 1
        else:
            print("Invalid input, try again.")

    # Black piece input
    piece_count = 0
    while piece_count <= 16:
        if piece_count == 16:
            print("Maximum limit of black pieces reached!")
            print("Analyzing position...")
            break
        elif piece_count == 0:
            input_str = input("Enter a black piece and position (ex. pawn e5): ").strip().lower()
        elif piece_count > 0: 
            input_str = input("Enter a black piece and position (ex. pawn e5). Type 'done' to get results: ").strip().lower()

        if input_str == "done":
            if piece_count < 1:
                print("You have to enter at least one black piece!")
                continue
            else:
                print("Analyzing position...")
                break

        parts = parse_piece_input(input_str)

        if parts is not None:
            piece, position = parts
            color = "black"
            if add_piece(board, piece, position, color):
                print(f"{color.title()} {piece} added!")
                print_board(board)
                piece_count += 1
            else:
                print("Position occupied by another piece, try again.")
        else: 
            print("Invalid input, try again.")
    
# Analyze captures 
    for white_pos, white_piece in board.items():
        if white_piece.startswith("white"):
            captures = get_capturable_pieces(
                board, white_piece, white_pos
            )

            if captures:
                print(
                    f"The {white_piece} at {white_pos} can capture: "
                    f"{', '.join(sorted(captures))}."
                )
            else:
                print(
                    f"The {white_piece} at {white_pos} "
                    "has no captures available."
                )


def is_valid_piece(piece):
    """
    Return valid chess pieces
    """
    valid_pieces = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    return piece in valid_pieces

def is_valid_position(position):
    """
    Return valid chess position
    """
    return (
        len(position) == 2
        and position[0] in "abcdefgh"
        and position[1] in "12345678"
    )

def parse_piece_input(input_str):
    """
    Parse and validate user input
    """
    parts = input_str.split()

    if len(parts) != 2:
        return None

    piece, position = parts

    if is_valid_piece(piece) and is_valid_position(position):
        return (piece, position)
    
    return None

def add_piece(board, piece, position, color): 
    """
    Add piece to the board if piece and position is valid
    and if the position is free
    """
    
    if not (is_valid_piece(piece) and is_valid_position(position)):
        return False
        
    if position in board:
        return False
    
    else:
        board[position] = f"{color} {piece}"
        return True

def get_pawn_captures(position, board):
    captures = []

    if not is_valid_position(position):
        return []

    col = position[0]
    row = int(position[1])

    target_row = row + 1
    target_columns = [
        chr(ord(col) - 1),
        chr(ord(col) + 1),
    ]

    for target_col in target_columns:
        target_pos = f"{target_col}{target_row}"

        if is_valid_position(target_pos) and target_pos in board:
            captures.append(target_pos)

    return captures

def get_rook_captures(position, board):
    captures = []

    if not is_valid_position(position):
        return []

    col = position[0]
    row = int(position[1])

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for col_move, row_move in moves:
        target_col = ord(col)
        target_row = row

        while True:
            target_col += col_move
            target_row += row_move

            target_pos = f"{chr(target_col)}{target_row}"

            if not is_valid_position(target_pos):
                break

            if target_pos in board:
                captures.append(target_pos)
                break

    return captures

def get_knight_captures(position, board):
    captures = []

    if not is_valid_position(position):
        return []

    col = position[0]
    row = int(position[1])

    moves = [
        (1, 2), (1, -2),
        (-1, 2), (-1, -2),
        (2, 1), (2, -1),
        (-2, 1), (-2, -1),
    ]

    for col_move, row_move in moves:
        target_col = chr(ord(col) + col_move)
        target_row = row + row_move
        target_pos = f"{target_col}{target_row}"

        if is_valid_position(target_pos) and target_pos in board:
            captures.append(target_pos)

    return captures

def get_bishop_captures(position, board):
    captures = []

    if not is_valid_position(position):
        return []

    col = position[0]
    row = int(position[1])

    moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for col_move, row_move in moves:
        target_col = ord(col)
        target_row = row

        while True:
            target_col += col_move
            target_row += row_move

            target_pos = f"{chr(target_col)}{target_row}"

            if not is_valid_position(target_pos):
                break

            if target_pos in board:
                captures.append(target_pos)
                break

    return captures

def get_queen_captures(position, board):
    captures = []

    if not is_valid_position(position):
        return []

    col = position[0]
    row = int(position[1])

    moves = [
        (1, 1), (1, -1),
        (-1, 1), (-1, -1),
        (1, 0), (-1, 0),
        (0, 1), (0, -1),
    ]

    for col_move, row_move in moves:
        target_col = ord(col)
        target_row = row

        while True:
            target_col += col_move
            target_row += row_move

            target_pos = f"{chr(target_col)}{target_row}"

            if not is_valid_position(target_pos):
                break

            if target_pos in board:
                captures.append(target_pos)
                break

    return captures

def get_king_captures(position, board):
    captures = []

    if not is_valid_position(position):
        return []

    col = position[0]
    row = int(position[1])

    moves = [
        (1, 1), (1, 0),
        (1, -1), (0, 1),
        (0, -1), (-1, 1),
        (-1, 0), (-1, -1),
    ]

    for col_move, row_move in moves:
        target_col = chr(ord(col) + col_move)
        target_row = row + row_move
        target_pos = f"{target_col}{target_row}"

        if is_valid_position(target_pos) and target_pos in board:
            captures.append(target_pos)

    return captures

def get_capturable_pieces(board, white_piece, white_pos):
    """
    Returns the list of captures by using a relevant function
    for each white chess piece.
    """
    white_pieces = {
        "white pawn": get_pawn_captures,
        "white knight": get_knight_captures,
        "white bishop": get_bishop_captures,
        "white rook": get_rook_captures,
        "white queen": get_queen_captures,
        "white king": get_king_captures
    }

    attacking_piece = white_pieces.get(white_piece)

    if not attacking_piece:
        return []
    
    targets = attacking_piece(white_pos, board)

    capturable_pieces = []

    for target_pos in targets:
        target_piece = board[target_pos].replace("black ", "")
        capturable_pieces.append(f"{target_piece} at {target_pos}")
        
    return capturable_pieces

def print_board(board):
    """Print a visual representation of the chess board."""
    symbols = {
        "white pawn": "♙", "white rook": "♖", "white knight": "♘",
        "white bishop": "♗", "white queen": "♕", "white king": "♔",
        "black pawn": "♟", "black rook": "♜", "black knight": "♞",
        "black bishop": "♝", "black queen": "♛", "black king": "♚",
    }

    print()

    for row in range(8, 0, -1):
        line = f"{row} |"

        for col in "abcdefgh":
            position = f"{col}{row}"

            if position in board:
                piece = board[position]
                line += symbols[piece] + " |"
            else:
                line += "__|"

        print(line)

    print("   a  b  c  d  e  f  g  h\n")


if __name__ == "__main__":
    main()