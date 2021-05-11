from config.basic_config import fund_code
from Service.Collaterals.service.collaterals import get_collateral_data

if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_collateral_data(fund_code_list)
