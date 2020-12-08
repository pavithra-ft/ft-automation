from config.basic_config import fund_code
from Service.FundRatios.service.fund_ratios import get_fund_ratios


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_fund_ratios(fund_code_list)
