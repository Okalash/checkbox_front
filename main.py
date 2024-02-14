from connect_module import Connection_mod
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton
import sys
from receipt import Receipt
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename="checkbox_log.log",filemode="a")

x_license_key = "test1ea7f100df623647e5657a20"  # TEST462432
pin_code = "5133377032"  # test_dw6uwh6zo

app = QApplication(sys.argv)

# window = QMainWindow()
# window.show()


client_bearer = Connection_mod.login(x_license_key, pin_code)
con_class = Connection_mod(x_license_key, pin_code, client_bearer)

#label = QLabel(client_bearer)



class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setWindowTitle("Checkbox Front")
        self.resize(800, 800)

        """open shift button"""
        open_shift_button = QPushButton("Відкрити зміну", self)
        open_shift_button.move(350, 400)
        open_shift_button.setCheckable(True)
        open_shift_button.clicked.connect(self.open_shift_clicked)

        """receipt button"""
        send_receipt_button = QPushButton("Провести чек", self)
        send_receipt_button.move(350, 450)
        send_receipt_button.setCheckable(True)
        send_receipt_button.clicked.connect(self.send_receipt_clicked)

        """close shift button"""
        close_shift_button = QPushButton("Закрити зміну", self)
        close_shift_button.move(350, 500)
        close_shift_button.setCheckable(True)
        close_shift_button.clicked.connect(self.close_shift_clicked)

    """open shift button action"""
    def open_shift_clicked(self):

        if con_class.is_last_shift_opened(client_bearer):
            logging.warning(f"{datetime.now()} Зміну не закрито! \n")
            print("Зміну не закрито!")
        else:
            self.check_ping_tax()
            result = con_class.open_shift()
            print(f"-----{result['status']}-----")
            logging.info(f"{datetime.now()} Open shift: {result} \n\n")

    def check_ping_tax(self):
        ping_tax = con_class.ping_tax_service(x_license_key)
        if ping_tax["status"] != "DONE":
            logging.critical(f"{datetime.now()} Статус офлайн!")
            print("Offline")
        else:
            logging.info(f"{datetime.now()} Система онлайн.")
            print("Online")

    """close shift button action"""
    def close_shift_clicked(self):
        if con_class.is_last_shift_opened(client_bearer):
            self.check_ping_tax()
            result = con_class.close_shift()
            print(f"-----{result['status']}-----")
            logging.info(f"{datetime.now()} Close shift: {result} \n\n")
            #print(result)
        else:
            logging.warning(f"{datetime.now()} Зміну не відкрито!")
            print(f"Зміну не відкрито!")

    """send receipt button action"""
    def send_receipt_clicked(self):
        receipt_class = Receipt("Ковбаска домашня", 15000, 1)
        result = receipt_class.send_receipt(client_bearer)
        print(("-----{0} id: {1}-----").format(result["transaction"]["status"], result["id"]))
        #print(result)


# app.exec()


win = Window()
win.show()
sys.exit(app.exec())
