from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        start_date = request.form['start_date']
        occupation = request.form['occupation']
        print(
            f"Entered details: {first_name}, {last_name}, {email}, {start_date} {occupation}")
    return render_template('index.html')


app.run(debug=True, port=5555)
