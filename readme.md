#### Install libs if not exists
```
$ pip install -r requirements.txt
```
```
#### Run Flash App
`` $ flask run ``
```

### run Application Flask
http://127.0.0.1:5000/

### The script program:

- There are already 3 users in the database:

user/pass
```
superadmin/123456
admin/123456
normaluser/123456
```

Register http://127.0.0.1:5000/register by default when registering in the form, a normal user will be created

+ Super Admin : after login redirect http://127.0.0.1:5000/user, see full information of user and have permissions edit, delete users
+ Admin : permissions see the infomation Username, Email
+ User : permissions see the infomation Username


### when not logged in, access to other paths other than /login is not allowed.
