from Service.FundMarketCapDetails.service.market_cap_excel import get_market_cap
from config.basic_config import fund_code

if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_market_cap(fund_code_list)
