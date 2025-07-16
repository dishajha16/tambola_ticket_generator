# utils/ticket_generator.py

import random

def generate_ticket():
    # Define column-wise number ranges
    column_ranges = {
        0: list(range(1, 10)),
        1: list(range(10, 20)),
        2: list(range(20, 30)),
        3: list(range(30, 40)),
        4: list(range(40, 50)),
        5: list(range(50, 60)),
        6: list(range(60, 70)),
        7: list(range(70, 80)),
        8: list(range(80, 91)),
    }

    # Step 1: Decide number of entries per column (1–3, total 15)
    col_counts = [1] * 9
    remaining = 15 - 9
    while remaining > 0:
        i = random.randint(0, 8)
        if col_counts[i] < 3:
            col_counts[i] += 1
            remaining -= 1

    # Step 2: Choose random numbers from each column range
    columns = {}
    for col in range(9):
        columns[col] = sorted(random.sample(column_ranges[col], col_counts[col]))

    # Step 3: Distribute to rows, ensuring each row gets exactly 5
    ticket = [['' for _ in range(9)] for _ in range(3)]
    row_counts = [0, 0, 0]

    # First pass: fill each column one by one
    for col in range(9):
        count = len(columns[col])
        available_rows = [i for i in range(3) if row_counts[i] < 5]
        if count > len(available_rows):
            # Force reset and try again
            return generate_ticket()

        chosen_rows = random.sample(available_rows, count)
        for i, row in enumerate(chosen_rows):
            ticket[row][col] = columns[col][i]
            row_counts[row] += 1

    # Final check
    if all(count == 5 for count in row_counts):
        return ticket
    else:
        # Retry if row constraints not satisfied
        return generate_ticket()
