import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash

from forms import RegistrationForm
from modelUser import ModelUser
from user import User

SECRET_KEY = os.urandom(32)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        _userName = request.form.get('userName')
        _userPass = request.form.get('userPass')
        user = User(0, _userName, _userPass)
        dbUserInfo = ModelUser.login(db, user)

        if dbUserInfo != None:
            if User.check_password(dbUserInfo.password, _userPass):
                login_user(dbUserInfo)
                return redirect(url_for('user'))
            else:
                flash("Invalid password ...")
                return redirect(url_for('login'))
        else:
            flash('Username does not exist')
            return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def reg():
    # validate form
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        # create user with rule = normal user
        userReg = User(1, name, password, email, 2)
        sql_insert = f"""INSERT INTO user (username,password,email,rule) \
          VALUES ('{userReg.username}', '{generate_password_hash(userReg.password)}', '{userReg.email}', '{userReg.rule}')"""
        curr = db.session
        try:
            curr.execute(sql_insert)
            curr.commit()
        except Exception as e:
            raise Exception(e)
        else:
            return redirect(url_for('login'))
        finally:
            curr.commit()

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def welcome():
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return ModelUser.getById(db, user_id)


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    cursor = db.session
    sql = "SELECT id, username, password, email , rule from user"
    rows = cursor.execute(sql).fetchall()
    if current_user.rule == 2:
        page = render_template("home.html", users=rows, user=current_user)
    else:
        if current_user.rule == 1:
            page = render_template("homeAdmin.html", users=rows, user=current_user)
        else:
            page = render_template("homeSAdmin.html", users=rows, user=current_user)
    return page


@app.route("/user/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit(user_id):
    form = RegistrationForm()
    user = ModelUser.getById(db, user_id)
    if request.form:
        newEmail = request.form.get("email")
        newRule = request.form.get("rule")
        cursor = db.session
        cursor.execute(f"UPDATE USER set EMAIL = '{newEmail}' , RULE = {newRule} where ID = {user_id}")
        cursor.commit()
        return redirect("/user")
    return render_template("edit.html", user=user, form=form)


@app.route("/user/delete/<int:user_id>")
@login_required
def delete(user_id):
    db.session.execute(f"DELETE from COMPANY where ID = {user_id};")
    return redirect("/user")


if __name__ == "__main__":
    app.run()
