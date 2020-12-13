import hashlib
import os
import sqlite3

data_path = os.path.abspath(os.curdir)
main_db = data_path + '\\data\\main.db'


class UserAccountDB:
    """
    Using this class, we can work with information
    about users in the database (Logins and passwords).
    Namely, add, change, edit passwords, logins, etc.
    """
    def __init__(self, db_path):
        self.path_to_db = db_path

    def add_new_user(self, login, password):
        """
        The method adds a new user to the database.
        The password is encrypted, the login is unique for each user.


        :param login (str) - is a unique user ID in the database.
        :param password (str) - Password must contain at least 6 characters.It is encrypted and placed in the database
        :return - True or False, depending on the success of the operation.
        """
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',                   # Hash algorithm used
            password.encode('utf-8'),   # Convert password to bytes
            salt,                       # Salt provided
            100000,                     # It is recommended to use at least 100,000 SHA-256 iterations
            dklen=128
        )
        encrypted_password = salt + key

        # We connect the database and add a new user to it
        con_db = sqlite3.connect(self.path_to_db, timeout=10)
        cursor = con_db.cursor()
        result = True

        create_db = """
                CREATE TABLE IF NOT EXISTS "LoginPassword"(
                "id_user" INTEGER PRIMARY KEY AUTOINCREMENT,
                "Login" TEXT NOT NULL UNIQUE,
                "Password" TEXT NOT NULL);"""
        sql = """
                INSERT INTO LoginPassword
                VALUES (?, ?, ?)
                """

        try:
            cursor.execute(create_db)
        except sqlite3.DatabaseError as err:
            print(err, 'here')

        val = (None, login, encrypted_password)  # Total values for transfer to the database

        try:
            cursor.execute(sql, val)  # Execute SQL Query
        except sqlite3.DatabaseError as err:
            print('Error:', err)  # Displaying an error message
            result = False
        else:
            con_db.commit()  # Requesting a transaction

        cursor.close()  # Close the cursor object
        con_db.close()  # Close the connection

        return result


class User:
    def __init__(self, db_path):
        self.user_db = db_path
        self.user_id = None
        self.login = None
        self.user_email = None
        self.access = False
        # self.user_account_db = None
        # self.passwords_amount = 0

    def authorization(self, login, password):
        """Function of user authorization.

        :param login (str) - user login
        :param password (str) - user password
        :return True or False, depending on the result.
        """
        con_db = sqlite3.connect(self.user_db, timeout=10)

        with con_db:
            cursor = con_db.cursor()
            cursor.execute("SELECT id_user, Login, Password FROM LoginPassword")
            login_password = cursor.fetchall()

        for u_id, lgn, psw in login_password:
            if lgn == login:
                # Login match, check password
                salt, key = psw[:32], psw[32:]
                new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128)

                if key == new_key:
                    # If the key is correct,
                    # we provide access to the account
                    self.access = True
                    self.user_id = u_id
                    self.login = login
                    break

        cursor.close()  # Close the cursor object
        con_db.close()  # Close the connection
        return self.access

    def connect_db_with_accounts(self):

        create_sql = """
            CREATE TABLE IF NOT EXISTS "UserData"(
            "user_id" INTEGER,
            "PasswordTo" TEXT NOT NULL,
            "Login"	TEXT NOT NULL,
            "Password" TEXT NOT NULL,
            "UserName" TEXT,
            "Email"	TEXT,
            "LastModDate" TEXT,
            FOREIGN KEY (user_id) REFERENCES LoginPassword(id_user)
            );
            """
        insert_values_in_db = """
                        INSERT INTO 'UserData'
                        VALUES (?,?,?,?,?,?,?)
                        """
        values = (self.user_id,
                  'tanks',
                  'TankLogin',
                  'pswd3124',
                  'Carpe_Diem',
                  'em@ail.com',
                  '12.02.2011')
        con = sqlite3.connect(self.user_db)
        with con:
            cur = con.cursor()
            cur.execute(create_sql)
            try:
                cur.execute(insert_values_in_db, values)
            except sqlite3.DatabaseError as err:
                print('Error:', err)
            else:
                con.commit()
        cur.close()
        con.close()

    def __repr__(self):
        return f'User name: {self.login}\nAuthorization status: {self.access}'

    def __del__(self):
        print(f'{self.login} deleted.')


usr_a_db = UserAccountDB(main_db)
usr_a_db.add_new_user('123qwe', '123qwe')


usr = User(main_db)
usr.authorization('123qwe', '123qwe')
usr.connect_db_with_accounts()
