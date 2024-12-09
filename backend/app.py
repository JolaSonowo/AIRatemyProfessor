from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page

@app.route('/add_professor_score', methods=['POST'])
def add_professor_score():
    data = request.json
    professor_name = data.get('professor_name')
    subject_name = data.get('subject_name')
    score = data.get('score')

    if not professor_name or not subject_name or score is None:
        return jsonify({'error': 'Professor name, subject name, and score are required'}), 400

    # Check if professor exists
    professor = Professor.query.filter_by(name=professor_name).first()
    if not professor:
        professor = Professor(name=professor_name)
        db.session.add(professor)
        db.session.commit()

    # Check if subject exists
    subject = Subject.query.filter_by(name=subject_name, professor_id=professor.id).first()
    if not subject:
        subject = Subject(name=subject_name, professor_id=professor.id)
        db.session.add(subject)
        db.session.commit()

    # Add the score
    new_score = Score(subject_id=subject.id, score=score)
    db.session.add(new_score)
    db.session.commit()

    return jsonify({'message': f'Score {score} for subject {subject_name} added for Professor {professor_name}'}), 201

@app.route('/get_professor_scores/<professor_name>', methods=['GET'])
def get_professor_scores(professor_name):
    professor = Professor.query.filter_by(name=professor_name).first()
    if not professor:
        return jsonify({'error': 'Professor not found'}), 404

    subjects = Subject.query.filter_by(professor_id=professor.id).all()
    results = {}

    for subject in subjects:
        scores = Score.query.filter_by(subject_id=subject.id).all()
        score_list = [score.score for score in scores]
        avg_score = sum(score_list) / len(score_list) if score_list else 0
        results[subject.name] = {'scores': score_list, 'average': avg_score}

    return jsonify({'professor': professor.name, 'subjects': results}), 200

# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
