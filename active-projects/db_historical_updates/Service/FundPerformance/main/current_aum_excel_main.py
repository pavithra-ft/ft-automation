from config.basic_config import fund_code
from Service.FundPerformance.service.current_aum_excel import get_current_aum


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_current_aum(fund_code_list)
