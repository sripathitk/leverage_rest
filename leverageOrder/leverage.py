from flask import Flask
from flask import request
from flask_classful import FlaskView,route
import logging
from alice_blue import *
import json
from datetime import datetime
import os
log_file = str(datetime.now().strftime('lev_%m_%d_%Y_%I_%M_%S')) + '.log'
logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler(log_file),
                              logging.StreamHandler()],
                    format='[%(asctime)s.%(msecs)03d] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )
from login.generate_alice_blue_token import generate_alice_blue_token
app = Flask(__name__)


class LeverageView(FlaskView):

    def __init__(self):
        with open(os.path.join(os.getcwd(), '../config/UserConfig.json')) as f:
            self.users_d = json.load(f)

         # BNF parameters
        self.bnf_enabled = self.users_d['users']['suma']['lev_bnf']['enabled']
        self.bnf_trading_symbol = self.users_d['users']['suma']['lev_bnf']['trading_symbol']
        self.bnf_leverage_quantity = int(self.users_d['users']['suma']['lev_bnf']['leverageQuantity'])
        # NF parameters
        self.nf_enabled = self.users_d['users']['suma']['lev_nf']['enabled']
        self.nf_trading_symbol = self.users_d['users']['suma']['lev_nf']['trading_symbol']
        self.nf_non_trading_symbol = self.users_d['users']['suma']['lev_nf']['non_trading_symbol']
        self.nf_leverage_quantity = int(self.users_d['users']['suma']['lev_nf']['leverageQuantity'])

        # code block to figure out whether access token is available or not.
        gat = generate_alice_blue_token()
        self.alice=gat.generate_access_token()

    @route("/placeLev", methods=['POST'])
    def placelev(self):
        logging.info("leverage order message received for user ")

        try:
            req_data = request.get_json()
            if req_data:
                instrument_token = req_data['instrument_token']
                exchange = req_data['exchange']
                trading_symbol = req_data['trading_symbol']
                if self.nf_non_trading_symbol not in trading_symbol:
                    lev_quantity = self.nf_leverage_quantity
                    if self.nf_enabled != "True":
                        logging.info("NF/Smoking in black is not enabled for user hence ignoring the order")
                        return True
                elif self.nf_non_trading_symbol in trading_symbol:
                    lev_quantity = self.bnf_leverage_quantity
                    if self.bnf_enabled != "True":
                        logging.info("BNF/Penguin cave is not enabled for user hence ignoring the order")
                        return True

                lev_order_type_s = req_data['lev_order_type']
                if lev_order_type_s == 'SELL':
                    lev_order_type = TransactionType.Sell
                elif lev_order_type_s == 'BUY':
                    lev_order_type = TransactionType.Buy

                instrument = self.alice.get_instrument_by_token(exchange, instrument_token)
                logging.info('placing leverage order  for {} with quantity {} and type {}'.
                             format(trading_symbol, lev_quantity, lev_order_type.value))
                response = self.alice.place_order(transaction_type=lev_order_type, instrument=instrument,
                                                  quantity=lev_quantity,
                                                  order_type=OrderType.Market,
                                                  product_type=ProductType.Intraday,
                                                  price=0.0,
                                                  trigger_price=0.0,
                                                  stop_loss=None,
                                                  square_off=None,
                                                  trailing_sl=None,
                                                  is_amo=False)
                logging.info('leverage order response from broker is {}'.format(response))
                if response['status'] == 'success':
                    logging.info(' Leverage order placed successfully for {} with quantity {}'
                                 .format(trading_symbol, lev_quantity))
                    return response
        except Exception as e:
            logging.error("Exception in executing Penguin Cave and Smoke in Black {}".format(e))
        return "error occurred"


LeverageView.register(app, route_base='/')

if __name__ == '__main__':
    app.run(debug=True)
