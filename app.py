from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'din_hemmelige_nøgle'  # Skift dette til en sikker nøgle i produktion

# ------------------------------------------------------
# 1) Database-konfiguration
# ------------------------------------------------------
# 'sqlite:///database.db' betyder:
#  - Brug en fil ved navn "database.db" i samme mappe som app.py
#  - Ingen "instance" er involveret her
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------------------------------------------
# 2) Flask-Login konfiguration
# ------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ------------------------------------------------------
# 3) Databasemodeller
# ------------------------------------------------------
class Bruger(UserMixin, db.Model):
    __tablename__ = 'brugere'
    id = db.Column(db.Integer, primary_key=True)
    brugernavn = db.Column(db.String(200), unique=True, nullable=False)
    adgangskode = db.Column(db.String(200), nullable=False)
    rolle = db.Column(db.String(20), nullable=False)

    def set_adgangskode(self, adgangskode):
        self.adgangskode = generate_password_hash(adgangskode)

    def check_adgangskode(self, adgangskode):
        return check_password_hash(self.adgangskode, adgangskode)


class Opgave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(80), nullable=False)
    beskrivelse = db.Column(db.String(200))
    sværhedsgrad = db.Column(db.String(20), nullable=False)  # 'let', 'svær', 'meget_svær'


class Adgang(db.Model):
    __tablename__ = 'adgang'
    bruger_id = db.Column(db.Integer, db.ForeignKey('brugere.id'), primary_key=True)
    opgave_id = db.Column(db.Integer, db.ForeignKey('opgave.id'), primary_key=True)


class GyldigtBrugernavn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brugernavn = db.Column(db.String(80), unique=True, nullable=False)

# ------------------------------------------------------
# 4) Flask-Login user_loader
# ------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return Bruger.query.get(int(user_id))

# ------------------------------------------------------
# 5) Routes
# ------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        brugernavn = request.form['brugernavn']
        adgangskode = request.form['adgangskode']
        print(f"[DEBUG] Forsøger at logge ind med {brugernavn}")

        bruger = Bruger.query.filter_by(brugernavn=brugernavn).first()
        if bruger:
            print(f"[DEBUG] Adgangskode i DB (hash): {bruger.adgangskode}")
            if bruger.check_adgangskode(adgangskode):
                login_user(bruger)
                flash('Du er nu logget ind!', 'success')
                return redirect(url_for('funktioner'))
            else:
                flash('Forkert brugernavn eller adgangskode', 'danger')
        else:
            flash('Forkert brugernavn eller adgangskode', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du er nu logget ud!', 'success')
    return redirect(url_for('login'))

@app.route('/opret-bruger', methods=['GET', 'POST'])
def opret_bruger():
    if request.method == 'POST':
        brugernavn = request.form['brugernavn']
        adgangskode = request.form['adgangskode']
        rolle = request.form['rolle']

        # Tjek om brugernavnet er gyldigt
        gyldigt_brugernavn = GyldigtBrugernavn.query.filter_by(brugernavn=brugernavn).first()
        if not gyldigt_brugernavn:
            flash('Ugyldigt brugernavn. Kontakt administratoren for at få adgang.', 'danger')
            return redirect(url_for('opret_bruger'))

        # Tjek om brugernavnet allerede er oprettet
        eksisterende_bruger = Bruger.query.filter_by(brugernavn=brugernavn).first()
        if eksisterende_bruger:
            flash('Brugernavnet eksisterer allerede!', 'danger')
            return redirect(url_for('opret_bruger'))

        # Opret en ny bruger
        ny_bruger = Bruger(brugernavn=brugernavn, rolle=rolle)
        ny_bruger.set_adgangskode(adgangskode)
        db.session.add(ny_bruger)
        db.session.commit()

        flash('Bruger oprettet!', 'success')
        return redirect(url_for('login'))

    return render_template('opret_bruger.html')

@app.route('/funktioner')
@login_required
def funktioner():
    if current_user.rolle == 'lærer':
        opgaver = Opgave.query.all()
    else:
        opgaver = Opgave.query.join(Adgang).filter(Adgang.bruger_id == current_user.id).all()
    return render_template('funktioner.html', opgaver=opgaver)

@app.route('/integraler')
@login_required
def integraler():
    return render_template('integraler.html')

@app.route('/definite-integral')
@login_required
def definite_integral():
    return render_template('definite_integral.html')

@app.route('/integraleradvanceret')
@login_required
def integraleradvanceret():
    return render_template('integraleradvanceret.html')

@app.route('/probability-intro')
@login_required
def probability_intro():
    return render_template('probability_intro.html')

@app.route('/normalfordelingen')
@login_required
def normalfordelingen():
    return render_template('normalfordelingen.html')

# ------------------------------------------------------
# 6) Automatisk oprettelse af database + testbruger
# ------------------------------------------------------
if __name__ == '__main__':
    # 1) Opret databasen/tabellerne
    with app.app_context():
        db.create_all()
        print("[INFO] db.create_all() udført – 'database.db' er (gen)oprettet.")

        # 2) Opret en testbruger, hvis den ikke allerede findes
        eksisterende_test = Bruger.query.filter_by(brugernavn='test').first()
        if not eksisterende_test:
            test_bruger = Bruger(brugernavn='test', rolle='elev')
            test_bruger.set_adgangskode('test')
            db.session.add(test_bruger)
            db.session.commit()
            print("[INFO] Testbruger 'test' oprettet med password 'test'.")
        else:
            print("[INFO] Testbruger 'test' findes allerede.")

    # 3) Start Flask
    app.run(debug=True)
