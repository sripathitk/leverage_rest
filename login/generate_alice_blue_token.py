import logging
from alice_blue import *
import json
import datetime
import os

logging.basicConfig(level=logging.INFO)


class generate_alice_blue_token:
    users_d = {}

    def __init__(self):
        pass

    def load_users_data(self):
        with open(os.path.join(os.getcwd(), '../config/UserConfig.json')) as f:
            self.users_d = json.load(f)
        return self.users_d

    def generate_access_token(self):
        # read data from csv.
        self.load_users_data()
        username = self.users_d['users']['suma']['aliceblue']['username']
        password = self.users_d['users']['suma']['aliceblue']['password']
        twofa = self.users_d['users']['suma']['aliceblue']['twoFA']
        api_secret = self.users_d['users']['suma']['aliceblue']['api_secret']
        access_token = self.users_d['users']['suma']['aliceblue']['access_token']
        logging.info('access token is {}'.format(access_token))
        modified_date = self.users_d['users']['suma']['aliceblue']['modified_date']

        # code block to figure out whether access token is available or not.
        try:
            if modified_date != datetime.date.today().__str__():
                access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=twofa,
                                                                    api_secret=api_secret)
                logging.info("Generating a new access token {} and modifying generation date to {}"
                             .format(access_token, datetime.date.today()))
            logging.debug("checking whether access token is valid")
            alice = AliceBlue(username=username, password=password, access_token=access_token)
        except Exception as e:
            logging.error(" current token {} is invalid and and exception "
                          "occurred in generating a new one ".format(access_token, e))
            logging.debug("Invalid access token , generating a new access token")
            access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=twofa,
                                                                api_secret=api_secret)
            alice = AliceBlue(username=username, password=password, access_token=access_token)
            logging.info("Stored access token is invalid , generated a new access token {} ".format(access_token))

        balance = alice.get_balance()
        if balance['status'] == 'success':
            modified_date = datetime.date.today().__str__()
            logging.info("Access token generation and verification  - success ")

        self.users_d['users']['suma']['aliceblue']['access_token'] = access_token
        self.users_d['users']['suma']['aliceblue']['modified_date'] = modified_date
        logging.info('access token  & modified_date values are {} & {}'.format(access_token, modified_date))
        with open(os.path.join(os.getcwd(), '../config/UserConfig.json'), 'w') as f:
            json.dump(self.users_d, f)
        return alice


# ---------------manual generation-------------------
# from alice_blue import *
# access_token = AliceBlue.login_and_get_access_token(username="AB068856", password="F@rmosa4", twoFA="a",
#                                                     api_secret="YMEJW3O3I4WE2508CYD6NPUL8WWK71AG6DYWHRI1BXZLVD1U0ZHP0XAI22KAHE6R")
# print(access_token)

# gat = generate_alice_blue_token()
# gat.generate_access_token()
