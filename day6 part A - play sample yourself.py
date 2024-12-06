import curses

# Movement deltas for directions
movement = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

directions = ["UP", "RIGHT", "DOWN", "LEFT"]  # Direction order for 90-degree rotation

class Game:
    def __init__(self, game_board_data):
        """
        Initializes the game, dynamically finding the starting position and direction.
        
        :param game_board_data: List of strings representing the board layout.
        """
        self.game_board = [list(row) for row in game_board_data.strip().split('\n')]
        self.height = len(self.game_board)
        self.width = len(self.game_board[0])
        
        # Find the starting position and direction
        self.player_pos, self.direction_index = self.find_starting_position()
        
        self.visited_positions = set()
        self.steps = 0
        self.new_steps = 0

    def find_starting_position(self):
        """Find the player's starting position and direction based on the symbol ('^', '>', 'v', '<')."""
        for i, row in enumerate(self.game_board):
            for j, cell in enumerate(row):
                if cell in '^>v<':  # The player symbol
                    # Determine the initial direction
                    direction_index = '^>v<'.index(cell)
                    return (i, j), direction_index
        return (0, 0), 0  # Default fallback in case no player symbol is found

    def render(self, stdscr):
        """Renders the current state of the game board to the screen."""
        stdscr.clear()

        # Get the terminal size
        terminal_height, terminal_width = stdscr.getmaxyx()

        # Render only the portion of the board that fits in the terminal window
        for i in range(min(self.height, terminal_height)):
            for j in range(min(self.width, terminal_width)):
                # Ensure we're not accessing out-of-bounds cells
                if i < self.height and j < self.width:
                    cell = self.game_board[i][j]

                    if len(cell) == 1:  # Ensure that 'cell' is a valid character
                        stdscr.addch(i, j, cell)
                    else:
                        stdscr.addch(i, j, '.')  # Default character in case of invalid cell

        stdscr.refresh()



    def move_player(self):
        """Moves the player based on the current direction and updates the game state."""
        dx, dy = movement[directions[self.direction_index]]
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if (new_x, new_y) not in self.visited_positions:
            self.new_steps += 1
            self.visited_positions.add((new_x, new_y))

        # Check if the player moved off the board
        if not (0 <= new_x < self.height and 0 <= new_y < self.width):
            return False  # Game over, out of bounds
        # Check if the move is valid (not hitting an obstacle)
        elif self.game_board[new_x][new_y] != '#':
            # Clear previous position
            self.game_board[self.player_pos[0]][self.player_pos[1]] = '.'
            # Move player to the new position
            self.game_board[new_x][new_y] = '^>v<'[self.direction_index]
            self.player_pos = (new_x, new_y)
        else:
            # Rotate direction by 90 degrees if movement is blocked
            self.direction_index = (self.direction_index + 1) % 4
        return True

    def get_steps(self):
        """Returns the number of distinct steps the player has taken."""
        return self.new_steps

def play_game(stdscr, game):
    """Main game loop using curses to display the game."""
    # Disable cursor and enable instant key detection
    curses.curs_set(0)
    stdscr.clear()

    while True:
        game.render(stdscr)  # Render the board

        key = stdscr.getch()

        # Get user input for direction change
        if key == curses.KEY_UP:
            game.direction_index = 0
        elif key == curses.KEY_RIGHT:
            game.direction_index = 1
        elif key == curses.KEY_DOWN:
            game.direction_index = 2
        elif key == curses.KEY_LEFT:
            game.direction_index = 3

        # Move player
        if not game.move_player():
            break  # Game over if the player moves off the board

    # Game over, show steps taken
    stdscr.clear()
    stdscr.addstr(0, 0, f"Game Over! You took {game.get_steps() - 1} steps.")
    stdscr.addstr(2, 0, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

def start_game(game_board_data):
    """
    Starts the game by initializing the board and running the game loop.
    
    :param game_board_data: List of strings representing the board layout.
    """
    game = Game(game_board_data)
    curses.wrapper(play_game, game)

#with open("day6-data.txt", 'r') as f:
#    game_board_data = f.read()
game_board_data = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''

start_game(game_board_data)