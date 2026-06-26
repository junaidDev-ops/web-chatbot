import os 
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager , UserMixin , login_user , logout_user , login_required ,  current_user


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User (db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique= True)
    password = db.Column(db.String(200))

@app.route("/signup", methods= ["POST"])
def signup():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    new_user = User(name=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup Successful!"})

@app.route("/login", methods= ["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if User is None:
        return jsonify({"message": "Email not found!"})
    
    if password == user.password:
        return jsonify({"message": "Login Successful!"})
    else:
        return jsonify({"message": "Wrong Password!"})


client = Groq(api_key= os.getenv("GROQ_API_KEY"))

chat_history = [
    {
        "role": "system",
        "content": "Tum hamesha short aur seedha jawab dena. Sirf jo poocha gaya hai uska jawab do, extra detail mat dena jab tak specifically na poocha jaye."
    }
]

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