from config.basic_config import fund_code
from Service.FundSectorDetails.service.sector_portfolio import get_fund_sector_portfolio


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_fund_sector_portfolio(fund_code_list)
