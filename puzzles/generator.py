import random
import string
from pathlib import Path
from typing import Dict, List, Union, Any
from dataclasses import dataclass


@dataclass
class PuzzleData:
    """Data structure for puzzle input/output pairs."""
    input: Union[List, str, int]
    output: Union[List, str, int]


class PuzzleGenerator:
    """Optimized puzzle generator with configurable parameters."""
    
    # Class constants
    LOWERCASE_LETTERS = string.ascii_lowercase
    ALPHANUMERIC = string.ascii_lowercase + string.digits
    DIRECTIONS = ['U', 'D', 'L', 'R']
    OPERATIONS = ["add", "sub"]
    
    # Direction mappings for efficient lookup
    DIRECTION_DELTAS = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0)
    }
    
    def __init__(self, output_dir: str = "./puzzles/outputs"):
        """Initialize generator with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def level1_frequency_beacon(self, num_variants: int = 5, 
                              min_word_len: int = 4, max_word_len: int = 7) -> PuzzleData:
        """Generate Level 1: Find the most frequent word variant."""
        word_length = random.randint(min_word_len, max_word_len)
        original_word = ''.join(random.choices(self.LOWERCASE_LETTERS, k=word_length))
        
        variants = []
        for _ in range(num_variants - 1):
            word_chars = list(original_word)
            idx_to_change = random.randrange(len(word_chars))
            original_char = word_chars[idx_to_change]
            
            # More efficient character replacement
            available_chars = self.LOWERCASE_LETTERS.replace(original_char, '')
            word_chars[idx_to_change] = random.choice(available_chars)
            variants.append(''.join(word_chars))
        
        # Insert original word at random position
        variants.insert(random.randrange(num_variants), original_word)
        return PuzzleData(variants, original_word)
    
    def level2_reactor_spike(self, min_size: int = 5, max_size: int = 15, 
                           min_val: int = 1, max_val: int = 10) -> PuzzleData:
        """Generate Level 2: Find the spike value in array."""
        size = random.randint(min_size, max_size)
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        
        if size >= 3:
            # Create spike at random position (not at edges)
            idx = random.randint(1, size - 2)
            spike_value = arr[idx - 1] + arr[idx + 1] + 1
            arr[idx] = spike_value
            output = spike_value
        else:
            output = -1
            
        return PuzzleData(arr, output)
    
    def level3_boot_sequence(self, min_cmds: int = 5, max_cmds: int = 10, 
                           min_val: int = 1, max_val: int = 20) -> PuzzleData:
        """Generate Level 3: Calculate final accumulator value."""
        acc = 0
        cmds = []
        num_cmds = random.randint(min_cmds, max_cmds)
        
        for _ in range(num_cmds):
            op = random.choice(self.OPERATIONS)
            val = random.randint(min_val, max_val)
            cmds.append(f"{op} {val}")
            acc += val if op == "add" else -val
            
        return PuzzleData(cmds, acc)
    
    def level4_cable_overlap(self, min_path_len: int = 3, max_path_len: int = 7) -> PuzzleData:
        """Generate Level 4: Find intersection point of two paths."""
        # Pre-determine intersection point
        intersection_x = random.randint(-5, 5)
        intersection_y = random.randint(-5, 5)
        
        def generate_path_to_point(target_x: int, target_y: int) -> List[str]:
            """Generate path from origin to target point."""
            path = []
            current_x, current_y = 0, 0
            
            while current_x != target_x or current_y != target_y:
                # Choose direction that moves toward target
                possible_moves = []
                for direction, (dx, dy) in self.DIRECTION_DELTAS.items():
                    new_x, new_y = current_x + dx, current_y + dy
                    # Prefer moves that get closer to target
                    if (abs(new_x - target_x) + abs(new_y - target_y) <= 
                        abs(current_x - target_x) + abs(current_y - target_y)):
                        possible_moves.append(direction)
                
                if not possible_moves:
                    possible_moves = list(self.DIRECTION_DELTAS.keys())
                
                direction = random.choice(possible_moves)
                distance = random.randint(1, 3)
                
                # Apply movement
                dx, dy = self.DIRECTION_DELTAS[direction]
                current_x += dx * distance
                current_y += dy * distance
                
                path.append(f"{direction}{distance}")
            
            return path
        
        path_a = generate_path_to_point(intersection_x, intersection_y)
        path_b = generate_path_to_point(intersection_x, intersection_y)
        
        return PuzzleData([path_a, path_b], [intersection_x, intersection_y])
    
    def level5_the_code(self, min_word_len: int = 6, max_word_len: int = 12) -> PuzzleData:
        """Generate Level 5: Transform string using position-based encoding."""
        word_length = random.randint(min_word_len, max_word_len)
        input_word = ''.join(random.choices(self.ALPHANUMERIC, k=word_length))
        
        # Optimized string transformation
        result = ''.join(str((ord(c) + i) % 10) for i, c in enumerate(input_word))
        return PuzzleData(input_word, result)
    
    def generate_all_levels(self) -> Dict[str, str]:
        """Generate all puzzle levels and save to files."""
        generators = {
            "level1": self.level1_frequency_beacon,
            "level2": self.level2_reactor_spike,
            "level3": self.level3_boot_sequence,
            "level4": self.level4_cable_overlap,
            "level5": self.level5_the_code,
        }
        
        files = {}
        for level_name, generator in generators.items():
            try:
                puzzle_data = generator()
                filepath = self.output_dir / f"{level_name}.txt"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"{puzzle_data.input}\n{puzzle_data.output}\n")
                
                files[level_name] = str(filepath)
                
            except Exception as e:
                print(f"Error generating {level_name}: {e}")
                continue
        
        return files
    
    def generate_level(self, level_name: str, **kwargs) -> PuzzleData:
        """Generate a specific level with custom parameters."""
        method_name = f"{level_name}_" + level_name.replace("level", "").strip()
        if hasattr(self, method_name):
            return getattr(self, method_name)(**kwargs)
        else:
            raise ValueError(f"Unknown level: {level_name}")


def main():
    """Main function to generate all puzzles."""
    generator = PuzzleGenerator()
    files = generator.generate_all_levels()
    
    print("Generated puzzle inputs and outputs in separate files:")
    for level, filepath in files.items():
        print(f"{level}: {filepath}")


if __name__ == "__main__":
    main()