from flask import Flask,render_template
from flask import request

import logging
from alice_blue import *
import json
import datetime
import os

logging.basicConfig(level=logging.DEBUG)

app= Flask(__name__)

@app.route("/placeLev",methods=['POST'])
def placelev():

       with open(os.path.join(os.getcwd(), 'config/UserConfig.json')) as f:
              users_d = json.load(f)

       username = users_d['users']['suma']['aliceblue']['username']
       password = users_d['users']['suma']['aliceblue']['password']
       twofa = users_d['users']['suma']['aliceblue']['twoFA']
       api_secret = users_d['users']['suma']['aliceblue']['api_secret']
       access_token = users_d['users']['suma']['aliceblue']['access_token']
       logging.info('access token is {}'.format(access_token))
       modified_date = users_d['users']['suma']['aliceblue']['modified_date']
       # BNF parameters
       bnf_enabled = users_d['users']['suma']['lev_bnf']['enabled']
       bnf_trading_symbol = users_d['users']['suma']['lev_bnf']['trading_symbol']
       bnf_lot_size = int(users_d['users']['suma']['lev_bnf']['lot_size'])
       bnf_ref_trade_size = int(users_d['users']['suma']['lev_bnf']['ref_trade_size'])
       bnf_fno_exchange = users_d['users']['suma']['lev_bnf']['fno_exchange']
       bnf_ce_position_type = users_d['users']['suma']['lev_bnf']['cePositionType']
       bnf_pe_position_type = users_d['users']['suma']['lev_bnf']['pePositionType']
       bnf_leverage_quantity = int(users_d['users']['suma']['lev_bnf']['leverageQuantity'])
       bnf_lev_order_type = users_d['users']['suma']['lev_bnf']['lev_order_type']
       bnf_exchange = users_d['users']['suma']['lev_bnf']['exchange']
       bnf_slm_order_type = users_d['users']['suma']['lev_bnf']['slmOrderType']
       bnf_ref_pos_quantity = users_d['users']['suma']['lev_bnf']['ref_pos_quantity']
       # NF parameters
       nf_enabled = users_d['users']['suma']['lev_nf']['enabled']
       nf_trading_symbol = users_d['users']['suma']['lev_nf']['trading_symbol']
       nf_non_trading_symbol = users_d['users']['suma']['lev_nf']['non_trading_symbol']
       nf_lot_size = int(users_d['users']['suma']['lev_nf']['lot_size'])
       nf_ref_trade_size = int(users_d['users']['suma']['lev_nf']['ref_trade_size'])
       nf_fno_exchange = users_d['users']['suma']['lev_nf']['fno_exchange']
       nf_ce_position_type = users_d['users']['suma']['lev_nf']['cePositionType']
       nf_pe_position_type = users_d['users']['suma']['lev_nf']['pePositionType']
       nf_leverage_quantity = int(users_d['users']['suma']['lev_nf']['leverageQuantity'])
       nf_lev_order_type = users_d['users']['suma']['lev_nf']['lev_order_type']
       nf_exchange = users_d['users']['suma']['lev_nf']['exchange']
       nf_slm_order_type = users_d['users']['suma']['lev_nf']['slmOrderType']
       nf_ref_pos_quantity = users_d['users']['suma']['lev_nf']['ref_pos_quantity']
       # code block to figure out whether access token is available or not.

       try:
              if modified_date != datetime.date.today().__str__():
                     access_token = AliceBlue.login_and_get_access_token(username=username, password=password,
                                                                         twoFA=twofa,
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
       return alice.get_order_history()
       # try:
       #        balance = alice.get_balance()
       #        if balance['status'] == 'success':
       #               modified_date = datetime.date.today().__str__()
       #               logging.info("Access token generation and verification  - success ")
       #               users_d['users']['suma']['aliceblue']['access_token'] = access_token
       #               users_d['users']['suma']['aliceblue']['modified_date'] = modified_date
       #               logging.info('access token  & modified_date values are {} & {}'.format(access_token, modified_date))
       #               print(access_token)
       #               with open(os.path.join(os.getcwd(), 'config/UserConfig.json'), 'w') as f:
       #                      json.dump(users_d, f)
       #        req_data = request.get_json()
       #        if(req_data):
       #               instrument_token=  req_data['instrument_token'];
       #               exchange = req_data['exchange'];
       #               trading_symbol = req_data['trading_symbol'];
       #               lev_quantity = int(req_data['lev_quantity']);
       #               lev_order_type_s = req_data['lev_order_type'];
       #               if lev_order_type_s== 'SELL':
       #                      lev_order_type=TransactionType.Sell
       #               elif lev_order_type_s== 'BUY':
       #                      lev_order_type = TransactionType.Buy
       #               logging.info('placing leverage order  for {} with quantity {}'
       #                            .format(trading_symbol, lev_quantity))
       #               instrument = alice.get_instrument_by_token(exchange, instrument_token)
       #               logging.info('Leverage order placed for {} with quantity {} and type {}'.
       #                            format(trading_symbol, lev_quantity, lev_order_type.value))
       #               response = alice.place_order(transaction_type=lev_order_type, instrument=instrument,
       #                                                 quantity=lev_quantity,
       #                                                 order_type=OrderType.Market,
       #                                                 product_type=ProductType.Intraday,
       #                                                 price=0.0,
       #                                                 trigger_price=0.0,
       #                                                 stop_loss=None,
       #                                                 square_off=None,
       #                                                 trailing_sl=None,
       #                                                 is_amo=False)
       #               logging.info('leverage order response from broker is {}'.format(response))
       #               if response['status'] == 'success':
       #                      logging.info(' Leverage order placed successfully for {} with quantity {}'
       #                                   .format(trading_symbol, lev_quantity))
       #                      return response
       # except Exception as e:
       #        logging.error("Exception in executing Penguin Cave and Smoke in Black {}".format(e))
       # return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)

