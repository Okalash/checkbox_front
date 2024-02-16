from connect_module import Connection_mod
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout, QLineEdit, QComboBox
import sys
from receipt import Receipt
import logging
from datetime import datetime
import uuid

logging.basicConfig(level=logging.INFO, filename="checkbox_log.log",filemode="a")

x_license_key = "test1ea7f100df623647e5657a20"  # TEST462432
pin_code = "5133377032"  # test_dw6uwh6zo

app = QApplication(sys.argv)

# window = QMainWindow()
# window.show()


client_bearer = Connection_mod.login(x_license_key, pin_code)
con_class = Connection_mod(x_license_key, pin_code, client_bearer)

#label = QLabel(client_bearer)

receipt_class = Receipt()
receipt_list = []

class ReceiptWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Фіскальний чек")
        self.resize(800,800)

        self.receipt_uuid = str(uuid.uuid4())

        """Name good"""
        self.good_name = QLineEdit()
        self.good_name.setPlaceholderText("Назва товару")
        self.good_name.textChanged.connect(self.good_name.setText)
        layout.addWidget(self.good_name)

        """Price good"""
        self.good_price = QLineEdit()
        self.good_price.setPlaceholderText("Ціна товару")
        self.good_price.textChanged.connect(self.good_price.setText)
        layout.addWidget(self.good_price)

        """Quantity good"""
        self.good_quantity = QLineEdit()
        self.good_quantity.setPlaceholderText("Кількість товару")
        self.good_quantity.textChanged.connect(self.good_quantity.setText)
        layout.addWidget(self.good_quantity)

        """Value type"""
        self.type_value = QComboBox()
        self.type_value.addItems(["Готівка", "Безготівка"])
        #self.type_value.currentIndexChanged.connect(self.index_changed)
        #How to save value?
        layout.addWidget(self.type_value)

        """Sum value"""
        self.value_sum = QLineEdit()
        self.value_sum.setPlaceholderText("Сума оплати")
        self.value_sum.textChanged.connect(self.value_sum.setText)
        layout.addWidget(self.value_sum)

        """Button to check"""
        self.button_to_pay = QPushButton("Оплата")
        self.button_to_pay.clicked.connect(self.button_to_pay_action)
        layout.addWidget(self.button_to_pay)

        self.setLayout(layout)

    def button_to_pay_action(self):
        good_code = 1
        good_name = self.good_name.text()
        good_price = int(self.good_price.text())
        good_quanity = int(self.good_quantity.text())
        type_value = "CASH"
        value_sum = int(self.value_sum.text())
        payload = {"id":self.receipt_uuid,
                    "goods":[
                            {
                                "good": {
                                    "code":good_code,
                                    "name":good_name,
                                    "price":good_price,
                                    "tax":[8]
                                   },
                                   "quantity":good_quanity
                                }
                            ],
                            "payments":[
                                {
                                    "type":type_value,
                                    "value":value_sum
                                }
                            ],
                        "footer": "Checkbox_front"
                        }

        result = receipt_class.send_receipt(client_bearer, payload)
        receipt_list.append(result)
        print("OK")









class MainWindow(QMainWindow):
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

    """Check ping tax status(online/offline)"""
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
            print(receipt_list)
            #print(result)
        else:
            logging.warning(f"{datetime.now()} Зміну не відкрито!")
            print(f"Зміну не відкрито!")

    """send receipt button action"""
    def send_receipt_clicked(self):
        self.r_window = ReceiptWindow()
        self.r_window.show()
        # receipt_class = Receipt("Ковбаска домашня", 15000, 1)
        # result = receipt_class.send_receipt(client_bearer)
        # print(("-----{0} id: {1}-----").format(result["transaction"]["status"], result["id"]))
        #print(result)


# app.exec()


win = MainWindow()
win.show()
sys.exit(app.exec())
