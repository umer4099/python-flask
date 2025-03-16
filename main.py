from flask import Flask, request, render_template_string, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.debug = True  # Enable debugging mode

# Database connection
try:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),  
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True  # Enable auto-commit
    cur = conn.cursor()
    print("Database connection successful!")
    
    # Ensure students table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            email VARCHAR(100)
        );
    """)

except Exception as e:
    print("Error connecting to database:", e)

# Routes for CRUD operations
@app.route("/")
def index():
    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()
    return render_template_string("""
        <h1>Student Records</h1>
        <table border="1">
            <tr><th>ID</th><th>Name</th><th>Age</th><th>Email</th><th>Actions</th></tr>
            {% for student in students %}
                <tr>
                    <td>{{ student[0] }}</td>
                    <td>{{ student[1] }}</td>
                    <td>{{ student[2] }}</td>
                    <td>{{ student[3] }}</td>
                    <td>
                        <a href="{{ url_for('edit_student', student_id=student[0]) }}">Edit</a> | 
                        <a href="{{ url_for('delete_student', student_id=student[0]) }}">Delete</a>
                    </td>
                </tr>
            {% endfor %}
        </table>
        <a href="{{ url_for('add_student') }}">Add Student</a>
    """, students=students)



@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        try:
            cur.execute("INSERT INTO students (name, age, email) VALUES (%s, %s, %s)", (name, age, email))
            conn.commit()  # Ensure changes are saved
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error inserting student: {str(e)}"
    return render_template_string("""
        <h1>Add Student</h1>
        <form method="POST">
            Name: <input type="text" name="name"><br>
            Age: <input type="number" name="age"><br>
            Email: <input type="email" name="email"><br>
            <input type="submit" value="Add Student">
        </form>
        <a href="{{ url_for('index') }}">Back to Student List</a>
    """)


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        try:
            cur.execute("UPDATE students SET name=%s, age=%s, email=%s WHERE id=%s", (name, age, email, student_id))
            conn.commit()  # Ensure changes are saved
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error updating student: {str(e)}"
    
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    return render_template_string("""
        <h1>Edit Student</h1>
        <form method="POST">
            Name: <input type="text" name="name" value="{{ student[1] }}"><br>
            Age: <input type="number" name="age" value="{{ student[2] }}"><br>
            Email: <input type="email" name="email" value="{{ student[3] }}"><br>
            <input type="submit" value="Update Student">
        </form>
        <a href="{{ url_for('index') }}">Back to Student List</a>
    """, student=student)


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    try:
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()  # Ensure changes are saved
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting student: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)