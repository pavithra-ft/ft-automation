from config.basic_config import fund_code
from Service.FundPerformance.service.fund_performance import get_fund_performance


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_fund_performance(fund_code_list)
