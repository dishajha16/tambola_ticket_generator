# utils/table_detector.py

import cv2
import numpy as np

def detect_ticket_tables(image, debug=True):
    """
    Detects full 3x9 tambola ticket tables in an image.
    Returns: list of (x, y, w, h) for each detected ticket table.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 10)

    # Detect horizontal lines
    horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horiz = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horiz_kernel, iterations=2)

    # Detect vertical lines
    vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    vert = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vert_kernel, iterations=2)

    # Combine
    grid = cv2.add(horiz, vert)

    # Find contours of full tables
    contours, _ = cv2.findContours(grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    table_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 300 and h > 100:
            table_boxes.append((x, y, w, h))

    if debug:
        debug_img = image.copy()
        for (x, y, w, h) in table_boxes:
            cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save debug overlays and line detections
        cv2.imwrite("output/debug_ticket_tables.jpg", debug_img)
        cv2.imwrite("output/horizontal_lines.jpg", horiz)
        cv2.imwrite("output/vertical_lines.jpg", vert)
        cv2.imwrite("output/combined_grid.jpg", grid)


    return table_boxes


