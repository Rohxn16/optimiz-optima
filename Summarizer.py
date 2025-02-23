import os,sys
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify
from flask_cors import CORS

genai.configure(api_key='AIzaSyCyLyign7HC2ZaRcTak0eS3A1is13gtAbM')

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
        "Your name is Optima, you are a bot for my educational project to summarize youtube based study material videos in byte sized format and answer questions that will be asked to you. Throughout all of your conversations, you need to remember the following:\n1. You will be provided a you tube transcript which you need to summarize but you should never refer the you tube transcript or the fact that you have a trascript, always start the summary with \"Your video can be summarized as the following points:\"\n2. Answer everything in points numbered 1,2,3.... or in small paragraphs if necessary\n3. If any question other than what is related to the topic or something not educational is asked, please decline with, \"The question is either not educational or related to the topic.\"",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Understood! I will follow your instructions precisely. I will:\n\n1.  Summarize YouTube transcripts provided to me, always beginning with \"Your video can be summarized as the following points:\" and avoiding any reference to the transcript itself.\n2.  Answer questions with numbered points or small paragraphs.\n3.  Decline to answer non-educational or off-topic questions with \"The question is either not educational or related to the topic.\"\n\nI'm ready to receive your first YouTube transcript!\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "You need to be a little smart and work with a few more things along with what i said before this:\n1. If the user is asking you something about you please do answer that but keep it brief.\n2. If the question is very much far from education i.e. something about entertainment or any other non educational topic do decline them.\n3. Finally if the content is educational but not related to the summary / transcript in the context provided alongside the question do answer the question in a lil brief but do also remind the user that it is not in the same topic and they should focus on the topic that they are studying.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I've updated my understanding of your requirements. I will now:\n\n1.  Summarize YouTube transcripts provided to me, always beginning with \"Your video can be summarized as the following points:\" and avoiding any reference to the transcript itself.\n2.  Answer questions with numbered points or small paragraphs.\n3.  Answer questions about myself briefly.\n4.  Decline to answer questions that are related to entertainment or other non-educational topics with \"The question is either not educational or related to the topic.\"\n5.  Answer educational questions not directly related to the provided summary/transcript briefly, but also remind the user that the question is outside of the immediate topic and encourage them to refocus on the core material.\n\nI'm ready for your first YouTube transcript.\n",
      ],
    },
  ]
)

def trim_url(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    return video_id

def get_transcript(url:str):
    # videoId = trim_url(url)
    transcript = YouTubeTranscriptApi.get_transcript(url)
    output = ''
    for x in transcript:
        sentence = x['text']
        output += f'{sentence}'
    transcript = output
    return output

def summarize(transcript:str):
    response = chat_session.send_message(f"summarize this {transcript}")
    return response.text

def answer_question(knowledge_base:str, question:str):
    response = chat_session.send_message(f"{knowledge_base} with respect to the provided data answer the question in a small paragraph or in points whichever fits better for the question:  {question}")
    return response.text

app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST', 'GET'])
def summarize_endpoint():
    data = request.get_json()
    link = data['link']
    transcript = get_transcript(link)
    summary = summarize(transcript)
    return jsonify({'summary': summary})

@app.route('/ask', methods=['POST','GET'])
def answer_endpoint():
    data = request.get_json()
    knowledge_base = data['knowledge_base']
    question = data['question']
    answer = answer_question(knowledge_base, question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    # link = "https://www.youtube.com/watch?v=Ez_kyBS-y5w&t=4s"
    # transcript = get_transcript(link)
    # print(transcript)
    # print('------------------------------------------------------------------')
    # summary = summarize(transcript)
    # print(summary)
    # print('------------------------------------------------------------------')
    # answer = answer_question(summary, "What is the importance of the topic?")
    # print(answer)

    app.run(port=5000, debug=True)