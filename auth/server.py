import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
server.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
server.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
server.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
server.config['MYSQL_PORT'] = int(os.environ.get("MYSQL_PORT", 3306))

"""if not server.config['MYSQL_HOST'] or not os.environ.get("JWT_SECRET"):
    raise EnvironmentError("Missing critical environment variables")
"""
@server.route('/login', methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username, )
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
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

@server.route('/validate', methods=["POST"])
def validate():
    if 'Authorization' not in request.headers:
        return "Missing credentials", 401

    encoded_jwt = request.headers["Authorization"].split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return "Token expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 401
    
    return decoded, 200


if __name__ == "__main__":
    print(__name__)
    server.run(host="0.0.0.0", port=5000)