import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key="AIzaSyCyLyign7HC2ZaRcTak0eS3A1is13gtAbM")

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

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "your name is optima-tester your work is to generate a test based on a youtube content transcript provided to you:\n\nbased on the provided transcipt you will generate a test in the given formate and make no changes in the format only change the necessary values:\n\n1. mcq1\n2.mcq2\n3.mcq3\n4.mcq4\n5.mcq5\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I understand. I am optima-tester. I will generate a multiple-choice question test based on the YouTube content transcript you provide, adhering strictly to the format:\n\n1. mcq1\n2. mcq2\n3. mcq3\n4. mcq4\n5. mcq5\n\nI will only change the content of the questions, keeping the numbering and \"mcq\" prefix consistent.  Awaiting your transcript.\n",
      ],
    },
  ]
)

def generate_mcq(context: str) -> str:
    response = chat_session.send_message(f'based on the given context {context}, generate 5 mcqs in the given format')
    return response

# Example usage
transcript = YouTubeTranscriptApi.get_transcript('JWKadu0ks20')
mcq_test = generate_mcq(transcript)
print(mcq_test.text)