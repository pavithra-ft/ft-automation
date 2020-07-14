import math
import datetime
import statistics
import database.db_queries as query
from scipy import optimize
from model.FundTablesModel import FundRatios


def calc_full_pe_ratio(sorted_exposure):
    pe_ratio_list = query.get_pe_ratio(sorted_exposure)
    pe_ratio_values = [float(pe_ratio['pe_ratio']) for security in sorted_exposure for pe_ratio in pe_ratio_list
                       if security[0] == pe_ratio['security_isin']]
    exposure_values = [float(exposure[1]) for exposure in sorted_exposure]
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    calc_pe_ratio = [float(exp * ratio) for exp, ratio in zip(exposure_values, pe_ratio_values)]
    full_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return full_pe_ratio


def calc_top5_pe_ratio(top5_holdings):
    pe_ratio_list = query.get_pe_ratio(top5_holdings)
    pe_ratio_values = [float(pe_ratio['pe_ratio']) for security in top5_holdings for pe_ratio in pe_ratio_list
                       if security[0] == pe_ratio['security_isin']]
    exposure_values = [float(exposure[1]) for exposure in top5_holdings]
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    calc_pe_ratio = [float(exp * ratio) for exp, ratio in zip(exposure_values, pe_ratio_values)]
    top5_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top5_pe_ratio


def calc_top10_pe_ratio(top10_holdings):
    pe_ratio_list = query.get_pe_ratio(top10_holdings)
    pe_ratio_values = [float(pe_ratio['pe_ratio']) for security in top10_holdings for pe_ratio in pe_ratio_list
                       if security[0] == pe_ratio['security_isin']]
    exposure_values = [float(exposure[1]) for exposure in top10_holdings]
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    calc_pe_ratio = [float(exp * ratio) for exp, ratio in zip(exposure_values, pe_ratio_values)]
    top10_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top10_pe_ratio


def calc_full_market_cap(sorted_exposure):
    mcap_list = query.get_fund_ratio_mcap(sorted_exposure)
    mcap_values = [float(market_cap['market_cap']) for security in sorted_exposure for market_cap in mcap_list
                   if security[0] == market_cap['security_isin']]
    exposure_values = [float(exposure[1]) for exposure in sorted_exposure]
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    calc_mcap = [float(exp * mcap) for exp, mcap in zip(exposure_values, mcap_values)]
    full_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return full_market_cap


def calc_top5_market_cap(top5_holdings):
    mcap_list = query.get_fund_ratio_mcap(top5_holdings)
    mcap_values = [float(market_cap['market_cap']) for security in top5_holdings for market_cap in mcap_list
                   if security[0] == market_cap['security_isin']]
    exposure_values = [float(exposure[1]) for exposure in top5_holdings]
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    calc_mcap = [float(exp * mcap) for exp, mcap in zip(exposure_values, mcap_values)]
    top5_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return top5_market_cap


def calc_top10_market_cap(top10_holdings):
    mcap_list = query.get_fund_ratio_mcap(top10_holdings)
    mcap_values = [float(market_cap['market_cap']) for security in top10_holdings for market_cap in mcap_list
                   if security[0] == market_cap['security_isin']]
    exposure_values = [float(exposure[1]) for exposure in top10_holdings]
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    calc_mcap = [float(exp * mcap) for exp, mcap in zip(exposure_values, mcap_values)]
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


def get_annualized_return(fund_code, reporting_date, fund_nav):
    nav_start_date = query.get_nav_start_date(fund_code)
    start_date_nav = -1
    start_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(str(reporting_date), "%Y-%m-%d").date()
    annualized_values = [(datetime.date(start_date.year, start_date.month, start_date.day), start_date_nav),
                         (datetime.date(end_date.year, end_date.month, end_date.day), fund_nav)]
    annualized_return = optimize.newton(lambda r: xnpv(r, annualized_values), 0.1)
    return annualized_return


