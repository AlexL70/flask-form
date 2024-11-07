from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from datetime import datetime

# Setup the Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_APP_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "alexander.levinson.70@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("APP2_PORTFOLIO_EMAIL_PASSWORD")
db = SQLAlchemy(app)
mail = Mail(app)

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
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date_str = request.form['start_date']
        start_date = datetime.strptime(date_str, '%Y-%m-%d')
        occupation = request.form['occupation']
        # Save the form data to the database
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, start_date=start_date, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        # Send an email to the user
        message_body = f"""\
        Dear {first_name},

        Your form has been submitted successfully.

        Here are the details you submitted:
        First Name: {first_name}
        Last Name: {last_name}
        Email: {email}
        Start Date: {start_date}
        Occupation: {occupation}
        
        Thank you for applying to our company.
        """
        message = Message(subject='Form Submission',
                          sender=app.config["MAIL_USERNAME"], recipients=[
                              email],
                          body=message_body)
        mail.send(message)
        # Show a success message in browser
        flash(f'{first_name}, your form submitted successfully!', 'success')
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
