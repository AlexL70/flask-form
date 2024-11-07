from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Setup the Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_APP_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

# Create a model for the database


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date_str = request.form['start_date']
        start_date = datetime.strptime(date_str, '%Y-%m-%d')
        occupation = request.form['occupation']
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, start_date=start_date, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        flash(f'{first_name}, your form submitted successfully!', 'success')
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
