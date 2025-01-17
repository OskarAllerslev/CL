from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/module1')
def module1():
    return render_template('module1.html')

@app.route('/definite-integral')
def definite_integral():
    return render_template('definite_integral.html')

@app.route('/probability-intro')
def probability_intro():
    return render_template('probability_intro.html')

if __name__ == '__main__':
    app.run(debug=True)
