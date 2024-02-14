import logging

import requests
import datetime
import uuid
import pytz


#getter setter license key
#getter setter pincode cashier
#bearer
#taxes

logging.basicConfig(level=logging.INFO, filename="checkbox_log.log",filemode="a")


class Connection_mod:

    @staticmethod
    def login(license_key, pin):
        pin_login_link = "https://api.checkbox.ua/api/v1/cashier/signinPinCode"
        client_name = 'Checkbox Front 0.1'
        client_version = "0.1a"
        headers = {
            "X-License-Key": license_key,
            "X-Client-Version": client_version,
            "X-Client-Name": client_name
        }

        data = {
          "pin_code": pin
        }

        login_request = requests.post(pin_login_link, json=data, headers=headers)

        print("Status Code", login_request.status_code)
        #print("JSON Response ", login_request.json())
        request_return = login_request.json()

        bearer = request_return['access_token']
        print(bearer)
        return bearer

    def __init__(self,license_key, pin, bearer, client_name = 'Checkbox Front', client_version = "0.1a"):
        self.license_key = license_key
        self.pin_code = pin
        self.bearer = bearer
        self.client_name = client_name
        self.client_version = client_version
        self.shift_uuid = ""
        self.shift_status = ""

    def ping_tax_service(self, license_key):

        ping_tax_link = "https://api.checkbox.ua/api/v1/cash-registers/ping-tax-service"
        headers = {
            "X-Client-Name": self.client_name,
            "X-Client-Version": self.client_version,
            "X-License-Key": license_key,
            "Authorization": f"Bearer {self.bearer}"
        }

        result = requests.post(ping_tax_link, headers=headers).json()
        return result

    def is_last_shift_opened(self,token):

        #get_shifts_link = "https://api.checkbox.ua/api/v1/shifts"
        get_cashier_shift_link = "https://api.checkbox.ua/api/v1/cashier/shift"
        headers = {
            "X-Client-Name": self.client_name,
            "X-Client-Version": self.client_version,
            "Authorization": f"Bearer {self.bearer}"
        }

        result = requests.get(get_cashier_shift_link,headers=headers).json()
        if not result:
            logging.info(f"{datetime.datetime.now()} Зміна закрита \n")
            return False
        else:
            logging.info(f"{datetime.datetime.now()} Зміна у статусі {result['status']} \n")
            return True


    def check_shift(self):

        check_shift_link = "https://api.checkbox.ua/api/v1/cashier/shift"

        headers = {
            "X-License-Key": self.license_key,  # TEST462432,
            "X-Client-Name": self.client_name,
            "X-Client-Version": self.client_version,
            "Authorization": f"Bearer {self.bearer}"
        }

        return requests.get(check_shift_link, headers=headers).json()

    def open_shift(self):
        shift_open_link = "https://api.checkbox.ua/api/v1/shifts"
        self.shift_uuid = str(uuid.uuid4())
        print(f"********\n{self.shift_uuid}\n********")

        headers = {
            "X-License-Key": self.license_key,#"test1ea7f100df623647e5657a20", #TEST462432,
            "X-Client-Name": self.client_name,
            "X-Client-Version": self.client_version,
            "Authorization": f"Bearer {self.bearer}"
        }

        body = {
            "id": self.shift_uuid,
            #"fiscal_date":datetime.datetime.now().isoformat()
        }

        shift_open_request = requests.post(shift_open_link, json=body, headers=headers)
        return_request = shift_open_request.json()

        print(return_request["status"])

        return return_request


    def close_shift(self):

        shift_close_link = "https://api.checkbox.ua/api/v1/shifts/close"

        headers = {
            "X-License-Key": self.license_key,#"test1ea7f100df623647e5657a20",  # TEST462432,
            "X-Client-Name": self.client_name,
            "X-Client-Version": self.client_version,
            "Authorization": f"Bearer {self.bearer}"
        }

        body = {
            "skip_client_name_check": True
        }

        shift_close_request = requests.post(shift_close_link, json=body, headers=headers)
        return_request = shift_close_request.json()

        if return_request:
            #print(return_request["status"])
            return return_request
        else:
            raise Exception(f"Shift is already closed")
        # if self.check_shift(bearer)["status"] == 'OPENED':
        #     shift_close_request = requests.post(shift_close_link, json=body, headers=headers)
        #
        #     return_request = shift_close_request.json()
        #
        #     return return_request
        # else:
        #     #raise Exception(f"Shift is closed")
        #     print(f"Shift is already closed")
