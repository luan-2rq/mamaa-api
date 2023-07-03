import datetime
import logging

import azure.functions as func

from .service import fetch_stock_data

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info(f"top_10_symbols: {fetch_stock_data()}")

    logging.info('Success! \nPython timer trigger function ran at %s', utc_timestamp)