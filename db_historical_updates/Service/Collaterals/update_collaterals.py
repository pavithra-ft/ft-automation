import datetime

from model.FundTablesModel import Collaterals
from database.db_queries import get_fund_dates, get_collateral_code, get_collateral_view_code, get_fund_short_code, \
    get_default_visibility_code, get_collateral_template_code, is_collaterals_exist, put_collaterals_data


def get_collateral_data(fund_code, reporting_date):
    collateral_data = Collaterals()
    collateral_data.set_collateral_code(get_collateral_code())
    collateral_data.set_view_code(get_collateral_view_code())
    collateral_data.set_collateral_type_code('FACTSHEET')
    collateral_data.set_entity_type('FUND')
    collateral_data.set_entity_code(fund_code)
    collateral_data.set_collateral_title(get_fund_short_code(fund_code) + ' Fintuple Factsheet')
    collateral_data.set_visibility_code(get_default_visibility_code(fund_code))
    collateral_data.set_template_code(get_collateral_template_code(fund_code, reporting_date))
    collateral_data.set_collateral_date(reporting_date + datetime.timedelta(days=1))
    collateral_data.set_collateral_status('PUBLISHED')
    collateral_data.set_reporting_date(reporting_date)
    collateral_data.set_effective_start_date(reporting_date + datetime.timedelta(days=1))
    collateral_data.set_is_premium('1')
    collateral_data.set_is_published('1')
    collateral_data.set_is_data_changed('1')
    collateral_data.set_published_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    collateral_data.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    collateral_data.set_created_by('ft-automation')
    return collateral_data


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        fund_dates = get_fund_dates(fund_code)
        for reporting_date in fund_dates:
            if not is_collaterals_exist(fund_code, reporting_date):
                collateral_data = get_collateral_data(fund_code, reporting_date)
                put_collaterals_data(collateral_data)
                print(collateral_data)

except Exception as error:
    print("Exception raised :", error)
