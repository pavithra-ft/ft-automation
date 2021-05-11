import re
import database.db_queries as query
import services.date_calculation as date
from pyjarowinkler import distance
from config.base_logger import app_logger
from dictionary.sector_dictionary import sector_dict
from model.index_tables_model import IndexPerformance
from extraction.bse_ratio_extraction import get_bse_data
from extraction.nse_pdf_extraction import get_nse_data
from dictionary.portfolio_dictionary import portfolio_dict


def get_isin(security_name):
    if portfolio_dict.__contains__(security_name):
        sec_name = portfolio_dict[security_name]
    else:
        sec_name = security_name
    isin_details = query.get_security_isin(sec_name.replace("'", " "))
    if len(isin_details) == 0:
        sec_name = sec_name.replace(".", " ").replace("'", " ")
        cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
        security_details = query.get_all_isin()
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
    app_logger.info(security_isin)
    return security_isin


def get_index_perf_calc(reporting_date, index_code):
    app_logger.info('Index Performance - Performance calculation is started')

    perf_1m_date = date.get_1m_date(reporting_date)
    perf_3m_date = date.get_3m_date(reporting_date)
    perf_6m_date = date.get_6m_date(reporting_date)
    perf_1y_date = date.get_1y_date(reporting_date)
    perf_2y_date = date.get_2y_date(reporting_date)
    perf_3y_date = date.get_3y_date(reporting_date)
    perf_5y_date = date.get_5y_date(reporting_date)
    start_date = query.get_index_start_date(index_code)

    start_index_price = query.get_index_start_price(start_date, index_code)
    curr_price = query.get_index_price_as_on_date(reporting_date, index_code)
    index_1m_price = query.get_index_price_as_on_date(perf_1m_date, index_code)
    index_3m_price = query.get_index_price_as_on_date(perf_3m_date, index_code)
    index_6m_price = query.get_index_price_as_on_date(perf_6m_date, index_code)
    index_1y_price = query.get_index_price_as_on_date(perf_1y_date, index_code)
    index_2y_price = query.get_index_price_as_on_date(perf_2y_date, index_code)
    index_3y_price = query.get_index_price_as_on_date(perf_3y_date, index_code)
    index_5y_price = query.get_index_price_as_on_date(perf_5y_date, index_code)

    date_power_1y = reporting_date - perf_1y_date
    date_power_2y = reporting_date - perf_2y_date
    date_power_3y = reporting_date - perf_3y_date
    date_power_5y = reporting_date - perf_5y_date
    power_inception = reporting_date - start_date

    perf_1m = round(((float(curr_price[-1][0]) / float(index_1m_price[-1][0])) - 1), 4) \
        if start_date <= perf_1m_date else None
    perf_3m = round(((float(curr_price[-1][0]) / float(index_3m_price[-1][0])) - 1), 4) \
        if start_date <= perf_3m_date else None
    perf_6m = round(((float(curr_price[-1][0]) / float(index_6m_price[-1][0])) - 1), 4) \
        if start_date <= perf_6m_date else None
    perf_1y = round((((float(curr_price[-1][0]) / float(index_1y_price[-1][0])) ** (365 / date_power_1y.days)) - 1), 4)\
        if start_date <= perf_1y_date else None
    perf_2y = round((((float(curr_price[-1][0]) / float(index_2y_price[-1][0])) ** (365 / date_power_2y.days)) - 1), 4)\
        if start_date <= perf_2y_date else None
    perf_3y = round((((float(curr_price[-1][0]) / float(index_3y_price[-1][0])) ** (365 / date_power_3y.days)) - 1), 4)\
        if start_date <= perf_3y_date else None
    perf_5y = round((((float(curr_price[-1][0]) / float(index_5y_price[-1][0])) ** (365 / date_power_5y.days)) - 1), 4)\
        if start_date <= perf_5y_date else None

    if power_inception.days >= 365:
        perf_inception = round((((float(curr_price[-1][0]) / start_index_price) **
                                 (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((float(curr_price[-1][0]) / start_index_price) - 1), 4)

    index_perf_data = {'index_code': index_code, 'perf_1m': perf_1m, 'perf_3m': perf_3m, 'perf_6m': perf_6m,
                       'perf_1y': perf_1y, 'perf_2y': perf_2y, 'perf_3y': perf_3y, 'perf_5y': perf_5y,
                       'perf_inception': perf_inception, 'reporting_date': reporting_date}
    app_logger.info('Index Performance - Performance calculation is completed')
    return index_perf_data


def get_index_ratios(index_code, nse_list, bse_list):
    app_logger.info('Index Performance - Ratios/Sector/Holding extraction is started')
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
                top_holding_isin = get_isin(ratios_data['top_holding_isin'])
            if ratios_data['top_sector_name'] is not None:
                if sector_dict.__contains__(ratios_data['top_sector_name'].capitalize().strip()):
                    industry = sector_dict[ratios_data['top_sector_name'].capitalize().strip()]
                else:
                    industry = ratios_data['top_sector_name'].capitalize().strip()
                top_sector_name = query.get_security_sector(industry)
            index_ratios_data.update({"standard_deviation": ratios_data['standard_deviation'],
                                      "pe_ratio": ratios_data['pe_ratio'], "top_sector_name": top_sector_name,
                                      "top_sector_exposure": ratios_data['top_sector_exposure'],
                                      "top_holding_isin": top_holding_isin,
                                      "top_holding_exposure": ratios_data['top_holding_exposure']})
    app_logger.info('Index Performance - Ratios/Sector/Holding extraction is Completed')
    return index_ratios_data


def get_index_performance(index_code, reporting_date, pdf_files):
    nse_list = get_nse_data(pdf_files)
    bse_list = get_bse_data()
    performance = get_index_perf_calc(reporting_date, index_code)
    ratios = get_index_ratios(index_code, nse_list, bse_list)

    index_performance = IndexPerformance()
    index_performance.set_index_code(performance['index_code'])
    index_performance.set_standard_deviation(ratios['standard_deviation'])
    index_performance.set_pe_ratio(ratios['pe_ratio'])
    index_performance.set_top_sector_name(ratios['top_sector_name'])
    index_performance.set_top_sector_exposure(ratios['top_sector_exposure'])
    index_performance.set_top_holding_isin(ratios['top_holding_isin'])
    index_performance.set_top_holding_exposure(ratios['top_holding_exposure'])
    index_performance.set_perf_1m(performance['perf_1m'])
    index_performance.set_perf_3m(performance['perf_3m'])
    index_performance.set_perf_6m(performance['perf_6m'])
    index_performance.set_perf_1y(performance['perf_1y'])
    index_performance.set_perf_2y(performance['perf_2y'])
    index_performance.set_perf_3y(performance['perf_3y'])
    index_performance.set_perf_5y(performance['perf_5y'])
    index_performance.set_perf_inception(performance['perf_inception'])
    index_performance.set_reporting_date(reporting_date)
    return index_performance
