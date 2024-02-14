import uuid
import requests
import connect_module
import logging
from datetime import datetime


logging.basicConfig(level=logging.INFO, filename="checkbox_log.log",filemode="a")


class Receipt:
    '''Why init? omg'''
    def __init__(self, goods, price, type_value):
        self.receipt_uuid = str(uuid.uuid4())
        self.goods = goods
        self.price = price
        self.type_value = type_value
        #x_license_key = "test1ea7f100df623647e5657a20"  # TEST462432
        #pin_code = "5133377032"  # test_dw6uwh6zo
        #client_bearer = connect.Connect.login(x_license_key, pin_code)
        #self.client_bearer = client_bearer

    @property
    def type_value(self):
        return self.__type_value

    @type_value.setter
    def type_value(self, value):
        if value == 0:
            self.__type_value = "CASH"
        elif value == 1:
            self.__type_value = "CASHLESS"
        else:
            print("Error value. Set default CASHLESS")


    def send_receipt(self, token):
        #x_license_key = "test1ea7f100df623647e5657a20"  # TEST462432
        #pin_code = "5133377032"  # test_dw6uwh6zo
        client_bearer = token
        headers = {
            # "test1ea7f100df623647e5657a20", #TEST462432,
            "X-Client-Name": "Checkbox Front",
            "X-Client-Version": "0.1a",
            "Authorization": f"Bearer {client_bearer}"
        }
        receipt_link = "https://api.checkbox.in.ua/api/v1/receipts/sell"
        payload = {"id": self.receipt_uuid,
                   "goods": [
                       {
                           "good": {
                               "code": "001",
                               "name": self.goods,
                               "price": self.price,
                               "tax": [8]
                           },
                           "quantity": 1000
                       }
                   ],
                   "payments": [
                       {
                           "type": self.type_value,
                           "value": self.price
                       }
                   ],
                   "footer": "Checkbox_front"
                   }
        receipt_request = requests.post(receipt_link, json=payload, headers=headers)
        return_json = receipt_request.json()
        logging.info(f"{datetime.now()} Проведено чек: {return_json} \n\n")
        print(return_json)
        return return_json

    def service_receipt(self, sum_value, token):
        client_bearer = token
        service_receipt_link = "https://api.checkbox.in.ua/api/v1/receipts/service"
        service_receipt_id = str(uuid.uuid4())
        headers = {
            # "X-License-Key": x_license_key,  # "test1ea7f100df623647e5657a20", #TEST462432,
            "X-Client-Name": "Checkbox Front",
            "X-Client-Version": "0.1a",
            "Authorization": f"Bearer {client_bearer}"
        }
        payload = {
            "id": service_receipt_id,
            "payment": {
                "type": "CASH",
                "value": str(sum_value)
            }
        }

        receipt_service_request = requests.post(service_receipt_link, json=payload, headers=headers)
        return_json = receipt_service_request.json()
        logging.info(f"{datetime.now()} Внесення/винесення: {return_json} \n\n")
        print(return_json)

    def prepayment_receipt(self, token):
        client_bearer = token
        prepayment_link = "https://api.checkbox.in.ua/api/v1/prepayment-receipts"
        prepayment_uuid = str(uuid.uuid4())
        headers = {
            # "X-License-Key": x_license_key,  # "test1ea7f100df623647e5657a20", #TEST462432,
            "X-Client-Name": "Checkbox Front",
            "X-Client-Version": "0.1a",
            "Authorization": f"Bearer {client_bearer}"
        }
        payload = {
                "cashier_name": "Касир",
                "departament": "Департамент",
                "goods": [
                    {
                        "good": {
                            "code": "001",
                            "name": "Товар 1",
                            "price": 15000,
                            "tax": [
                                8
                            ]
                        },
                        "quantity": 1000,
                        "is_return": False
                    }
                ],
                "footer": "Вау, чек передплати",
                "payments": [
                    {
                        "type": "CASH",
                        "value": 5000
                    }]
            }

        prepayment_request = requests.post(prepayment_link, headers=headers, json=payload)
        prepayment_payload = prepayment_request.json()
        prepayment_number = prepayment_payload["pre_payment_relation_id"]
        print(prepayment_payload)
        print("Order: ", prepayment_number)
        return prepayment_number

    def afterpayment_receipt(self, order_id, token):
        client_bearer = token
        afterpayment_link = f"https://api.checkbox.in.ua/api/v1/prepayment-receipts/{order_id}"
        afterpayment_uuid = str(uuid.uuid4())

        headers = {
            "X-Client-Name": "Checkbox Front",
            "X-Client-Version": "0.1a",
            "Authorization": f"Bearer {client_bearer}",
            "relation_id": order_id
        }

        payload = {
                "cashier_name": "Касир",
                "departament": "Департамент",
                "payments": [{
                    "type": "CASHLESS",
                    "card_mask":"4141***777",
                    "bank_name":"Privit",
                    "rrn":"1231002354234",
                    "value": 10000
                }],
                "footer": "Вау, чек післясплати!"
        }
        afterpayment_request = requests.post(afterpayment_link, headers=headers, json=payload)
        afterpayment_payload = afterpayment_request.json()
        print(f"____Afterpayment {order_id}______")
        print(afterpayment_payload)

#recepit = Receipt("Шалена бджілка", 3600, "CASHLESS")
#recepit.send_receipt()
#recepit.service_receipt(1000)
#recepit.service_receipt(1000)
#num_order = recepit.prepayment_receipt()
#num_order = "1707255754"
#recepit.afterpayment_receipt(num_order)