import re
import calendar

from pyjarowinkler import distance
from dateutil.relativedelta import relativedelta

from extraction.bse_extraction import get_bse_data
from extraction.nse_pdf_extraction import get_nse_data
from dictionary.portfolio_dictionary import portfolio_dict
from services.db_actions import get_index_price_as_on_date, get_index_start_price, put_index_performance, \
    get_index_start_date, get_security_isin, get_all_isin, get_security_sector


def get_1m_date(reporting_date):
    previous_1m_date = reporting_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_3m_date(reporting_date):
    previous_3m_date = reporting_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    return previous_3m_end_date


def get_6m_date(reporting_date):
    previous_6m_date = reporting_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1])
    return previous_6m_end_date


def get_1y_date(reporting_date):
    previous_1y_date = reporting_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    return previous_1y_end_date


def get_2y_date(reporting_date):
    previous_2y_date = reporting_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1])
    return previous_2y_end_date


def get_3y_date(reporting_date):
    previous_3y_date = reporting_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1])
    return previous_3y_end_date


def get_5y_date(reporting_date):
    previous_5y_date = reporting_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1])
    return previous_5y_end_date


def get_isin(security_name, iq_database):
    if portfolio_dict.__contains__(security_name):
        sec_name = portfolio_dict[security_name]
    else:
        sec_name = security_name
    isin_details = get_security_isin(sec_name.replace("'", " "), iq_database)
    if len(isin_details) == 0:
        sec_name = sec_name.replace(".", " ").replace("'", " ")
        cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
        security_details = get_all_isin(iq_database)
        max_ratio = 0
        max_index = 0
        for value in range(len(security_details)):
            name = security_details[value][1].replace(".", " ").replace("'", " ")
            cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
            ratio = distance.get_jaro_distance(cleaned_sec_name, cleaned_name, winkler=True, scaling=0.1)
            if ratio > 0 and max_ratio < ratio:
                max_ratio = ratio
                max_index = value
        security_isin = security_details[max_index][0]
    else:
        security_isin = isin_details[0][0]
    print(security_isin)
    return security_isin


