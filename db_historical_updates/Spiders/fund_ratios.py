import time
import math
import MySQLdb
import schedule
import datetime
import statistics

from envparse import env
from scipy import optimize
from Spiders.db_actions import get_fund_nav, get_benchmark_perf_1m, get_pe_ratio, get_fund_ratio_mcap, \
    get_nav_start_date, get_all_fund_return, get_risk_free_rate, get_fund_codes, is_fund_ratio_exist, \
    put_fund_ratio_data, get_fund_portfolio


def calc_top5_pe_ratio(top5_holdings, iq_database):
    pe_ratio_list = get_pe_ratio(top5_holdings, iq_database)
    pe_ratio_values = []
    exposure_values = []
    for security in top5_holdings:
        for pe_ratio in pe_ratio_list:
            if security['security_isin'] == pe_ratio['security_isin']:
                pe_ratio_values.append(pe_ratio['pe_ratio'])
    for exposure in top5_holdings:
        exposure_values.append(exposure['exposure'])
    calc_pe_ratio = []
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        calc_pe_ratio.append(exp * ratio)
    top5_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top5_pe_ratio


def calc_top10_pe_ratio(top10_holdings, iq_database):
    pe_ratio_list = get_pe_ratio(top10_holdings, iq_database)
    pe_ratio_values = []
    exposure_values = []
    for security in top10_holdings:
        for pe_ratio in pe_ratio_list:
            if security['security_isin'] == pe_ratio['security_isin']:
                pe_ratio_values.append(pe_ratio['pe_ratio'])
    for exposure in top10_holdings:
        exposure_values.append(exposure['exposure'])
    calc_pe_ratio = []
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        calc_pe_ratio.append(exp * ratio)
    top10_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top10_pe_ratio


def calc_top5_market_cap(top5_holdings, iq_database):
    mcap_list = get_fund_ratio_mcap(top5_holdings, iq_database)
    mcap_values = []
    exposure_values = []
    for security in top5_holdings:
        for market_cap in mcap_list:
            if security['security_isin'] == market_cap['security_isin']:
                mcap_values.append(market_cap['market_cap'])
    for exposure in top5_holdings:
        exposure_values.append(exposure['exposure'])
    calc_mcap = []
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    for exp, mcap in zip(exposure_values, mcap_values):
        calc_mcap.append(exp * mcap)
    top5_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return top5_market_cap


def calc_top10_market_cap(top10_holdings, iq_database):
    mcap_list = get_fund_ratio_mcap(top10_holdings, iq_database)
    mcap_values = []
    exposure_values = []
    for security in top10_holdings:
        for market_cap in mcap_list:
            if security['security_isin'] == market_cap['security_isin']:
                mcap_values.append(market_cap['market_cap'])
    for exposure in top10_holdings:
        exposure_values.append(exposure['exposure'])
    calc_mcap = []
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    for exp, mcap in zip(exposure_values, mcap_values):
        calc_mcap.append(exp * mcap)
    top10_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return top10_market_cap


def get_negative_excess_return(fund_return_list, risk_free):
    negative_excess_return_list = []
    for return_value in fund_return_list:
        if (return_value - risk_free) > 0:
            negative_excess_return_list.append(0)
        else:
            negative_excess_return_list.append((return_value - risk_free) ** 2)
    negative_excess_returns_risk_free = round(sum(negative_excess_return_list), 4)
    return negative_excess_returns_risk_free


def xnpv(rate, annualized_values):
    return sum([av / (1 + rate) ** ((t - annualized_values[0][0]).days / 365.0) for (t, av) in annualized_values])


def get_annualized_return(fund_code, reporting_date, fund_nav, app_database):
    nav_start_date = get_nav_start_date(fund_code, app_database)
    start_date_nav = -1
    start_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(str(reporting_date), "%Y-%m-%d").date()
    annualized_values = [(datetime.date(start_date.year, start_date.month, start_date.day), start_date_nav),
                         (datetime.date(end_date.year, end_date.month, end_date.day), fund_nav)]
    annualized_return = optimize.newton(lambda r: xnpv(r, annualized_values), 0.1)
    return annualized_return


