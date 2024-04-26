import sqlite3
import logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
def get_balance(account_number, owner):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT balance FROM accounts where id=? and owner=?''',
            (account_number, owner))
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    except sqlite3.DatabaseError as e:
        logging.error("Database error {}", e) # Ideally, use logging instead of print in production
        return None  # Returning None or re-raising after logging could be a design decision
    finally:
        con.close()

def do_transfer(source, target, amount):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT id FROM accounts where id=?''',
            (target,))
        row = cur.fetchone()
        if row is None:
            return False
        cur.execute('''
            UPDATE accounts SET balance=balance-? where id=?''',
            (amount, source))
        cur.execute('''
            UPDATE accounts SET balance=balance+? where id=?''',
            (amount, target))
        con.commit()
        return True
    except sqlite3.DatabaseError as e:
        logging.error("Database error {}", e)  # Again, consider using logging
        return False  # Indicates failure to the caller
    finally:
        con.close()