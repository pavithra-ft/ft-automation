from datetime import datetime

from model.FundTablesModel import FundMarketCapDetails
from database.db_queries import get_portfolio_dates, get_portfolio_details, get_mcap_for_security, put_market_cap_data


def get_mcap_from_portfolio(portfolio_values):
    mcap_type_code = None
    mcap_values = {}
    cap_sum = 0
    for value in portfolio_values:
        type_code = get_mcap_for_security(value['security_isin'])
        if type_code is not None:
            mcap_type_code = type_code.capitalize()
        cap_sum += value['exposure']
        if mcap_values.__contains__(mcap_type_code):
            mcap_values[mcap_type_code] += value['exposure']
        else:
            mcap_values.update({mcap_type_code: value['exposure']})
    return mcap_values


try:
    fund_code_list = ['40274836']
    for fund_code in fund_code_list:
        portfolio_date_list = get_portfolio_dates(fund_code)
        for reporting_date in portfolio_date_list:
            portfolio_values = get_portfolio_details(fund_code, reporting_date)
            mcap_values = get_mcap_from_portfolio(portfolio_values)
            market_cap_list = []
            for market_cap, exposure in mcap_values.items():
                mcap_body = FundMarketCapDetails()
                mcap_body.set_fund_code(fund_code)
                mcap_body.set_type_market_cap(market_cap)
                mcap_body.set_exposure(round(exposure, 4))
                mcap_body.set_start_date(reporting_date.replace(day=1))
                mcap_body.set_end_date(reporting_date)
                mcap_body.set_created_ts(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                mcap_body.set_action_by('ft-automation')
                market_cap_list.append(mcap_body)
            put_market_cap_data(market_cap_list)

except Exception as error:
    print("Exception raised :", error)