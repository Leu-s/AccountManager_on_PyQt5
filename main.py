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

        self.user_account_db = UserAccount.UserAccountDB()
        self.user_is_authorized = False

        self.pushButton_Generate_pswd.clicked.connect(self.generate_strong_password)  # Кнопка генерации нового пароля
        self.radioButton_default_symbols.toggled.connect(self.on_off_all_buttons_in_generate_password)
        self.btn_AddNew.clicked.connect(self.add_new_account)

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

        if not check_user_name:
            self.Line_Login.setText('Valid parameters: length > 3, A-Z, a-z, 0-9, _ ')
        if not check_password[0]:
            self.Line_Password.setText('Password is not correct, try this: ' + check_password[1])

        if check_password[0] and check_user_name:
            add = self.user_account_db.add_new_user(login=user_name, password=password)
            if add:
                self.UserStatus.setText(f'The user ({user_name}) has been successfully added to the database.\n'
                                        'Sign in to your account.')
            else:
                self.Line_Login.setText('Unknown error, user not added.')
                self.Line_Password.setText('Please, try again.')

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
