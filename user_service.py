import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import request, g
import jwt
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
# we can put it in secretManager or env
SECRET = 'bfg28y7efg238re7r6t32gfo23vfy7237yibdyo238do2v3'

def get_user_with_credentials(email, password):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        # using parameterized queries to prevent SQL injection vulnerability.
        # It uses  placeholders separates the data from the code
        cur.execute('''
            SELECT email, name, password FROM users where email=?''',
            (email,))
        row = cur.fetchone()
    except sqlite3.Error as e:
        logging.error("Database error {}", e)  # Use logging in production
        return None
    finally:
        if con:
            con.close()

        if row is None:
            return None
        email, name, hash = row
        # sha256
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}

def logged_in():
    token = request.cookies.get('auth_token')
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        g.user = data['sub']
        return True
    except jwt.ExpiredSignatureError:
        logging.error("The token has expired.")  # Handle expired token case
        return False
    except jwt.InvalidTokenError:
        logging.error("Invalid token. Please log in again.")  # Handle invalid token case
        return False

def create_token(email):
    now = datetime.utcnow()
    payload = {'sub': email, 'iat': now, 'exp': now + timedelta(minutes=60)}
    try:
        token = jwt.encode(payload, SECRET, algorithm='HS256')
        return token
    except jwt.PyJWTError as e:
        logging.error("Error encoding token: {}", e)  # Log encoding errors
        return None