def get_index_performance(reporting_date, index_code, iq_database):
    start_date = get_index_start_date(index_code, iq_database)
    start_index_price = get_index_start_price(start_date, index_code, iq_database)
    curr_price = get_index_price_as_on_date(reporting_date, index_code, iq_database)
    perf_1m_date = get_1m_date(reporting_date)
    perf_3m_date = get_3m_date(reporting_date)
    perf_6m_date = get_6m_date(reporting_date)
    perf_1y_date = get_1y_date(reporting_date)
    perf_2y_date = get_2y_date(reporting_date)
    perf_3y_date = get_3y_date(reporting_date)
    perf_5y_date = get_5y_date(reporting_date)
    perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, perf_5y = None, None, None, None, None, None, None
    # Calculation of 1 month index performance
    if start_date <= perf_1m_date:
        index_1m_price = get_index_price_as_on_date(perf_1m_date, index_code, iq_database)
        perf_1m = round(((curr_price[0][0] / index_1m_price[0][0]) - 1), 4)
    # Calculation of 3 months index performance
    if start_date <= perf_3m_date:
        index_3m_price = get_index_price_as_on_date(perf_3m_date, index_code, iq_database)
        perf_3m = round(((curr_price[0][0] / index_3m_price[0][0]) - 1), 4)
    # Calculation of 6 months index performance
    if start_date <= perf_6m_date:
        index_6m_price = get_index_price_as_on_date(perf_6m_date, index_code, iq_database)
        perf_6m = round(((curr_price[0][0] / index_6m_price[0][0]) - 1), 4)
    # Calculation of 1 year index performance
    if start_date <= perf_1y_date:
        index_1y_price = get_index_price_as_on_date(perf_1y_date, index_code, iq_database)
        date_power_1y = reporting_date - perf_1y_date
        perf_1y = round((((curr_price[0][0] / index_1y_price[0][0]) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years index performance
    if start_date <= perf_2y_date:
        index_2y_price = get_index_price_as_on_date(perf_2y_date, index_code, iq_database)
        date_power_2y = reporting_date - perf_2y_date
        perf_2y = round((((curr_price[0][0] / index_2y_price[0][0]) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years index performance
    if start_date <= perf_3y_date:
        index_3y_price = get_index_price_as_on_date(perf_3y_date, index_code, iq_database)
        date_power_3y = reporting_date - perf_3y_date
        perf_3y = round((((curr_price[0][0] / index_3y_price[0][0]) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years index performance
    if start_date <= perf_5y_date:
        index_5y_price = get_index_price_as_on_date(perf_5y_date, index_code, iq_database)
        date_power_5y = reporting_date - perf_5y_date
        perf_5y = round((((curr_price[0][0] / index_5y_price[0][0]) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of index performance inception
    power_inception = reporting_date - start_date
    if power_inception >= 365:
        perf_inception = round((((curr_price[0][0] / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    index_perf_data = {"index_code": index_code, "perf_1m": perf_1m, "perf_3m": perf_3m, "perf_6m": perf_6m,
                       "perf_1y": perf_1y, "perf_2y": perf_2y, "perf_3y": perf_3y, "perf_5y": perf_5y,
                       "perf_inception": perf_inception, "reporting_date": reporting_date}
    return index_perf_data


def get_index_ratios(index_code, nse_list, bse_list, iq_database):
    top_sector_name, top_holding_isin = None, None
    index_ratios_data = {"standard_deviation": None, "pe_ratio": None, "top_sector_name": None,
                         "top_sector_exposure": None, "top_holding_isin": None, "top_holding_exposure": None}
    index_ratio_list = []
    for nse in nse_list:
        index_ratio_list.append(nse)
    for bse in bse_list:
        index_ratio_list.append(bse)
    for ratios_data in index_ratio_list:
        if ratios_data['index_code'] == index_code:
            if ratios_data['top_holding_isin'] is not None:
                top_holding_isin = get_isin(ratios_data['top_holding_isin'], iq_database)
            if ratios_data['top_sector_name'] is not None:
                industry = ratios_data['top_sector_name'].capitalize().strip()
                top_sector_name = get_security_sector(industry, iq_database)
            index_ratios_data.update({"standard_deviation": ratios_data['standard_deviation'],
                                      "pe_ratio": ratios_data['pe_ratio'], "top_sector_name": top_sector_name,
                                      "top_sector_exposure": ratios_data['top_sector_exposure'],
                                      "top_holding_isin": top_holding_isin,
                                      "top_holding_exposure": ratios_data['top_holding_exposure']})
    return index_ratios_data


def index_performance(index_code, reporting_date, pdf_files, iq_database):
    index_performance = []
    nse_list = get_nse_data(pdf_files)
    bse_list = get_bse_data()
    performance = get_index_performance(reporting_date, index_code, iq_database)
    ratios = get_index_ratios(index_code, nse_list, bse_list, iq_database)
    index_performance.append({"index_code": performance['index_code'],
                              "standard_deviation": ratios['standard_deviation'], "pe_ratio": ratios['pe_ratio'],
                              "top_sector_name": ratios['top_sector_name'],
                              "top_sector_exposure": ratios['top_sector_exposure'],
                              "top_holding_isin": ratios['top_holding_isin'],
                              "top_holding_exposure": ratios['top_holding_exposure'], "perf_1m": performance['perf_1m'],
                              "perf_3m": performance['perf_3m'], "perf_6m": performance['perf_6m'],
                              "perf_1y": performance['perf_1y'], "perf_2y": performance['perf_2y'],
                              "perf_3y": performance['perf_3y'], "perf_5y": performance['perf_5y'],
                              "perf_inception": performance['perf_inception'],
                              "reporting_date": performance['reporting_date']})
    put_index_performance(index_performance, iq_database)
    for i in index_performance:
        print(i)
