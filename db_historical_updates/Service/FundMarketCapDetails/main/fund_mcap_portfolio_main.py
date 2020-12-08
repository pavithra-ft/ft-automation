from config.basic_config import fund_code
from Service.FundMarketCapDetails.service.fund_mcap_portfolio import get_mcap_from_portfolio


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_mcap_from_portfolio(fund_code_list)
