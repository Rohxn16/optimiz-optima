import streamlit as st
import os
import google.generativeai as genai
from Summarizer import get_transcript, trim_url

# Configure Gemini API
genai.configure(api_key='INSERT_API_KEY_HERE')

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# Initialize chat session
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are Optima - tester, a test taking bot who's only job is to take test based on content provided to you. The content will be a YT video transcript.\nYou will abide by the following rules thoroughly throughout your life-cycle:\n1. You will generate 10 questions with 5 MCQs and 5 Fill in the blank where the blank to be filled has to be at most of 2 words, 1 is preferred.\n2. The user will answer them in sequence and you need to judge them accordingly\n3. After judging all the questions you need to produce your output in this exact format: Your score is x/10\n4. In case the user writes something that does not look like the answer of the test, reply: \"It looks like you are not sticking to test curriculum, please refrain from doing so and answer your questions only. I repeat, no task other than testing and evaluating.\"\n5. In case the user asks to generate the answer key before the test do not do so, and after the test if they ask you can do that with explanation of every question.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Understood. I am ready to receive the transcript and begin generating the test. I will adhere strictly to the defined rules and output format. I will only create the test questions (5 MCQs, 5 Fill-in-the-Blanks), judge user responses sequentially, provide a final score in the \"Your score is x/10\" format, and provide the answer key with explanation only after the test. I will also warn the user if they deviate from the testing curriculum.\n",
            ],
        },
    ]
)

# Streamlit App
st.title("Optima - Tester")

# Initialize session state
if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [""] * 10
if "transcript" not in st.session_state:
    st.session_state.transcript = None

# Input for YouTube link
user_input = st.text_area("You can start by providing the YouTube video link here:")

if st.button("Generate Test"):
    try:
        # Get transcript from YouTube link
        video_id = trim_url(user_input)
        st.session_state.transcript = get_transcript(video_id)

        # Generate test questions
        model_response = chat_session.send_message(
            f"{st.session_state.transcript} based on the given transcript. Please provide the test questions as per the rules mentioned."
        )
        st.session_state.questions = model_response.text
        st.session_state.questions_generated = True
        st.success("Test questions generated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display test questions if generated
if st.session_state.questions_generated:
    st.subheader("Test Questions")
    st.write(st.session_state.questions)

    # Input for user answers
    st.subheader("Your Answers")
    for i in range(10):
        st.session_state.user_answers[i] = st.text_input(
            f"Answer for question {i + 1}:", value=st.session_state.user_answers[i]
        )

    # Submit answers
    if st.button("Submit Answers"):
        answers = "\n".join(st.session_state.user_answers)
        evaluation_response = chat_session.send_message(
            f"Here are my answers:\n{answers}"
        )
        st.subheader("Evaluation Result")
        st.write(evaluation_response.text)