def get_fund_ratios(fund_code, reporting_date, iq_database, app_database):
    top5_pe_ratio = top10_pe_ratio = top5_market_cap = top10_market_cap = None
    fund_nav = get_fund_nav(fund_code, reporting_date, iq_database)[0][0]
    portfolio_values = get_fund_portfolio(fund_code, reporting_date, iq_database)
    benchmark_perf_1m = get_benchmark_perf_1m(fund_code, reporting_date, iq_database)
    fund_return_list = get_all_fund_return(fund_code, iq_database)
    portfolio_sum = 0
    if portfolio_values is not None:
        for value in portfolio_values:
            if 'exposure' in value:
                portfolio_sum += value['exposure']
    portfolio_sum = round(portfolio_sum * 100)
    if portfolio_sum > 0:
        sorted_exposure = sorted(portfolio_values, key=lambda i: i['exposure'], reverse=True)
        sorted_pf_values = [i for i in sorted_exposure if not (i['security_isin'] == 'CASH')]
        top5_holdings = sorted_pf_values[0:5]
        top10_holdings = sorted_pf_values[0:10]
        pe5_ratio = calc_top5_pe_ratio(top5_holdings, iq_database)
        top5_pe_ratio = None if (pe5_ratio == 0) else pe5_ratio
        pe10_ratio = calc_top10_pe_ratio(top10_holdings, iq_database)
        top10_pe_ratio = None if (pe10_ratio == 0) else pe10_ratio
        market5_cap = calc_top5_market_cap(top5_holdings, iq_database)
        top5_market_cap = None if (market5_cap == 0) else market5_cap
        market10_cap = calc_top10_market_cap(top10_holdings, iq_database)
        top10_market_cap = None if (market10_cap == 0) else market10_cap
    standard_deviation = round(statistics.stdev(fund_return_list), 4)
    median = round(statistics.median(fund_return_list), 4)
    risk_free = get_risk_free_rate(iq_database)
    negative_excess_returns_risk_free = get_negative_excess_return(fund_return_list, risk_free)
    sigma = round(math.sqrt(negative_excess_returns_risk_free / 12), 4)
    annualized_return = get_annualized_return(fund_code, reporting_date, fund_nav, app_database)
    sortino_ratio = round(((annualized_return - risk_free) / sigma), 4)
    fund_alpha = round(((fund_return_list[-1] - benchmark_perf_1m) * 100), 4)
    updated_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_by = "ft-automation"
    fund_ratio_data = {"fund_code": fund_code, "reporting_date": reporting_date, "top5_pe_ratio": top5_pe_ratio,
                       "top10_pe_ratio": top10_pe_ratio, "top5_market_cap": top5_market_cap,
                       "top10_market_cap": top10_market_cap, "standard_deviation": standard_deviation,
                       "median": median, "sigma": sigma, "sortino_ratio": sortino_ratio,
                       "negative_excess_returns_risk_free": negative_excess_returns_risk_free,
                       "fund_alpha": fund_alpha, "updated_ts": updated_ts, "updated_by": updated_by}
    print(fund_ratio_data)
    return fund_ratio_data


def fund_ratios():
    db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    # db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_db, app_db = 'iq', 'app'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)

    fund_code_list = get_fund_codes(iq_database)
    for fund_detail in fund_code_list:
        if not is_fund_ratio_exist(fund_detail[0], fund_detail[1], iq_database):
            fund_ratio_data = get_fund_ratios(fund_detail[0], fund_detail[1], iq_database, app_database)
            put_fund_ratio_data(fund_ratio_data, iq_database)

    iq_database.commit()
    print("Commit success")
    iq_database.close()
    app_database.close()


schedule.every(3).hour.do(fund_ratios)
while True:
    schedule.run_pending()
    time.sleep(1)
