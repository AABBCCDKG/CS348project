from models import User, Adoption
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import distinct

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pet(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    status = db.Column(db.String(20))  # available / adopted
    # shelter_id = db.Column(db.Integer, db.ForeignKey('shelter.shelter_id'))

# --- Initialize Database (Run once) ---
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('pet_list.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        pet = Pet(
            name=request.form['name'],
            type=request.form['type'],
            breed=request.form['breed'],
            age=int(request.form['age']),
            status=request.form['status'],
            # shelter_id=int(request.form['shelter_id'])
        )
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('index'))
    # shelters = Shelter.query.all()
    return render_template('pet_form.html', action='Add')

@app.route('/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if request.method == 'POST':
        pet.name = request.form['name']
        pet.type = request.form['type']
        pet.breed = request.form['breed']
        pet.age = int(request.form['age'])
        pet.status = request.form['status']
        # pet.shelter_id = int(request.form['shelter_id'])
        db.session.commit()
        return redirect(url_for('index'))
    # shelters = Shelter.query.all()
    return render_template('pet_form.html', pet=pet, action='Edit')

@app.route('/delete/<int:pet_id>')
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    pet_types = [row[0] for row in db.session.query(distinct(Pet.type)).all()]
    results = []
    if request.method == 'POST':
        pet_type = request.form['type']
        min_age = request.form['min_age']
        max_age = request.form['max_age']
        sql = text("""
            SELECT type, COUNT(*) as count, AVG(age) as avg_age
            FROM pet
            WHERE type = :type AND age BETWEEN :min_age AND :max_age
            GROUP BY type
        """)
        results = db.session.execute(sql, {
            'type': pet_type,
            'min_age': min_age,
            'max_age': max_age
        }).fetchall()
    return render_template('report.html',
                           types=pet_types,
                           results=results)

if __name__ == '__main__':
    app.run(debug=True)