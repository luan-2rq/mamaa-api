import logging
import json
import azure.functions as func
from .service import get_top_10_stocks_data


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    top_10_stocks_data = get_top_10_stocks_data()

    logging.info(f"top_10_stocks_data: {top_10_stocks_data}")
    return func.HttpResponse(headers={"Access-Control-Allow-Origin": "*"},body=top_10_stocks_data, mimetype="application/json", status_code=200)
    