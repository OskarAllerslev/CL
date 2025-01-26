from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
    laerer_id = db.Column(db.Integer, db.ForeignKey('brugere.id'))  # Foreign key
    
    # Korrekt konfiguration af relation
    elever = db.relationship(
        'Bruger', 
        backref=db.backref('laerer', remote_side=[id])  # <-- Vigtigt: remote_side=[id]
    )
    def get_total_points(self):
        total = db.session.query(db.func.sum(BrugerPoints.points)).filter(BrugerPoints.bruger_id == self.id).scalar()
        return total if total else 0
    
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


class BrugerPoints(db.Model):
    __tablename__ = 'bruger_points'
    id = db.Column(db.Integer, primary_key=True)
    bruger_id = db.Column(db.Integer, db.ForeignKey('brugere.id'), nullable=False)
    opgave_id = db.Column(db.Integer, db.ForeignKey('opgave.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    # Relation til Bruger og Opgave
    bruger = db.relationship('Bruger', backref='points')
    opgave = db.relationship('Opgave', backref='points')

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


@app.route('/check')
def check():
    gyldige = GyldigtBrugernavn.query.all()
    return f"Gyldige brugernavne: {[g.brugernavn for g in gyldige]}"


@app.route('/give-points', methods=['POST'])
@login_required
def give_points():
    data = request.get_json()  # Hent JSON-data fra anmodningen
    if not data:
        return jsonify({'success': False, 'message': 'Ingen data modtaget'}), 400

    opgave_id = data.get('opgave_id')
    points = data.get('points')

    if not opgave_id or not points:
        return jsonify({'success': False, 'message': 'Manglende opgave_id eller points'}), 400

    # Tjek om brugeren allerede har løst denne opgave
    existing_points = BrugerPoints.query.filter_by(bruger_id=current_user.id, opgave_id=opgave_id).first()
    if existing_points:
        return jsonify({'success': False, 'message': 'Du har allerede fået points for denne opgave.'}), 400

    # Gem points i databasen
    new_points = BrugerPoints(bruger_id=current_user.id, opgave_id=opgave_id, points=points)
    db.session.add(new_points)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Points tilføjet!'}), 200
@app.route('/opret-bruger', methods=['GET', 'POST'])
def opret_bruger():
    if request.method == 'POST':
        brugernavn = request.form['brugernavn']
        adgangskode = request.form['adgangskode']
        rolle = request.form['rolle']

        # Tjek om brugernavnet er gyldigt
        gyldigt_brugernavn = GyldigtBrugernavn.query.filter_by(brugernavn=brugernavn).first()
        print(f"[DEBUG] Søger efter gyldigt brugernavn: {brugernavn}. Fundet: {gyldigt_brugernavn}")
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

from sqlalchemy.orm import joinedload  # Tilføj denne import

@app.route('/laerer-dashboard', methods=['GET', 'POST'])
@login_required
def laerer_dashboard():
    if current_user.rolle != 'lærer':
        flash("Adgang nægtet: Kun for lærere", 'danger')
        return redirect(url_for('index'))
    
    search_query = request.args.get('search', '')
    query = Bruger.query.filter_by(rolle='elev').options(joinedload(Bruger.laerer))
    
    if search_query:
        query = query.filter(Bruger.brugernavn.ilike(f'%{search_query}%'))
    
    elever = query.all()
    return render_template('laerer_dashboard.html', elever=elever, search_query=search_query)

@app.route('/tilknyt-laerer/<int:elev_id>', methods=['POST'])
@login_required
def tilknyt_laerer(elev_id):
    if current_user.rolle != 'lærer':
        flash("Adgang nægtet", 'danger')
        return redirect(url_for('index'))
    
    elev = Bruger.query.get_or_404(elev_id)
    elev.laerer_id = current_user.id
    db.session.commit()
    flash(f'{elev.brugernavn} er nu tilknyttet dig!', 'success')
    return redirect(url_for('laerer_dashboard'))

@app.route('/fjern-tilknytning/<int:elev_id>', methods=['POST'])
@login_required
def fjern_tilknytning(elev_id):
    if current_user.rolle != 'lærer':
        flash("Adgang nægtet", 'danger')
        return redirect(url_for('index'))
    
    elev = Bruger.query.get_or_404(elev_id)
    if elev.laerer_id == current_user.id:
        elev.laerer_id = None
        db.session.commit()
        flash(f'Tilknytning til {elev.brugernavn} fjernet!', 'success')
    else:
        flash('Du kan kun fjerne dine egne elever', 'warning')
    
    return redirect(url_for('laerer_dashboard'))

@app.route('/points')
@login_required
def points():
    return render_template('points.html')

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
    app.run(debug=True)
