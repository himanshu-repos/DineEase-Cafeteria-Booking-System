import streamlit as st
import random
import mysql.connector
from fpdf import FPDF
import os

# Price per seat
PRICE_PER_SEAT = 80

# Folder path for saving the token PDF
PDF_SAVE_PATH = r"C:\Minor Project 1\Tokens"

os.makedirs(PDF_SAVE_PATH, exist_ok=True)

# Database connection function
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="mess_token_generator"
    )

def generate_unique_code():
    while True:
        code = str(random.randint(100000, 999999))

        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT code FROM booking_details WHERE code = %s UNION SELECT code FROM token_details WHERE code = %s", (code, code))
        result = cursor.fetchone()
        connection.close()

        if not result:
            return code


def generate_token(name, number, seats):
    try:
        code = generate_unique_code()

        # Save to the database
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO booking_details (name, number, seats, code) VALUES (%s, %s, %s, %s)",
            (name, number, seats, code)
        )
        connection.commit()
        connection.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Mess Token", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {number}", ln=True)
        pdf.cell(200, 10, txt=f"Seats: {seats}", ln=True)
        pdf.cell(200, 10, txt=f"Token Code: {code}", ln=True)

        pdf_output_path = os.path.join(PDF_SAVE_PATH, f"{name}_token.pdf")
        pdf.output(pdf_output_path)

        return code, seats * PRICE_PER_SEAT, pdf_output_path
    except mysql.connector.Error as err:
        st.error(f"Database Error: {err}")
        return None, None, None


st.title("Mess Token Booking")

name = st.text_input("Enter Your Name")
number = st.text_input("Enter Your Phone Number")
seats = st.number_input("Number of Seats", min_value=1, step=1)

# Initialize session state for controlling the flow
if "token_generated" not in st.session_state:
    st.session_state.token_generated = False
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "total_price" not in st.session_state:
    st.session_state.total_price = None
if "pdf_output_path" not in st.session_state:
    st.session_state.pdf_output_path = None

if not st.session_state.token_generated:
    # Button to initiate token generation
    if st.button("Generate Token"):
        if name and number and seats:
            # Generate code, total price, and save PDF
            st.session_state.generated_code, st.session_state.total_price, _ = generate_token(name, number, seats)

            qr_image_path = "C:\\Users\\dubey\\Downloads\\qr_code.jpeg"
            st.image(qr_image_path, caption="Scan to Pay", use_container_width=True)

            st.write(f"Total Price: ₹{st.session_state.total_price} (₹80 per seat)")

            st.session_state.token_generated = True
        else:
            st.error("Please fill all the details!")

if st.session_state.token_generated:
    if st.button("Next"):
        if st.session_state.pdf_output_path is None:
            generated_code, total_price, pdf_output_path = generate_token(name, number, seats)
            if generated_code:
                st.session_state.generated_code = generated_code
                st.session_state.total_price = total_price
                st.session_state.pdf_output_path = pdf_output_path

                st.success("Token Generated Successfully!")

                st.write("Download your token PDF:")
                st.download_button("Download Token", data=open(pdf_output_path, "rb").read(), file_name=f"{name}_token.pdf")
