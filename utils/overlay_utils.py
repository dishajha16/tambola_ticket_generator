# utils/overlay_utils.py

import cv2

def draw_clean_ticket(image, ticket, x, y, w, h):
    """
    Overwrites the region (x, y, w, h) in the image with a clean 3x9 ticket grid
    and writes the numbers from `ticket` into the cells.
    """
    # Step 1: Clear the region (white background)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)

    cell_w = w // 9
    cell_h = h // 3

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.9
    thickness = 2
    text_color = (0, 0, 0)
    grid_color = (255, 0, 0)  # Blue lines

    for row in range(3):
        for col in range(9):
            cell_x = x + col * cell_w
            cell_y = y + row * cell_h
            cell_rect = (cell_x, cell_y, cell_w, cell_h)

            # Draw grid cell
            cv2.rectangle(image, (cell_x, cell_y), (cell_x + cell_w, cell_y + cell_h), grid_color, 1)

            # Draw number if present
            number = ticket[row][col]
            if number != '':
                text = str(number)
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                text_x = cell_x + (cell_w - text_size[0]) // 2
                text_y = cell_y + (cell_h + text_size[1]) // 2
                cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, thickness)

    return image