def get_fund_ratios(fund_code, reporting_date):
    top5_pe_ratio = top10_pe_ratio = top5_market_cap = top10_market_cap = full_pe_ratio = full_market_cap = None
    fund_nav = float(query.get_fund_nav(fund_code, reporting_date)[0][0])
    portfolio_values = query.get_fund_portfolio(fund_code, reporting_date)
    benchmark_perf_1m = query.get_benchmark_perf_1m(fund_code, reporting_date)
    fund_return_list = query.get_all_fund_return(fund_code, reporting_date)
    portfolio_sum = 0
    if portfolio_values is not None:
        for value in portfolio_values:
            if value[1]:
                portfolio_sum += value[1]
    portfolio_sum = round(portfolio_sum * 100)

    if portfolio_sum == 100:
        sorted_exposure = sorted(portfolio_values, key=lambda i: i[1], reverse=True)
        full_ratio = calc_full_pe_ratio(sorted_exposure)
        full_pe_ratio = None if (full_ratio == 0) else full_ratio
        full_cap = calc_full_market_cap(sorted_exposure)
        full_market_cap = None if (full_cap == 0) else full_cap

    if portfolio_sum > 0:
        sorted_exposure = sorted(portfolio_values, key=lambda i: i[1], reverse=True)
        sorted_pf_values = [i for i in sorted_exposure if not (i[0] == 'CASH')]
        top5_holdings = sorted_pf_values[0:5]
        top10_holdings = sorted_pf_values[0:10]
        pe5_ratio = calc_top5_pe_ratio(top5_holdings)
        top5_pe_ratio = None if (pe5_ratio == 0) else pe5_ratio
        pe10_ratio = calc_top10_pe_ratio(top10_holdings)
        top10_pe_ratio = None if (pe10_ratio == 0) else pe10_ratio
        market5_cap = calc_top5_market_cap(top5_holdings)
        top5_market_cap = None if (market5_cap == 0) else market5_cap
        market10_cap = calc_top10_market_cap(top10_holdings)
        top10_market_cap = None if (market10_cap == 0) else market10_cap

    risk_free = query.get_risk_free_rate()
    negative_excess_returns_risk_free = get_negative_excess_return(fund_return_list, risk_free)
    sigma = round(math.sqrt(negative_excess_returns_risk_free / 12), 4)
    annualized_return = get_annualized_return(fund_code, reporting_date, fund_nav)

    fund_ratio_data = FundRatios()
    fund_ratio_data.set_fund_code(fund_code)
    fund_ratio_data.set_reporting_date(reporting_date)
    fund_ratio_data.set_full_pe_ratio(full_pe_ratio)
    fund_ratio_data.set_top5_pe_ratio(top5_pe_ratio)
    fund_ratio_data.set_top10_pe_ratio(top10_pe_ratio)
    fund_ratio_data.set_full_market_cap(full_market_cap)
    fund_ratio_data.set_top5_market_cap(top5_market_cap)
    fund_ratio_data.set_top10_market_cap(top10_market_cap)
    fund_ratio_data.set_standard_deviation(round(statistics.stdev(fund_return_list), 4))
    fund_ratio_data.set_median(round(statistics.median(fund_return_list), 4))
    fund_ratio_data.set_sigma(sigma)
    fund_ratio_data.set_sortino_ratio(round(((annualized_return - risk_free) / sigma), 4))
    fund_ratio_data.set_negative_excess_returns_risk_free(negative_excess_returns_risk_free)
    fund_ratio_data.set_fund_alpha(round(((fund_return_list[-1] - benchmark_perf_1m) * 100), 4))
    fund_ratio_data.set_updated_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fund_ratio_data.set_updated_by('ft-automation')
    print(fund_ratio_data)
    return fund_ratio_data


try:
    fund_code_list = query.get_fund_codes_fund_ratios('')
    fund_code_list.pop(0)
    for fund_detail in fund_code_list:
        fund_ratio_data = get_fund_ratios(fund_detail[0], fund_detail[1])
        query.put_fund_ratios(fund_ratio_data)

except Exception as error:
    print("Exception raised :", error)
