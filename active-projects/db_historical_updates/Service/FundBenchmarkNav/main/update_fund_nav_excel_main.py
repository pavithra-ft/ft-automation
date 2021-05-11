from config.basic_config import fund_code
from Service.FundBenchmarkNav.service.update_fund_nav_excel import get_fund_nav


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_fund_nav(fund_code_list)
