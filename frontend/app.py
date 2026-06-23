import os
import requests
import streamlit as st


BACKEND_URL = "http://127.0.0.1:8000/ask"
FEEDBACK_FILE = "feedback/feedback.txt"


os.makedirs("feedback", exist_ok=True)


st.set_page_config(
    page_title="University Student Support Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("University Student Support Assistant")
st.write(
    "Ask questions about course registration, examination rules, library services, "
    "ICT support, hostel application, fee payment, academic calendar, or student conduct."
)

question = st.text_area("Enter your question here:")

if st.button("Ask Assistant"):
    if not question.strip():
        st.warning("Please enter a question before submitting.")

    else:
        with st.spinner("Generating response, please wait..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"question": question},
                    timeout=70
                )

                if response.status_code == 200:
                    data = response.json()

                    st.session_state["last_question"] = question
                    st.session_state["last_answer"] = data["answer"]

                    st.success("Response generated successfully.")

                else:
                    error_detail = response.json().get("detail", "Unknown error occurred.")
                    st.error(f"Error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Connection error: Backend is not running. "
                    "Please start the FastAPI server first."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "Slow response: The assistant took too long to respond. "
                    "Please try again."
                )

            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")


if "last_answer" in st.session_state:
    st.subheader("Answer")
    st.write(st.session_state["last_answer"])

    st.divider()

    st.subheader("Rate this answer")

    rating = st.radio(
        "How would you rate this response?",
        ["Good", "Average", "Poor"],
        horizontal=True
    )

    if st.button("Submit Feedback"):
        with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"Question: {st.session_state['last_question']}\n"
                f"Answer: {st.session_state['last_answer']}\n"
                f"Rating: {rating}\n"
                f"{'-'*50}\n"
            )

        st.success("Feedback saved successfully.")