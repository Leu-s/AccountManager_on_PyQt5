from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import time
import PasswordManager

ui_form = uic.loadUiType('A-Manager.ui')[0]


class AccountManager(QtWidgets.QMainWindow, ui_form):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.pushButton_Generate_pswd.clicked.connect(self.generate_strong_password)  # Кнопка генерации нового пароля
        self.radioButton_default_symbols.toggled.connect(self.on_off_all_symbols)

    def on_off_all_symbols(self):
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
