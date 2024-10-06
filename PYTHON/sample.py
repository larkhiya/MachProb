import re

def count_operators(line):
    # Define a regex pattern to match operators correctly
    operator_pattern = r'(?<!\d)([+\-*/=]|[<>]{2}|[+-]{2})(?!\d)'

    # Use regex findall to find all operators in the line
    matches = re.findall(operator_pattern, line)

    # Count the matches
    operator_count = len(matches)

    return operator_count

def total_operators(lines):
    total_count = 0
    for line in lines:
        total_count += count_operators(line)
    return total_count

# Example usage with more test lines
lines = [
    "int x = 10, y = 8, z = -2;",
    "x = x + y;",
    "y = x - y;",
    "x = x - y;",
    "z = x - -10;",
    "x = x >> 1;",      # Right shift
    "y = y << 1;",      # Left shift
    "if (x < y) {",     # Less than
    "x = (x + y) * 2;", # Multiple operators
    "y = z < 0 ? x : y;", # Ternary operator with less than
    "while (x >= y) x--;" # Greater than or equal
]

total_count = total_operators(lines)
print(f"T(n) = {total_count}")  # Should output the correct count
