# --- Day 1: Countdown to Disarm ---

> **[URGENT - EYES ONLY - PRIORITY OMEGA]**
>
> **AGENT, WE HAVE A SITUATION.**
>
> The rogue anarchist collective known as "The Cypher Syndicate" has activated a city-wide chrono-bomb. We don't know its exact mechanism, but their manifesto claims it will "reset the city to zero." We're interpreting that as a very, very bad thing.
>
> Our infiltration teams are neutralized. You are our last line of defense. We've managed to get you a direct remote link to the bomb's core processor, but it's protected by a five-level cascading security system. You must solve each challenge to peel back a layer of the bomb's defenses.
>
> The timer is already ticking. You have your terminal, your wits, and very little time. Good luck.

---

## --- Step 1: Signal Noise ---

Your first task is to intercept the bomb's internal schematic. The Syndicate is broadcasting it on all channels, but they're using a powerful jamming field to bury the real data in static. Your receiver has picked up multiple noisy copies of the schematic.

The good news is that the jamming is inconsistent. At any given character position in the transmission, the most frequently occurring character is the correct one. You must reconstruct the original message from these multiple noisy copies.

For example, given these four transmissions:
```
hxllo
hello
healo
hezlo
```

- In the first position, `h` is the most common.
- In the second position, `e` is the most common.
- In the third position, `l` is the most common.
- In the fourth position, `l` is the most common.
- In the fifth position, `o` is the most common.

By finding the most frequent character at each position, you can reconstruct the true schematic: `hello`.

**Your puzzle input is a list of noisy signals.** To bypass the first layer of security, what is the clear-text schematic?

---

## --- Step 2: Energy Log Sorting ---

The schematic is in! It gives you access to the bomb's reactor energy logs. According to a fragment of the bombmaker's notes, the device has a critical vulnerability: a regulation node that can be overloaded. This node is identifiable in the logs as the *first* power reading that represents a significant spike—a value that is strictly greater than the readings immediately before and after it.

You must scan the list of power readings and find the location of this first unstable peak. The answer isn't the energy value itself, but its index in the log.

For example, given this energy log: `[3, 7, 1, 5, 2, 9]`

- `7` is the first number that is greater than its left neighbor (`3`) and its right neighbor (`1`).
- It is located at `index 1`.
- While `5` is also a peak, `7` occurs first in the sequence.

**Your puzzle input is a list of energy readings.** At what index is the critical vulnerability located?

---

## --- Step 3: Instruction Tangle ---

You've isolated the vulnerable node. To overload it, you must execute a specific instruction sequence. The Syndicate's AI has left a boot sequence log on the node which you must simulate to determine its final state. If you can calculate the result, you can use it to craft a counter-command.

The sequence starts with an accumulator at `0`. Each instruction modifies the accumulator.

- `inc x` adds the number `x` to the accumulator.
- `dec x` subtracts the number `x` from the accumulator.

For example, given the instruction sequence `["inc 5", "dec 2", "inc 3"]`:

1. Start with accumulator = `0`.
2. `inc 5`: accumulator becomes `0 + 5 = 5`.
3. `dec 2`: accumulator becomes `5 - 2 = 3`.
4. `inc 3`: accumulator becomes `3 + 3 = 6`.

The final result is `6`.

**Your puzzle input is a list of calibration instructions.** What is the final value of the accumulator?

---

## --- Step 4: Grid Path Match ---

Success! The node is overloaded, but the system is fighting back. It has deployed two "Hunter" security programs that patrol the bomb's internal circuitry grid. They move to seek out and purge your connection. To proceed, you must disable them. The only way to do that is to plant a logic bomb at the *first* grid coordinate that they both visit.

You have the movement logs for both Hunter programs, which both start at `(0, 0)`. The paths are a series of moves like `R2` (move Right 2 units) or `U1` (move Up 1 unit). A move like `R2` means visiting `(1, 0)` and then `(2, 0)`.

You must simulate both paths and find the first coordinate (excluding the starting point `(0,0)`) that was visited by *both* programs.

For example, with these paths:
- Path A = `["R2", "U1"]`
- Path B = `["U1", "R2"]`

1.  **Hunter A's Path:** Starts at `(0,0)`.
    - `R2`: Visits `(1,0)`, then `(2,0)`. Path so far: `{(1,0), (2,0)}`.
    - `U1`: Visits `(2,1)`. Total path: `{(1,0), (2,0), (2,1)}`.
2.  **Hunter B's Path:** Starts at `(0,0)`.
    - `U1`: Visits `(0,1)`.
    - `R2`: Visits `(1,1)`, then `(2,1)`. As it moves to `(2,1)`, you check if Hunter A has already been there. It has! This is their first point of intersection.

The first shared cell is `(2,1)`.

**Your puzzle input is the two lists of moves.** At which coordinate must you plant the logic bomb?

---

## --- Step 5: Defuse Code ---

The Hunter programs are down! You've reached the final layer: the main detonation keypad. It requires an 8-digit code. Our analysts have found a hidden message from the bomb's disgruntled creator—a secret formula to derive the code from a master passphrase.

To generate each digit of the 8-digit code, you take one character of the 8-character passphrase. The digit is calculated using the following rule:

`digit = (ASCII value of the character + its zero-based index) % 10`

The master passphrase for your specific instance of the bomb is: `OVERRIDE`

Let's calculate the code for `OVERRIDE` as an example:
- `O`: `(ord('O') + 0) % 10` -> `(79 + 0) % 10` -> `79 % 10` -> `9`
- `V`: `(ord('V') + 1) % 10` -> `(86 + 1) % 10` -> `87 % 10` -> `7`
- `E`: `(ord('E') + 2) % 10` -> `(69 + 2) % 10` -> `71 % 10` -> `1`
- `R`: `(ord('R') + 3) % 10` -> `(82 + 3) % 10` -> `85 % 10` -> `5`
- `R`: `(ord('R') + 4) % 10` -> `(82 + 4) % 10` -> `86 % 10` -> `6`
- `I`: `(ord('I') + 5) % 10` -> `(73 + 5) % 10` -> `78 % 10` -> `8`
- `D`: `(ord('D') + 6) % 10` -> `(68 + 6) % 10` -> `74 % 10` -> `4`
- `E`: `(ord('E') + 7) % 10` -> `(69 + 7) % 10` -> `76 % 10` -> `6`

The final code would be `97156846`.

**Your puzzle input is the passphrase for your specific bomb: `CYPHERGO`**

Calculate the 8-digit defusal code. The fate of the city is in your hands.