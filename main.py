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

        msg = QtWidgets.QMessageBox()
        msg.setIcon(msg.Information)
        msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))
        msg.resize(50, 500)

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
                msg.exec_()
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
                msg.exec_()

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
