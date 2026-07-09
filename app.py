from flask import Flask, render_template, request, redirect, session, send_file
from database.db import get_connection
import pandas as pd
import webbrowser
from threading import Timer
from utils.predictor import predict_csv

app = Flask(__name__)
app.secret_key = "fraudguard_secret_key"


# ---------------- HOME ---------------- #

@app.route('/')
def home():
    return render_template('index.html')


# ---------------- LOGIN ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            session['user'] = user[1]

            return redirect('/dashboard')

        return render_template(
            "login.html",
            error="❌ Invalid Email or Password",
            email=email
        )

    return render_template("login.html")


# ---------------- REGISTER ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (username, email, password)
            )

            conn.commit()

            cursor.close()
            conn.close()

            return redirect('/login')

        except:

            conn.rollback()

            cursor.close()
            conn.close()

            return render_template(
                "register.html",
                error="❌ Email already registered.",
                username=username,
                email=email
            )

    return render_template("register.html")


# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template(
        "dashboard.html",
        username=session['user'],
        total_transactions=0,
        fraud_count=0,
        legitimate_count=0
    )


# ---------------- PREDICTION ---------------- #

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        file = request.files['file']

        if file:

            df = pd.read_csv(file)

            total, fraud, legitimate, fraud_transactions = predict_csv(df)

            fraud_transactions.to_csv(
                "fraud_report.csv",
                index=False
            )

            fraud_transactions = fraud_transactions.to_dict(
                orient="records"
            )

            return render_template(
                "result.html",
                username=session['user'],
                total_transactions=total,
                fraud_count=fraud,
                legitimate_count=legitimate,
                fraud_transactions=fraud_transactions
            )

    return render_template("prediction.html")


# ---------------- DOWNLOAD REPORT ---------------- #

@app.route('/download')
def download():

    return send_file(
        "fraud_report.csv",
        as_attachment=True
    )


# ---------------- LOGOUT ---------------- #

@app.route('/logout')

def logout():

    session.pop('user', None)

    return redirect('/login')


# ---------------- AUTO OPEN ---------------- #

def open_browser():

    webbrowser.open_new(
        "http://127.0.0.1:5000"
    )


# ---------------- RUN APP ---------------- #

if __name__ == '__main__':

    Timer(1, open_browser).start()

    app.run(debug=False)