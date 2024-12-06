import random

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
        self.game_board = [list(row) for row in game_board_data.strip().split('\n')]
        self.height = len(self.game_board)
        self.width = len(self.game_board[0])
        self.player_pos, self.direction_index = self.find_starting_position()
        self.visited_positions = set()  # Tracks unique steps
        self.visited_positions.add(self.player_pos)  # Add starting position to visited

    def reset(self):
        """Reset the game to its initial state."""
        self.visited_positions.clear()
        self.player_pos, self.direction_index = self.find_starting_position()
        self.visited_positions.add(self.player_pos)  # Add starting position to visited
        return self.get_state()

    def step(self):
        """Move the player based on the current direction. Rotate if encountering an obstacle."""
        dx, dy = movement[directions[self.direction_index]]
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if not (0 <= new_x < self.height and 0 <= new_y < self.width):
            return self.get_state(), -1, True  # Out of bounds, game over
        
        if self.game_board[new_x][new_y] == '#':
            # Rotate right (clockwise) by 90 degrees
            self.direction_index = (self.direction_index + 1) % 4
            return self.get_state(), -1, False  # Continue without moving
        
        # Update the player's position
        self.game_board[self.player_pos[0]][self.player_pos[1]] = '.'
        self.game_board[new_x][new_y] = '^>v<'[self.direction_index]
        self.player_pos = (new_x, new_y)
        
        # Mark the new position as visited
        self.visited_positions.add(self.player_pos)
        
        # Reward for a valid move
        reward = 1
        done = False
        
        # Check if the game is over (e.g., if all positions are visited or the player hits an obstacle)
        if len(self.visited_positions) >= self.width * self.height:
            done = True
        
        return self.get_state(), reward, done
    
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

    def get_unique_steps(self):
        """Returns the total number of unique steps (visited positions)."""
        return len(self.visited_positions)


class RuleBasedAgent:
    def __init__(self, game):
        self.game = game

    def play(self):
        state = self.game.reset()
        done = False
        while not done:
            # The agent moves strictly in the direction it is facing
            state, reward, done = self.game.step()
            print(f"Moved {directions[state[2]]} to position {state[:2]} - Reward: {reward}")
            
            if done:
                print("Game Over!")
                break
        
        # Print the total number of unique steps (positions visited)
        print(f"Total unique steps: {self.game.get_unique_steps()}")


# Example usage:
# game_board_sample_data = '''....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...'''

#game_sample = Game(game_board_sample_data)
#agent_sample = RuleBasedAgent(game_sample)

#agent_sample.play()

# Part A solution
with open("day6-data.txt", 'r') as f:
    game_board_full_data = f.read()

game_full = Game(game_board_full_data)
agent_full = RuleBasedAgent(game_full)

agent_full.play()

# That's the right answer! You are one gold star closer to finding the Chief Historian. [Continue to Part Two]