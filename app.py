from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/integraler')
def integraler():
    return render_template('integraler.html')

@app.route('/definite-integral')
def definite_integral():
    return render_template('definite_integral.html')

@app.route('/probability-intro')
def probability_intro():
    return render_template('probability_intro.html')

@app.route('/normalfordelingen')
def normalfordelingen():
    return render_template('normalfordelingen.html')

if __name__ == '__main__':
    app.run(debug=True)
