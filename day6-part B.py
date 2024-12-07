from collections import defaultdict

# Movement deltas for directions
movement = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

# Directions in order for 90-degree rotation
directions = ["UP", "RIGHT", "DOWN", "LEFT"]

class Game:
    def __init__(self, game_board_data):
        self.original_board = [list(row) for row in game_board_data.strip().split('\n')]
        self.height = len(self.original_board)
        self.width = len(self.original_board[0])
        if any(len(row) != self.width for row in self.original_board):
            raise ValueError("Game board rows must all have the same length.")
        self.reset()
    
    def reset(self):
        """Reset the game to its initial state."""
        self.game_board = [row[:] for row in self.original_board]
        self.height = len(self.game_board)
        self.width = len(self.game_board[0]) if self.height > 0 else 0
        self.player_pos, self.direction_index = self.find_starting_position()
        self.visited_positions = set()  # Tracks unique steps
        self.visited_positions.add(self.player_pos)  # Add starting position to visited
        return self.get_state()

    def step(self):
        """Move the player based on the current direction. Rotate if encountering an obstacle."""
        dx, dy = movement[directions[self.direction_index]]
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if not (0 <= new_x < self.height and 0 <= new_y < self.width):
            return self.get_state(), True  # Out of bounds, game over
        
        if self.game_board[new_x][new_y] == '#':
            # Rotate right (clockwise) by 90 degrees
            self.direction_index = (self.direction_index + 1) % 4
            return self.get_state(), False  # Continue without moving
        
        # Update the player's position
        self.game_board[self.player_pos[0]][self.player_pos[1]] = '.'
        self.game_board[new_x][new_y] = '^>v<'[self.direction_index]
        self.player_pos = (new_x, new_y)
        
        # Mark the new position as visited
        self.visited_positions.add(self.player_pos)
        
        done = False
        
        # Check if the game is over (e.g., if all positions are visited or the player hits an obstacle)
        if len(self.visited_positions) >= self.width * self.height:
            done = True
        
        return self.get_state(), done

    def find_starting_position(self):
        """Find the player's starting position and direction based on the symbol ('^', '>', 'v', '<')."""
        for i, row in enumerate(self.game_board):
            for j, cell in enumerate(row):
                if cell in '^>v<':  # The player symbol
                    direction_index = '^>v<'.index(cell)
                    return (i, j), direction_index
        return (0, 0), 0  # Default fallback if no player symbol is found
    
    def get_state(self):
        """Returns a simplified state representation of the board and player's position."""
        return (self.player_pos[0], self.player_pos[1], self.direction_index)


class RuleBasedAgent:
    def __init__(self, game):
        self.game = game
        self.unique_obstacle_positions = set()
        self.print_counter = defaultdict(int)

    def simulate_game_with_obstacle(self, obstacle_position):
        """Simulate the game with a specific obstacle to check for loops."""
        self.game.reset()  # Ensure the board is reset before placing the obstacle
        self.game.game_board[obstacle_position[0]][obstacle_position[1]] = '#'  # Place the obstacle
        visited_states = set()
        state = self.game.get_state()  # Get the initial state after placing the obstacle
        done = False

                # Only print a value if it has been printed fewer than 3 times
        if self.print_counter[len(self.unique_obstacle_positions)] < 3:
            print(len(self.unique_obstacle_positions))
            self.print_counter[len(self.unique_obstacle_positions)] += 1

        while not done:
            if state in visited_states:
                self.game.reset()  # Reset after detecting a loop
                return True  # Loop detected
            visited_states.add(state)
            state, done = self.game.step()
        
        self.game.reset()  # Ensure the board is reset for the next test
        return False  # No loop detected


    def find_all_loop_positions(self, runs=1000):
        """Simulate multiple games and find all positions where an obstacle causes a loop."""
        for _ in range(runs):
            print(f"This is run {_} of {runs}.")
            for i in range(self.game.height):
                for j in range(self.game.width):
                    # Skip non-empty positions and the starting position
                    if self.game.original_board[i][j] == '.' and (i, j) != self.game.player_pos:
                        if self.simulate_game_with_obstacle((i, j)):
                            self.unique_obstacle_positions.add((i, j))
        
        return len(self.unique_obstacle_positions)


# Load the game board data
with open("day6-data.txt", 'r') as f:
    raw_data = f.read()

sample_raw_data = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''

# Preprocess to strip uneven rows and ensure uniform lengths
lines = [line.strip() for line in raw_data.split('\n') if line.strip()]  # Remove empty or whitespace-only lines
max_width = max(len(line) for line in lines)  # Find the longest row
game_board_full_data = '\n'.join(line.ljust(max_width, '.') for line in lines)  # Pad shorter rows with '.'

# Initialize the game and agent
game_full = Game(game_board_full_data)
agent_full = RuleBasedAgent(game_full)

# Run simulations
unique_loop_positions = agent_full.find_all_loop_positions(runs=1)
print(f"Number of unique loop-causing positions: {unique_loop_positions}")

#That's the right answer! You are one gold star closer to finding the Chief Historian.
#You have completed Day 6! You can [Share] this victory or [Return to Your Advent Calendar].