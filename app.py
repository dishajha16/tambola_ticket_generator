# app.py

import streamlit as st
import cv2
import numpy as np
from utils.table_detector import detect_ticket_tables
from utils.ticket_generator import generate_ticket
from utils.overlay_utils import draw_clean_ticket  # updated draw function

st.set_page_config(layout="wide")
st.title("🎟️ Tambola Ticket Replacer with Boundary Detection")

uploaded_file = st.file_uploader("Upload Tambola Image (JPG only)", type=["jpg", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    st.image(image, caption="🖼️ Original Image", use_container_width=True)

    if st.button("🔄 Replace Detected Tickets"):
        table_boxes = detect_ticket_tables(image, debug=True)
        st.write(f"🧠 Tables Detected: {len(table_boxes)}")

        if not table_boxes:
            st.error("❌ No ticket tables found.")
        else:
            modified_image = image.copy()

            for (x, y, w, h) in table_boxes:
                ticket = generate_ticket()
                modified_image = draw_clean_ticket(modified_image, ticket, x, y, w, h)

            # Save output
            cv2.imwrite("output/final_debug_result.jpg", modified_image)

            # Display
            rgb = cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB)
            st.image(rgb, caption="✅ Updated Tambola Image", use_container_width=True)

            # Download button
            st.download_button(
                label="📥 Download Updated Image",
                data=cv2.imencode('.jpg', modified_image)[1].tobytes(),
                file_name="new_tambola_tickets.jpg",
                mime="image/jpeg"
            )
