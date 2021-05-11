from config.basic_config import fund_code
from Service.FundPerformance.service.mcap_code_fundperf import get_market_cap_type_code


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_market_cap_type_code(fund_code_list)
