from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets

app = Flask(__name__)

# Configure database
db_name = 'testing.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for flash messages
app.secret_key = secrets.token_hex(16)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Task model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"
with app.app_context():
    db.create_all()

    
# Homepage - Add & List tasks
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
            return redirect("/")
        except Exception as e:
            flash(f"Error occurred: {e}", "error")
            return redirect("/")
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

# View individual task
@app.route("/task/<int:id>")
def task_detail(id):
    task = MyTask.query.get_or_404(id)
    return render_template("task_detail.html", task=task)

# Delete a task
@app.route("/delete/<int:id>")
def delete(id):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        flash("Task deleted successfully!", "success")
        return redirect("/")
    except Exception as e:
        flash(f"Error occurred: {e}", "error")
        return redirect("/")

# Edit/Update a task
@app.route("/update/<int:id>", methods=["POST", "GET"])
def edit(id):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            flash("Task updated successfully!", "success")
            return redirect("/")
        except Exception as e:
            flash(f"Error occurred: {e}", "error")
            return redirect(f"/update/{id}")
    else:
        return render_template('edit.html', task=task)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
