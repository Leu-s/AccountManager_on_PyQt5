from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import time
import PasswordManager
import UserAccount

ui_form = uic.loadUiType('A-Manager.ui')[0]


class AccountManager(QtWidgets.QMainWindow, ui_form):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        user_db = UserAccount.data_base_path
        self.user_account_db = UserAccount.UserAccountDB(db_path=user_db)

        self.user = UserAccount.User(db_path=user_db)
        if not self.user.access:
            self.change_access_rights()

        self.pushButton_Generate_pswd.clicked.connect(self.generate_strong_password)  # Кнопка генерации нового пароля
        self.radioButton_default_symbols.toggled.connect(self.on_off_all_buttons_in_generate_password)
        self.btn_AddNew.clicked.connect(self.add_new_account)

        self.Btn_Login.clicked.connect(self.redirect_btn_login)

    def redirect_btn_login(self):
        """
        Redirect the program to functions self.authorization() or change_access_rights
        depending on the user's authorization status.
        If the user was logged in, log out of the account.
        """
        if not self.user.access:
            self.authorization()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(msg.Information)
            msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))
            msg.setWindowTitle('Confirm exit')
            msg.setText('Are you sure you want to log out of your account?')
            msg.addButton('Cancel', msg.RejectRole)
            ok_btn = msg.addButton('OK', msg.AcceptRole)
            msg.exec_()
            if msg.clickedButton() == ok_btn:
                self.user.access = False
                self.change_access_rights()

    def authorization(self):
        """
        Authorizing the user.
        """
        user_name = self.Line_Login.text()
        password = self.Line_Password.text()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(msg.Information)
        msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))

        if len(password) + len(user_name) == 0:
            msg.setWindowTitle('Invalid login or password')
            msg.setText('Login and password fields are empty.')
            msg.setInformativeText('INFO: Enter your username and password and try again.\n'
                                   'If you do not have an account - register.')
            msg.setDefaultButton(msg.Default)
            msg.exec_()

        elif len(user_name) not in range(3, 13) or len(password) not in range(6, 26):
            msg.setWindowTitle('Invalid login or password')
            msg.setText('Check the spelling of the username and password.')
            msg.setInformativeText('INFO: Check your keyboard layout and if Caps Lock is off.')
            msg.exec_()

        else:
            start = self.user.authorization(login=user_name, password=password)
            if start:
                msg.setWindowTitle('Authorization was successful!')
                msg.setText('Now you have access to all the functionality.')
                msg.setInformativeText('INFO: Enjoy fast access to all your passwords!')
                msg.exec_()
            else:
                msg.setWindowTitle('Authorization failed')
                msg.setText('Try again.')
                msg.setInformativeText('INFO: Check the spelling of the username and password.')
                msg.exec_()

        return self.change_access_rights() if self.user.access else None

    def change_access_rights(self):
        """
        The method changes the user's access rights
        depending on whether he is authorized or not.
        """
        status = self.user.access
        self.AddNewAccount.setEnabled(status)
        self.TBL_group_box.setEnabled(status)
        self.btn_AddNew.setEnabled(False if status else True)
        if status:
            self.Line_Login.setEnabled(False if status else True)
            self.Line_Password.setEnabled(False if status else True)
            self.Btn_Login.setEnabled(status)
            self.Btn_Login.setText('Log out')
            self.Line_Password.setText('*'*len(self.Line_Password.text()))
            self.UserStatus.setText(f'Welcome, {self.user.login}!\n'
                                    f'You have {self.user.passwords_amount} accounts.\n'
                                    f'{"Email: "}'
                                    f'{self.user.user_email if self.user.user_email else "Not specified."}')
        elif not status:
            self.UserInitialization.setEnabled(False if status else True)
            self.Line_Login.setEnabled(False if status else True)
            self.Line_Password.setEnabled(False if status else True)
            self.Btn_Login.setText('Log in')
            self.Btn_Login.setEnabled(False if status else True)
            self.Line_Password.setText('')
            self.UserStatus.setText('Sign in to your account')

    def on_off_all_buttons_in_generate_password(self):
        """
        Changing the state of buttons with valid characters to generate a password.
        """
        enable_status = [True if not self.radioButton_default_symbols.isChecked() else False]
        check_status = [False if not enable_status else True]
        self.checkBox_a_z.setChecked(check_status[0])
        self.checkBox_a_z.setEnabled(enable_status[0])
        self.checkBox_A_Z.setChecked(check_status[0])
        self.checkBox_A_Z.setEnabled(enable_status[0])
        self.checkBox_0_9.setChecked(check_status[0])
        self.checkBox_0_9.setEnabled(enable_status[0])
        self.checkBox_Sym.setChecked(check_status[0])
        self.checkBox_Sym.setEnabled(enable_status[0])

    def add_new_account(self):
        """
        Method for adding a new user in to data base
        """
        user_name = self.Line_Login.text()
        password = self.Line_Password.text()
        check_user_name = PasswordManager.check_correct_username(user_name)
        check_password = PasswordManager.password_security_check(password)

        msg = QtWidgets.QMessageBox()
        msg.setIcon(msg.Information)
        msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))

        if not check_user_name and not check_password[0]:
            msg.setWindowTitle('Invalid login and password')
            msg.setText('Generate password automatically?')
            msg.setInformativeText('INFO: Valid characters: 0-9, A-Z, a-z, _\nLogin: 3 < length < 13\n'
                                   'Password: 6 < length < 26')
            msg.addButton('Cancel', msg.RejectRole)
            generate_password_btn = msg.addButton('Generate password', msg.ActionRole)
            msg.setDefaultButton(generate_password_btn)
            msg.exec()

            if msg.clickedButton() == generate_password_btn:
                self.Line_Password.setText(PasswordManager.create_password(default=True))

        elif check_user_name or check_password[0]:
            if not check_user_name:
                msg.setWindowTitle('Invalid login')
                msg.setText('Try again.')
                msg.setInformativeText('INFO: Valid characters: 0-9, A-Z, a-z, _\n3 < length < 13')
                msg.exec()

            elif not check_password[0]:
                msg.setWindowTitle('Invalid password')
                msg.setText('INFO: Valid characters: 0-9, A-Z, a-z, _')
                msg.setInformativeText('Generate password automatically?')
                msg.addButton('Cancel', msg.RejectRole)
                generate_password_btn = msg.addButton('Generate password', msg.ActionRole)
                msg.setDefaultButton(generate_password_btn)
                msg.exec()
                if msg.clickedButton() == generate_password_btn:
                    self.Line_Password.setText(PasswordManager.create_password(default=True))

        if check_password[0] and check_user_name:
            add = self.user_account_db.add_new_user(login=user_name, password=password)
            if add:
                self.UserStatus.setText(f'The user ({user_name}) has been successfully added to the database.\n'
                                        'Sign in to your account.')
                msg.setWindowTitle('Successful registration')
                msg.setText('Congratulations!')
                msg.setInformativeText('Now log in using your data to open access to all the possibilities =)')
                msg.exec()

    def generate_strong_password(self):
        """
        New password generation method.
        """

        if self.checkBox_0_9.isChecked() == self.checkBox_a_z.isChecked() \
                == self.checkBox_A_Z.isChecked is False:
            self.checkBox_Sym.setChecked(True)
            print(self.checkBox_Sym.isChecked())

        password = PasswordManager.create_password(s_amount=int(self.symbols_amount.text()),
                                                   num=self.checkBox_0_9.isChecked(),
                                                   low_reg=self.checkBox_a_z.isChecked(),
                                                   high_reg=self.checkBox_A_Z.isChecked(),
                                                   s_symbols=self.checkBox_Sym.isChecked())

        self.lineEdit_Ready_Pass.setText(password)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AccountManager()
    window.show()  # Show the window
    app.exec_()  # Start application


if __name__ == '__main__':
    main()
