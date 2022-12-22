from user import User

class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor = db.session
            rows = cursor.execute(f"SELECT id, username, password, email , rule from user where username = '{user.username}' ")
            if rows != None:
                for row in rows:
                    user2 = User(row[0],row[1], row[2], row[3], row[4])
                return user2
            else:
                return None
        except Exception as ex:
            return None

    @classmethod
    def getById(self,db,id):
        try:
            cursor = db.session
            sql= """SELECT id, username, password,  email , rule FROM user 
                    WHERE id = '{}'""".format(id)
            rows = cursor.execute(sql)
            if rows != None:
                for row in rows:
                    user = User(row[0],row[1], row[2], row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            return None