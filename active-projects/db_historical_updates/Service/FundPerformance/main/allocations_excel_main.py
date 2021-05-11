from config.basic_config import fund_code
from Service.FundPerformance.service.allocations_excel import get_allocations


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_allocations(fund_code_list)
