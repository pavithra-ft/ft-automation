from database.db_queries import get_portfolio_dates, get_portfolio_details, put_allocations


def get_allocation_from_portfolio(portfolio_values):
    allocation_values = {'cash_allocation': None}
    allocation_sum = 0
    for security in portfolio_values:
        if security['security_isin'] != 'CASH':
            allocation_sum += float(security['exposure'])
            if allocation_values.__contains__('equity_allocation'):
                allocation_values['equity_allocation'] += float(security['exposure'])
            else:
                allocation_values.update({'equity_allocation': round(float(security['exposure']), 4)})
        else:
            allocation_values.update({'cash_allocation': round(float(security['exposure']), 4)})
    return allocation_values


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        portfolio_date_list = get_portfolio_dates(fund_code)
        for reporting_date in portfolio_date_list:
            portfolio_values = get_portfolio_details(fund_code, reporting_date)
            allocation_values = get_allocation_from_portfolio(portfolio_values)
            put_allocations(fund_code, allocation_values, reporting_date)

except Exception as error:
    print("Exception raised :", error)
