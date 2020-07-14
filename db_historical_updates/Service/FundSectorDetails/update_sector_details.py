from datetime import datetime
from model.FundTablesModel import FundSector
from database.db_queries import get_portfolio_dates, get_portfolio_details, get_sector_from_portfolio, put_fund_sector


def get_fund_sector_from_portfolio(portfolio_values):
    sector_response = None
    sector_breakdown = []
    for security_data in portfolio_values:
        sector_body = {"isin": security_data["security_isin"], "sector": None, "exposure": security_data["exposure"]}
        if security_data["security_isin"]:
            sec_isin = security_data["security_isin"]
            sector_response = get_sector_from_portfolio(sec_isin)
        sector_body["sector"] = sector_response[0][0]
        sector_breakdown.append(sector_body)
    sector_breakdown_result = {}
    sector_sum = 0
    for i in sector_breakdown:
        sector_sum += i['exposure']
        if sector_breakdown_result.__contains__(i["sector"]):
            sector_breakdown_result[i["sector"]] += i["exposure"]
        else:
            sector_breakdown_result.update({i["sector"]: i["exposure"]})
    for sec, exp in sector_breakdown_result.items():
        if exp == 0:
            sector_breakdown_result[sec] = None
        else:
            sector_breakdown_result[sec] = round(exp, 4)
    return sector_breakdown_result


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        portfolio_date_list = get_portfolio_dates(fund_code)
        for reporting_date in portfolio_date_list:
            portfolio_values = get_portfolio_details(fund_code, reporting_date)
            sector_values = get_fund_sector_from_portfolio(portfolio_values)
            sector_data_list = []
            for sector_name, exposure in sector_values.items():
                sectorBody = FundSector()
                sectorBody.set_fund_code(fund_code)
                sectorBody.set_sector_type_name(sector_name)
                sectorBody.set_exposure(exposure)
                sectorBody.set_start_date(reporting_date.replace(day=1))
                sectorBody.set_end_date(reporting_date)
                sectorBody.set_created_ts(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sectorBody.set_action_by('ft-automation')
                sector_data_list.append(sectorBody)
            put_fund_sector(sector_data_list)

except Exception as error:
    print("Exception raised :", error)
