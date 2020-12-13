import hashlib
import os
import sqlite3

# salt_from_storage = salt + key
# salt_from_storage = salt[:32]
# key_from_storage = key[32:]


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.user_email = None
        self.access = False

    def __repr__(self):
        return self.login + ' '.join([self.user_email if self.user_email else 'User email not specified.'])


class UserAccountDB:
    """
    Using this class, we can work with information
    about users in the database (Logins and passwords).
    Namely, add, change, edit passwords, logins, etc.
    """
    def __init__(self):
        self.path_to_db = \
            "C:\\Users\\Leus\\Desktop\\Different programs\\Py Programs\\Менеджер паролей\\data\\user_accounts.db"

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
        encrypted_password = str(salt + key)

        # We connect the database and add a new user to it
        con_db = sqlite3.connect(self.path_to_db)
        cursor = con_db.cursor()
        result = True

        sql = """
        INSERT INTO LoginPassword
        VALUES (?, ?, ?)
        """

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
