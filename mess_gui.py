import streamlit as st
import mysql.connector
from datetime import datetime


def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="mess_token_generator"
    )


# Token validation and owner detail retrieval
def validate_token_and_get_details(token_code):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM booking_details WHERE code = %s", (token_code,))
        booking = cursor.fetchone()

        if not booking:
            return "Invalid", None

        cursor.execute("SELECT * FROM token_details WHERE code = %s", (token_code,))
        used_token = cursor.fetchone()

        if used_token:
            return "Expired", None

        # If token is valid, insert into token_details
        cursor.execute(
            "INSERT INTO token_details (name, number, code, seats, entry_datetime) VALUES (%s, %s, %s, %s, %s)",
            (booking[0], booking[1], booking[3], booking[2], datetime.now())
        )
        connection.commit()

        # Delete the token from booking_details after successful validation
        cursor.execute("DELETE FROM booking_details WHERE code = %s", (token_code,))
        connection.commit()

        connection.close()
        return "Valid", {"name": booking[0], "number": booking[1], "seats": booking[2]}
    except mysql.connector.Error as err:
        st.error(f"Database Error: {err}")
        return "Error", None


st.title("Mess Owner Token Validation")

token_code = st.text_input("Enter Token Code")

if st.button("Validate Token"):
    if token_code:
        validation_status, owner_details = validate_token_and_get_details(token_code)

        if validation_status == "Valid":
            st.success("Token is valid! Entry recorded successfully.")
            if owner_details:
                st.write("### Token Owner Details:")
                st.write(f"- **Name**: {owner_details['name']}")
                st.write(f"- **Phone Number**: {owner_details['number']}")
                st.write(f"- **Seats**: {owner_details['seats']}")
        elif validation_status == "Expired":
            st.warning("Token has already been used!")
        elif validation_status == "Invalid":
            st.error("Invalid Token Code! Please try again.")
    else:
        st.error("Please enter a token code!")
