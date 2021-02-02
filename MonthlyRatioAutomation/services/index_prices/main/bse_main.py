from services.index_prices.service.bse_index_prices import get_bse_index

if __name__ == "__main__":
    historical_url = ['https://api.bseindia.com/BseIndiaAPI/api/IndexArchDaily']
    get_bse_index(historical_url)
