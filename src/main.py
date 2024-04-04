from flask import Flask, jsonify, request
from models import User
from sql_utilities import SqlUtilities

sql_utility = SqlUtilities(db_path="user.db",
                           table_sql="""CREATE TABLE IF NOT EXISTS users(name, last_name, email, password)""")
sql_utility.disconnect()
app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    register_data = request.json
    name = register_data["name"]
    last_name = register_data["last_name"]
    email = register_data["email"]
    password = register_data["password"]

    user = User(name=name, last_name=last_name, email=email, password=password)
    sql_utility.reconnect()
    sql_utility.im.execute("""INSERT INTO users VALUES (?,?,?,?)""",
                           (user.name, user.last_name, user.email, user.password))
    sql_utility.db.commit()
    sql_utility.disconnect()

    return jsonify(user.to_json())


@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    email = login_data["email"]
    password = login_data["password"]

    sql_utility.reconnect()
    result = sql_utility.im.execute("""SELECT * FROM users WHERE email = ? AND password = ?""", (email, password))
    user = result.fetchone()

    sql_utility.disconnect()

    if not user:
        return "You entered the wrong email or password."

    return jsonify(user)

@app.route('/get-users', methods=['GET'])
def get_users():
    sql_utility.reconnect()
    result = sql_utility.im.execute("""SELECT * FROM users""")
    return_data = result.fetchall()

    sql_utility.disconnect()
    
    return return_data


if __name__ == '__main__':
    app.run()
