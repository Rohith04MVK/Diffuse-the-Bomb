# --- Day 1: Countdown to Disarm ---

> **[URGENT - EYES ONLY - PRIORITY OMEGA]**
>
> **AGENT, WE HAVE A SITUATION.**
>
> The rogue anarchist collective known as "The Equalists" has activated a city-wide chrono-bomb. We don't know its exact mechanism, but their manifesto claims it will "reset the city to zero." We're interpreting that as a very, very bad thing.
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

---

## --- Step 4: Flawed Security Audit ---

The overload command from Step 3 has sent the bomb's security AI into a panic! It's now performing a security audit on its own database of historical access codes, trying to find which ones are "secure" according to a new, very simple (and flawed) policy.

You've intercepted the list of codes and their corresponding security policies. By figuring out how many codes the AI considers "valid," you can predict its next move and bypass this security layer.

Each line in your input represents a single policy and its associated code, like this:

`2-4 a: aabbcc`

This line is broken down into three parts:
-   `2-4`: The policy requires the letter to appear a minimum of 2 times and a maximum of 4 times.
-   `a`: The letter the policy applies to.
-   `aabbcc`: The access code to check.

To be **valid**, the letter must appear in the code a number of times that is within the min-max range (inclusive).

Let's look at some examples:
-   `1-3 a: abcde` is **valid**. The letter 'a' appears 1 time, which is between 1 and 3.
-   `1-3 b: cdefg` is **invalid**. The letter 'b' appears 0 times, which is not between 1 and 3.
-   `2-9 c: ccccccccc` is **valid**. The letter 'c' appears 9 times, which is between 2 and 9.

**Your puzzle input is a list of these policy/code lines.** How many of the access codes are considered valid by this flawed logic?

---

## --- Step 5: The Recursive Defusal Cipher ---

The audit is bypassed! You've reached the final manual override panel. The keypad is glowing, awaiting an 8-digit code. Intercepted communications reveal the bomb's creator used a highly paranoid encryption method: a **dynamic recursive cipher**.

Unlike a simple Caesar cipher with a fixed key, this cipher's key changes with every character you process. The process generates one digit of the final code, and that very digit becomes the shift value for the *next* character.

Here is the process:

1.  Start with a **current shift value** of `0`.
2.  For each character in the 8-character passphrase, from left to right:
    a. Calculate the `new_ascii` value by adding the `current_shift_value` to the character's standard ASCII value.
    b. The `digit` for the final code is `new_ascii % 10`.
    c. **Crucially, the `current_shift_value` for the next character becomes the `digit` you just calculated.**

Let's calculate the code for the example passphrase `AGENT`:

- **Start:** `current_shift = 0`

- **Character 'A' (index 0):**
  - `new_ascii = ord('A') + current_shift` -> `65 + 0 = 65`.
  - `digit = 65 % 10 = 5`.
  - **Code is `5...`**, **next shift becomes `5`**.

- **Character 'G' (index 1):**
  - `new_ascii = ord('G') + current_shift` -> `71 + 5 = 76`.
  - `digit = 76 % 10 = 6`.
  - **Code is `56...`**, **next shift becomes `6`**.

...and so on. The final code for `AGENT` would be `56537`.

**Your puzzle input is the final passphrase: `CYPHERGO`**. Time is critical. What is the 8-digit defusal code?