from database.db_actions import get_benchmark_index, get_index_price_as_on_date, get_benchmark_nav, \
    get_alt_benchmark_index, get_alt_benchmark_nav, get_cap_type
from service.DateCalculation import get_effective_start_end_date, get_1m_date


def calc_benchmark_nav(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    previous_1m_date = get_1m_date(fund_info.get_reporting_date())
    benchmark_index = get_benchmark_index(fund_info.get_fund_code())
    index_price = get_index_price_as_on_date(effective_end_date, benchmark_index)
    prev_index_price = get_index_price_as_on_date(previous_1m_date, benchmark_index)
    previous_benchmark_nav = get_benchmark_nav(fund_info.get_fund_code(), previous_1m_date)
    benchmark_return = (float(index_price) / float(prev_index_price)) - 1
    benchmark_nav = round((float(previous_benchmark_nav) * (1 + benchmark_return)), 6)
    return benchmark_nav


def calc_alt_benchmark_nav(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    previous_1m_date = get_1m_date(fund_info.get_reporting_date())
    alt_benchmark_index = get_alt_benchmark_index(fund_info.get_fund_code())
    alt_index_price = get_index_price_as_on_date(effective_end_date, alt_benchmark_index)
    alt_prev_index_price = get_index_price_as_on_date(previous_1m_date, alt_benchmark_index)
    previous_alt_benchmark_nav = get_alt_benchmark_nav(fund_info.get_fund_code(), previous_1m_date)
    alt_benchmark_return = (float(alt_index_price) / float(alt_prev_index_price)) - 1
    alt_benchmark_nav = round((float(previous_alt_benchmark_nav) * (1 + alt_benchmark_return)), 6)
    return alt_benchmark_nav


def get_market_cap_type_code(market_cap_values):
    market_cap_type_code = None
    mcap_check = not market_cap_values
    if mcap_check is True:
        market_cap_type_code = None
    elif mcap_check is False:
        if len(market_cap_values) == 1:
            if market_cap_values.__contains__('Cash'):
                del market_cap_values['Cash']
            market_cap_type_code = None
        else:
            for key in market_cap_values:
                market_cap_values[key] *= 100
            mega_value = market_cap_values['Mega'] if 'Mega' in market_cap_values.keys() else 0
            large_value = market_cap_values['Large'] if 'Large' in market_cap_values.keys() else 0
            small_value = market_cap_values['Small'] if 'Small' in market_cap_values.keys() else 0
            micro_value = market_cap_values['Micro'] if 'Micro' in market_cap_values.keys() else 0
            market_cap_values.update({"Large": mega_value + large_value})
            market_cap_values.update({"Small": small_value + micro_value})
            keys_to_remove = ["Cash", "Micro", "Mega", "ETF"]
            for key in keys_to_remove:
                if key in market_cap_values.keys():
                    del market_cap_values[key]
            large_exposure = market_cap_values['Large'] if 'Large' in market_cap_values.keys() else 0
            small_exposure = market_cap_values['Small'] if 'Small' in market_cap_values.keys() else 0
            mid_exposure = market_cap_values['Mid'] if 'Mid' in market_cap_values.keys() else 0
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
    print(market_cap_type_code)
    return market_cap_type_code
