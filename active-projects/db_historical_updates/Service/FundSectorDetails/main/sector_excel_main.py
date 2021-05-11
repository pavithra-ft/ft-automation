from config.basic_config import fund_code
from Service.FundSectorDetails.service.sector_excel import get_fund_sector_details


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_fund_sector_details(fund_code_list)
