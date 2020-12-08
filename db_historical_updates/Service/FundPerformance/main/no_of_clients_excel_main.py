from config.basic_config import fund_code
from Service.FundPerformance.service.no_of_clients_excel import get_no_of_clients


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_no_of_clients(fund_code_list)
