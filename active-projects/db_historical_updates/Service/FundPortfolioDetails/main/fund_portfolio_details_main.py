from config.basic_config import fund_code
from Service.FundPortfolioDetails.service.fund_portfolio_details import get_fund_portfolio


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_fund_portfolio(fund_code_list)
