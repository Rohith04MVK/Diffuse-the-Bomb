import random
import string
from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class PuzzleData:
    input: Union[List, str, int]
    output: Union[List, str, int]


class PuzzleGenerator:
    LOWERCASE_LETTERS = string.ascii_lowercase
    OPERATIONS = ["inc", "dec"]

    def level1_signal_noise(self, num_variants=100, min_word_len=10, max_word_len=15) -> PuzzleData:
        """Generates a signal noise puzzle with at least 100 variants."""
        word_length = random.randint(min_word_len, max_word_len)
        original_word = ''.join(random.choices(
            self.LOWERCASE_LETTERS, k=word_length))
        variants = [original_word] * 3
        for _ in range(num_variants):
            word_chars = list(original_word)
            for _ in range(random.randint(1, word_length // 2)):
                idx_to_change = random.randrange(word_length)
                original_char = word_chars[idx_to_change]
                available_chars = self.LOWERCASE_LETTERS.replace(
                    original_char, '')
                word_chars[idx_to_change] = random.choice(available_chars)
            variants.append(''.join(word_chars))
        random.shuffle(variants)
        return PuzzleData("\n".join(variants), original_word)

    def level2_energy_log_sorting(self, min_size=100, max_size=150, min_val=1, max_val=100) -> PuzzleData:
        """Generates an energy log sorting puzzle with at least 100 items."""
        size = random.randint(min_size, max_size)
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        spike_idx = random.randint(1, size - 2)
        left_val, right_val = arr[spike_idx - 1], arr[spike_idx + 1]
        arr[spike_idx] = max(left_val, right_val) + random.randint(10, 20)
        output_idx = -1
        for i in range(1, len(arr) - 1):
            if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
                output_idx = i
                break
        return PuzzleData(str(arr), str(output_idx))

    def level3_instruction_tangle(self, min_cmds=100, max_cmds=150, min_val=1, max_val=50) -> PuzzleData:
        """Generates an instruction tangle puzzle with at least 100 commands."""
        acc, cmds, num_cmds = 0, [], random.randint(min_cmds, max_cmds)
        for _ in range(num_cmds):
            op, val = random.choice(
                self.OPERATIONS), random.randint(min_val, max_val)
            cmds.append(f"{op} {val}")
            acc += val if op == "inc" else -val
        return PuzzleData("\n".join(cmds), str(acc))

    def level4_flawed_audit(self, min_lines=100, max_lines=150, min_pass_len=8, max_pass_len=16) -> PuzzleData:
        """Generates a flawed audit puzzle with at least 100 lines."""
        lines, valid_count, num_lines = [], 0, random.randint(
            min_lines, max_lines)
        for _ in range(num_lines):
            policy_char = random.choice(self.LOWERCASE_LETTERS)
            password = ''.join(random.choices(
                self.LOWERCASE_LETTERS, k=random.randint(min_pass_len, max_pass_len)))
            actual_count = password.count(policy_char)
            is_valid = random.choice([True, False])
            if is_valid:
                min_c = random.randint(
                    1, actual_count) if actual_count > 0 else 0
                max_c = random.randint(actual_count, actual_count + 5)
                valid_count += 1
            else:
                if random.choice([True, False]) and actual_count > 0:
                    max_c = random.randint(0, actual_count - 1)
                    min_c = random.randint(0, max_c)
                else:
                    min_c = random.randint(actual_count + 1, actual_count + 5)
                    max_c = random.randint(min_c, min_c + 5)
            lines.append(f"{min_c}-{max_c} {policy_char}: {password}")
        return PuzzleData("\n".join(lines), str(valid_count))

    def level5_recursive_cipher(self, word_length=100) -> PuzzleData:
        """Generates a recursive cipher puzzle with at least 100 characters."""
        input_word = ''.join(random.choices(
            string.ascii_uppercase, k=word_length))
        output_digits, current_shift = [], 0
        for char in input_word:
            new_ascii = ord(char) + current_shift
            digit = new_ascii % 10
            output_digits.append(str(digit))
            current_shift = digit
        return PuzzleData(input_word, "".join(output_digits))

    def generate_all_puzzles(self) -> Dict[int, PuzzleData]:
        """Generates all puzzle levels and returns them in a dictionary."""
        return {
            1: self.level2_energy_log_sorting(),      # was 2, now 1
            2: self.level3_instruction_tangle(),      # was 3, now 2
            3: self.level1_signal_noise(),            # was 1, now 3
            4: self.level4_flawed_audit(),
            5: self.level5_recursive_cipher(),
        }
