from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Avinash1234@localhost:3306/student'
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    payment_mode = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Route for the default index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for adding student details and payments
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        payment_mode = request.form['payment_mode']
        amount = float(request.form['amount'])

        # Create a new Student object
        new_student = Student(name=name, country=country, payment_mode=payment_mode, amount=amount)

        # Add the new student to the database
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('show_students'))

    return render_template('add_student.html')

# Route for displaying all students and total count
@app.route('/show_students')
def show_students():
    students = Student.query.all()
    total_students = len(students)
    total_money = sum(student.amount for student in students)
    
    # Initialize counts for online and offline students
    total_online_students = 0
    total_online_money = 0
    total_offline_students = 0
    total_offline_money = 0
    
    # Iterate through students to calculate totals
    for student in students:
        if student.payment_mode == 'Online':
            total_online_students += 1
            total_online_money += student.amount
        elif student.payment_mode == 'Offline':
            total_offline_students += 1
            total_offline_money += student.amount
        else:
            # Handle unexpected payment mode values
            print(f"Unexpected payment mode for student {student.name}: {student.payment_mode}")

    return render_template('show_students.html', students=students, total_students=total_students, total_money=total_money,
                           total_online_students=total_online_students, total_online_money=total_online_money,
                           total_offline_students=total_offline_students, total_offline_money=total_offline_money)

if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
