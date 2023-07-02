import logging
import json
import azure.functions as func
from .service import get_current_stock_price


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    get_current_stock_price()

    return func.HttpResponse(body=json.dumps({}), mimetype="application/json", status_code=200)
    