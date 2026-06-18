import os 
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template


load_dotenv()
app = Flask(__name__)
client = Groq(api_key= os.getenv("GROQ_API_KEY"))

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    chat_history.append({
        "role" : "user",
        "content": user_msg
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_history
    )

    ai_reply = response.choices[0].message.content


    chat_history.append({
        "role": "assistant",
        "content": ai_reply
    })
    
    return jsonify({"reply":ai_reply})


if __name__== "__main__":
    app.run(debug=True)