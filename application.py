import os

from flask import Flask, render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#key: sgE01Y9XzDeh7L4ElWSRww
#secret: OS4npdTfqJvE0vAVsyxD3zANfwFPEkCTJsv6U5NqaMY

app = Flask(__name__)

# Check for environment variable
# postgres://pqmhdefpcrzunt:5ffd965fa6e1320993778fd91c78d282921d7277dc1af8a2a5806284bee70d3c@ec2-54-227-240-7.compute-1.amazonaws.com:5432/d9790in18n8pmm
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registrate"""

    # Get form information.
    user_name = request.form.get("user_name")
    user_password = request.form.get("user_password")

    db.execute("INSERT INTO users (user_name, user_password) VALUES (:user_name, :user_password)",
            {"user_name": user_name, "user_password": user_password})
    db.commit()
    return render_template("success.html")
