from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VengaPlus'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='default')  # Добавляем поле для ролей

@app.route('/regpage', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'default')  # Получаем роль из формы
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует!', 'error')
            return redirect(url_for('register'))
        if existing_email:
            flash('Пользователь с таким email уже существует!', 'error')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна. Теперь вы можете войти!', 'success')
        return redirect(url_for('login'))
    return render_template('regpage.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
