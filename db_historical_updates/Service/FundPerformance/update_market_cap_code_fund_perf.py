from database.db_queries import get_mcap_dates, get_monthly_market_cap, get_fund_code_fund_perf, get_cap_type, \
    put_mcap_type_code_fundperf


def get_market_cap_type_code(market_cap_values):
    market_cap_type_code = None
    large_exposure = small_exposure = mid_exposure = 0
    if not market_cap_values:
        market_cap_type_code = None
    elif market_cap_values is not None:
        if len(market_cap_values) == 1:
            if market_cap_values[0][0] == 'Cash':
                market_cap_type_code = None
        else:
            for obj in market_cap_values:
                if obj[0][1] is None:
                    market_cap_values.remove(obj)
            for cap in market_cap_values:
                if cap[0][0] == 'Large' or cap[0][0] == 'Mega':
                    large_exposure += float(cap[0][1]) * 100
                if cap[0][0] == 'Small' or cap[0][0] == 'Micro':
                    small_exposure += float(cap[0][1]) * 100
                if cap[0][0] == 'Mid':
                    mid_exposure += float(cap[0][1]) * 100
            if large_exposure >= 20 and mid_exposure >= 20 and small_exposure >= 20:
                market_cap_type_code = get_cap_type("Multi Cap")
            elif ((65 > large_exposure >= 25 and 65 > mid_exposure >= 25) or
                  (65 > mid_exposure >= 25 and 65 > small_exposure >= 25) or
                  (65 > small_exposure >= 25 and 65 > large_exposure >= 25)):
                if large_exposure < mid_exposure and large_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Mid-Small Cap")
                elif mid_exposure < large_exposure and mid_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Large-Small Cap")
                elif small_exposure < large_exposure and small_exposure < mid_exposure:
                    market_cap_type_code = get_cap_type("Large-Mid Cap")
            else:
                if large_exposure > mid_exposure and large_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Large Cap")
                elif mid_exposure > large_exposure and mid_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Mid Cap")
                else:
                    market_cap_type_code = get_cap_type("Small Cap")
    market_cap = {"fund_code": fund_code, "date": str(date[0]), "market_cap_type_code": market_cap_type_code}
    return market_cap


try:
    fund_code_list = get_fund_code_fund_perf()
    for fund_code in fund_code_list:
        start_date = get_mcap_dates(fund_code)
        for date in start_date:
            monthly_cap = get_monthly_market_cap(fund_code, str(date[0]))
            market_cap = get_market_cap_type_code(monthly_cap)
            put_mcap_type_code_fundperf(market_cap)

except Exception as error:
    print("Exception raised :", error)
