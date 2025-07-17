from flask import Flask, render_template, request, redirect, session, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
Scss(app, static_dir="static", asset_dir="static/scss")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    username = db.Column(db.String(80), nullable=False)
    def __repr__(self) -> str:
        return f"Task {self.id}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        if not username:
            return render_template("login.html", error="Username required")
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session["username"] = username
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/", methods=["POST", "GET"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task, username=username)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        tasks = MyTask.query.filter_by(username=username).order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks, username=username)

@app.route("/delete/<int:id>")
def delete(id:int):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    delete_task = MyTask.query.filter_by(id=id, username=username).first_or_404()
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def update(id:int):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    edit_task = MyTask.query.filter_by(id=id, username=username).first_or_404()
    if request.method == "POST":
        edit_task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("edit.html", task=edit_task)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
