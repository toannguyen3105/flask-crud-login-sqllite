from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password,email="", rule = 2):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.rule = rule

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @classmethod
    def get(self, db, id):
        conn = db.connect()
        curr = conn.cursor()

        sql = f"SELECT user_id, user_name, user_email, user_role FROM `sounds`.`usuarios` WHERE user_id = '{id}'"

        curr.execute(sql)

        user = curr.fetchone()

        if user != None:
            # Entonces el usuario estaba en la base de datos
            # Como esto se utiliza cuando el usuario ya inicio sesion la contraseña ya no es importante
            return User(user[0], user[1], user[2], is_admin=user[3])
        else:
            return None