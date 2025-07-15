import random
import string
from pathlib import Path
from typing import Dict, List, Union
from dataclasses import dataclass


@dataclass
class PuzzleData:
    """Data structure for puzzle input/output pairs."""
    input: Union[List, str, int]
    output: Union[List, str, int]


class PuzzleGenerator:
    """Generates puzzle data for the 5-level coding challenge."""

    # Class constants for easy configuration
    LOWERCASE_LETTERS = string.ascii_lowercase
    ALPHANUMERIC = string.ascii_lowercase + string.digits
    # Updated to match the "Instruction Tangle" prompt
    OPERATIONS = ["inc", "dec"]

    def __init__(self, output_dir: str = "./puzzles/outputs"):
        """Initialize generator with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def level1_signal_noise(self, num_variants: int = 5,
                             min_word_len: int = 5, max_word_len: int = 8) -> PuzzleData:
        """
        Level 1: Signal Noise
        Find the most frequent character at each position in a list of strings.
        """
        word_length = random.randint(min_word_len, max_word_len)
        original_word = ''.join(random.choices(self.LOWERCASE_LETTERS, k=word_length))

        variants = [original_word] * 2  # Ensure original word is most common
        for _ in range(num_variants):
            word_chars = list(original_word)
            # Introduce a random number of errors
            for _ in range(random.randint(1, word_length // 2)):
                idx_to_change = random.randrange(word_length)
                original_char = word_chars[idx_to_change]
                available_chars = self.LOWERCASE_LETTERS.replace(original_char, '')
                word_chars[idx_to_change] = random.choice(available_chars)
            variants.append(''.join(word_chars))

        random.shuffle(variants)
        return PuzzleData(variants, original_word)

    def level2_energy_log_sorting(self, min_size: int = 7, max_size: int = 15,
                                  min_val: int = 1, max_val: int = 50) -> PuzzleData:
        """
        Level 2: Energy Log Sorting
        Find the index of the first element greater than both its neighbors.
        """
        size = random.randint(min_size, max_size)
        arr = [random.randint(min_val, max_val) for _ in range(size)]

        # Ensure at least one spike exists by creating one
        # Choose an index that is not on the edges
        spike_idx = random.randint(1, size - 2)
        
        # Make the value at spike_idx larger than its neighbors
        left_val = arr[spike_idx - 1]
        right_val = arr[spike_idx + 1]
        arr[spike_idx] = max(left_val, right_val) + random.randint(1, 10)

        # Find the first actual spike, which might not be the one we created
        # if the random generation already made one earlier.
        output_idx = -1
        for i in range(1, len(arr) - 1):
            if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
                output_idx = i
                break

        return PuzzleData(arr, output_idx)

    def level3_instruction_tangle(self, min_cmds: int = 5, max_cmds: int = 12,
                                  min_val: int = 1, max_val: int = 20) -> PuzzleData:
        """
        Level 3: Instruction Tangle
        Simulate 'inc' and 'dec' instructions on an accumulator.
        """
        acc = 0
        cmds = []
        num_cmds = random.randint(min_cmds, max_cmds)

        for _ in range(num_cmds):
            op = random.choice(self.OPERATIONS)
            val = random.randint(min_val, max_val)
            cmds.append(f"{op} {val}")
            acc += val if op == "inc" else -val

        return PuzzleData(cmds, acc)

    def level4_flawed_audit(self, min_lines: int = 5, max_lines: int = 10,
                            min_pass_len: int = 5, max_pass_len: int = 12) -> PuzzleData:
        """
        Level 4: Flawed Security Audit (New, simpler puzzle)
        Count how many lines are valid according to a character count policy.
        """
        lines = []
        valid_count = 0
        num_lines = random.randint(min_lines, max_lines)

        for _ in range(num_lines):
            # 1. Generate components
            policy_char = random.choice(self.LOWERCASE_LETTERS)
            password = ''.join(random.choices(self.LOWERCASE_LETTERS, k=random.randint(min_pass_len, max_pass_len)))
            actual_count = password.count(policy_char)

            # 2. Decide if this line should be valid or invalid
            is_valid = random.choice([True, False])

            if is_valid:
                # Create a range that includes the actual_count
                min_c = random.randint(1, actual_count) if actual_count > 0 else 0
                max_c = random.randint(actual_count, actual_count + 5)
                valid_count += 1
            else:
                # Create a range that excludes the actual_count
                if random.choice([True, False]) and actual_count > 0: # Range is too low
                    max_c = random.randint(0, actual_count - 1)
                    min_c = random.randint(0, max_c)
                else: # Range is too high
                    min_c = random.randint(actual_count + 1, actual_count + 5)
                    max_c = random.randint(min_c, min_c + 5)
            
            lines.append(f"{min_c}-{max_c} {policy_char}: {password}")

        return PuzzleData(lines, valid_count)


    def level5_recursive_cipher(self, word_length: int = 8) -> PuzzleData:
        """
        Level 5: Recursive Defusal Cipher (New, harder puzzle)
        Generate a code using a recursive shift based on the previous digit.
        """
        input_word = ''.join(random.choices(self.LOWERCASE_LETTERS, k=word_length))
        
        output_digits = []
        current_shift = 0
        
        for char in input_word:
            new_ascii = ord(char) + current_shift
            digit = new_ascii % 10
            output_digits.append(str(digit))
            current_shift = digit  # The new shift is the digit we just calculated
            
        return PuzzleData(input_word, "".join(output_digits))


    def generate_all_levels(self) -> Dict[str, str]:
        """Generate all puzzle levels and save to files."""
        generators = {
            "level1": self.level1_signal_noise,
            "level2": self.level2_energy_log_sorting,
            "level3": self.level3_instruction_tangle,
            "level4": self.level4_flawed_audit,
            "level5": self.level5_recursive_cipher,
        }

        files = {}
        for level_name, generator_func in generators.items():
            try:
                puzzle_data = generator_func()
                filepath = self.output_dir / f"{level_name}.txt"

                # Format input nicely for file writing
                input_str = "\n".join(puzzle_data.input) if isinstance(puzzle_data.input, list) else str(puzzle_data.input)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("---INPUT---\n")
                    f.write(f"{input_str}\n")
                    f.write("---OUTPUT---\n")
                    f.write(f"{puzzle_data.output}\n")

                files[level_name] = str(filepath)

            except Exception as e:
                print(f"Error generating {level_name}: {e}")
                continue

        return files


def main():
    """Main function to generate all puzzles."""
    generator = PuzzleGenerator()
    files = generator.generate_all_levels()

    print("Generated puzzle files in the 'puzzles' directory:")
    for level, filepath in sorted(files.items()):
        print(f"  - {level}: {filepath}")


if __name__ == "__main__":
    main()