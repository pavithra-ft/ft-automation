from services.index_prices.service.nse_index_prices import get_nse_index

if __name__ == "__main__":
    historical_url = ['https://www1.nseindia.com/products/dynaContent/equities/indices']
    get_nse_index(historical_url)
