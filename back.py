from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sequences.db' 
db = SQLAlchemy(app)

#"Concernant les fonctionnalités de création de séquences, j'ai travaillé sur une liste de questions prédéfinies."
questions = [
    {"id": 1, "title": "Question 1", "tags": "algorithme"},
    {"id": 2, "title": "Question 2", "tags": "python"},
    {"id": 3, "title": "Question 3", "tags": "python"},
    {"id": 4, "title": "Question 4", "tags": "sql"},
    {"id": 5, "title": "Question 5", "tags": "sql"},
    {"id": 6, "title": "Question 6", "tags": "sql"},
]

@app.route('/')
def home():

    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/filter', methods=['POST'])#filtrer 
def filter_questions():
   
    tag = request.form['tagFilter']
    filtrer_lesquestions= [q for q in questions if tag in q['tags']]
    
    return render_template('index.html', questions=filtrer_lesquestions)


class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    questions = db.relationship('Question', secondary='sequence_question', backref='sequences')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

sequence_question = db.Table('sequence_question',
    db.Column('sequence_id', db.Integer, db.ForeignKey('sequence.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
)


with app.app_context():
    db.create_all()




@app.route('/create_sequence', methods=['POST'])#listes des
def create_sequence():
    sequence_title = request.form['sequenceTitle']
    selected_questions = request.form.getlist('selectedQuestions[]')
    sequence = Sequence(title=sequence_title)

    
    for question_id in selected_questions:
        question = Question.query.filter_by(id=question_id).first()
        if question is not None:
            sequence.questions.append(question)

    
    db.session.add(sequence)
    db.session.commit()
    sequences = Sequence.query.all()
    return render_template('sequences.html', sequences=sequences)

@app.route('/delete_sequence/<int:id>', methods=['POST'])
def delete_sequence(id):
    
    sequence = Sequence.query.get(id)
    db.session.delete(sequence)
    db.session.commit()

    try:
        
        sequences = Sequence.query.all()

       
        return render_template('sequences.html', sequences=sequences)
    except:
        db.session.rollback()
        raise



@app.route('/view_sequence/<int:sequence_id>')#afficher la sequence
def view_sequence(sequence_id):
    sequence = Sequence.query.get(sequence_id)

    if sequence:
        return render_template('view_sequence.html', sequence=sequence_question)
    else:
        message = "La séquence avec l'identifiant {} n'existe pas.".format(sequence_id)
        return render_template('sequences.html', sequences=sequence_question, message=message)





if __name__ == '__main__':
    
    app.run(debug=True)