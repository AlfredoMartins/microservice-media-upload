import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

# config
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = os.environ.get("MYSQL_PORT")

@app.route('/login', methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    cur = mysql.connect.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username, )
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid creadentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SCRET"), True)
    else:
        return "Invalid credentials", 401

def createJWT(username, secret, auth):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": auth,
        },
        secret,
        algorithm="HS256",
    )

@app.route('/validate', methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decoded(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "Not authorized", 403
    
    return decoded, 200


if __name__ == "__main__":
    print(__name__)
    app.run(host="0.0.0.0", port=5000)