from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import PasswordManager
import UserAccount

ui_form = uic.loadUiType('A-Manager.ui')[0]


class AccountManager(QtWidgets.QMainWindow, ui_form):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        data_base = UserAccount.main_db
        UserAccount.create_db(data_base)
        self.user_account_db = UserAccount.UserAccountDB(db_path=data_base)
        self.user = UserAccount.User(db_path=data_base)
        if not self.user.access:
            self.change_access_rights()

        self.btn_AddNew.clicked.connect(self.add_new_user)
        self.btn_Apply.clicked.connect(self.fill_in_the_table)
        self.Btn_Login.clicked.connect(self.redirect_btn_login)
        self.btn_AddNewAccount.clicked.connect(self.add_new_account)
        self.btn_generate_pswd.clicked.connect(self.new_acc_gen_pswd_btn)
        self.pushButton_Generate_pswd.clicked.connect(self.generate_strong_password)  # Кнопка генерации нового пароля
        self.radioButton_default_symbols.toggled.connect(self.on_off_all_buttons_in_generate_password)

        #######################
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.table_context_menu)

    def table_context_menu(self, pos):
        menu = QtWidgets.QMenu()
        copy_item = menu.addAction('Copy')
        edit_item = menu.addAction('Edit line')
        delete_line = menu.addAction('Delete line')

        edit_item.setEnabled(False)
        copy_item.setEnabled(False)

        menu.addSeparator()

        action = menu.exec_(QtGui.QCursor.pos())
        if action == delete_line:
            self.delete_row(pos)

    def delete_row(self, pos):
        """Record deletion method."""
        row = self.tableWidget.rowAt(pos.y())
        if row < 0:
            return

        self.tableWidget.selectRow(row)

        self.fill_in_the_table(row_id=True)

        row_id = self.tableWidget.item(row, 6).text()

        self.fill_in_the_table(row_id=False)
        
        confirmation = self.msg_delete_row()

        if confirmation:
            self.user.remove_data_from_db(int(row_id))
            self.fill_in_the_table()

    def msg_delete_row(self):
        """Window for user confirmation of record deletion"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(msg.Warning)
        msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))
        msg.setWindowTitle('Confirm deletion')
        msg.setText('Are you sure you want to delete the entry?')
        msg.setInformativeText('INFO: Once deleted, you cannot restore it.')
        msg.addButton('Cancel', msg.RejectRole)
        delete_btn = msg.addButton('Delete', msg.AcceptRole)
        msg.exec()
        if msg.clickedButton() == delete_btn:
            return True
        else:
            return False

    def new_acc_gen_pswd_btn(self):
        """
        The method fills in the password automatically
        if the flag is set.
        """
        if self.btn_generate_pswd.isChecked():
            self.line_password.setText(PasswordManager.create_password(default=True))
            self.line_password.setEnabled(False)
        else:
            self.line_password.setEnabled(True)

    def fill_in_the_table(self, row_id=False):
        """
        The method fills the table in the application.
        Clears it before filling.
        """
        # Clearing the table
        [self.tableWidget.removeRow(i) for i in reversed(range(self.tableWidget.rowCount()))]

        s_login = self.ShowLogins.isChecked()
        s_email = self.ShowEmails.isChecked()
        s_pswd = self.ShowPswrd.isChecked()
        s_usr_name = self.ShowUsrNames.isChecked()
        s_date = self.ShowDate.isChecked()

        # We receive information from the database for filling
        data = self.user.output_user_data_from_table()
        if data:
            for item in data:
                self.tableWidget.insertRow(0)
                self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(item[0]))
                self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(item[1] if s_login else None))
                self.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(item[2] if s_pswd else None))
                self.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(item[3] if s_usr_name else None))
                self.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(item[4] if s_email else None))
                self.tableWidget.setItem(0, 5, QtWidgets.QTableWidgetItem(item[5] if s_date else None))
                self.tableWidget.setItem(0, 6, QtWidgets.QTableWidgetItem(str(item[6])) if row_id else None)
            else:
                self.tableWidget.setColumnHidden(1, True if not s_login else False)
                self.tableWidget.setColumnHidden(2, True if not s_pswd else False)
                self.tableWidget.setColumnHidden(3, True if not s_usr_name else False)
                self.tableWidget.setColumnHidden(4, True if not s_email else False)
                self.tableWidget.setColumnHidden(5, True if not s_date else False)
                self.tableWidget.setColumnHidden(6, True if not row_id else False)
                self.tableWidget.resizeColumnsToContents()

    def add_new_account(self):
        """
        Method of adding a new account by the user. There are notifications
        about the result of the operation.
        """

        if self.checkMatches.isChecked():
            matches = self.user.check_matches(pswd_to=self.lineEdit_pswd_to.text(),
                                              login=self.line_login.text(),
                                              pswd=self.line_password.text(),
                                              usr_name=self.line_username.text(),
                                              email=self.line_Email.text())
            if matches:
                confirmation = self.msg_check_matches()
                if not confirmation:
                    self.label_add_info.setText('Operation canceled by user.')
                    return

        add = self.user.add_new_data(password_to=self.lineEdit_pswd_to.text(),
                                     login=self.line_login.text(),
                                     password=self.line_password.text(),
                                     user_name=self.line_username.text(),
                                     email=self.line_Email.text())
        if add:
            self.label_add_info.setText('Data added successfully!')
            self.fill_in_the_table()
        else:
            self.label_add_info.setText('No data added =(')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(msg.Information)
            msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))
            msg.setWindowTitle('Unknown error')
            msg.setText('Please check the information.')
            msg.setInformativeText('INFO:\nApplication length at least 4 characters.\n'
                                   'Login length is at least 4 characters.\n'
                                   'Password length at least 6 characters.')
            msg.exec()

    def msg_check_matches(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(msg.Warning)
        msg.setWindowIcon(QtGui.QIcon('\\static\\icon.png'))
        msg.setWindowTitle('Found a match')
        msg.setText('What are you going to do?')
        msg.setInformativeText('INFO: You can add an entry or cancel the operation.')
        msg.addButton('Cancel', msg.RejectRole)
        confirm_btn = msg.addButton('Confirm', msg.AcceptRole)
        msg.exec()
        if msg.clickedButton() == confirm_btn:
            return True
        else:
            return False

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
            self.fill_in_the_table()
            self.Line_Login.setEnabled(False if status else True)
            self.Line_Password.setEnabled(False if status else True)
            self.Btn_Login.setEnabled(status)
            self.tableWidget.setEnabled(status)
            self.Btn_Login.setText('Log out')
            self.Line_Password.setText('*'*len(self.Line_Password.text()))
            self.UserStatus.setText(f'Welcome, {self.user.login}!\n'
                                    # FIX IT LATER
                                    f'You have ---- accounts.\n'
                                    f'{"Email: "}'
                                    f'{self.user.user_email if self.user.user_email else "Not specified."}')
        elif not status:
            [self.tableWidget.removeRow(i) for i in reversed(range(self.tableWidget.rowCount()))]
            self.tableWidget.setEnabled(status)
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

    def add_new_user(self):
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
            else:
                self.UserStatus.setText(f'A user with this name ({user_name}) already exists '
                                        f'in the database.\n'
                                        'Please, try another name.')
                msg.setWindowTitle('Registration error')
                msg.setText(f'A user with this name ({user_name}) already exists in the database.')
                msg.setInformativeText('Please, try another name.')
                msg.exec()

    def generate_strong_password(self):
        """
        New password generation method.
        """

        if self.checkBox_0_9.isChecked() == self.checkBox_a_z.isChecked() \
                == self.checkBox_A_Z.isChecked is False:
            self.checkBox_Sym.setChecked(True)

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
