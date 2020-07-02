import re
from pyjarowinkler import distance
from database.db_queries import iq_session
from config.base_logger import app_logger, sql_logger
from dictionary.portfolio_dictionary import portfolio_dict
from extraction.security_ratio_bse_500 import get_security_ratio
from database.db_queries import get_security_isin, get_all_isin, put_mas_securities


def get_isin(security_name):
    if portfolio_dict.__contains__(security_name):
        sec_name = portfolio_dict[security_name]
    else:
        sec_name = security_name
    isin_details = get_security_isin(sec_name)
    if len(isin_details) == 0:
        sec_name = sec_name.replace(".", " ").replace("'", " ")
        cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
        security_details = get_all_isin()
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


def get_mas_security_ratio(security_ratio_list):
    app_logger.info('Mas Securities - Ratios extraction is started')
    mas_security_ratio_list = []
    for security in security_ratio_list:
        security_isin = get_isin(security['securtiy_name'])
        # Get pe_ratio
        if security['price_to_earnings'] == '--' or security['price_to_earnings'] is None:
            pe_ratio = None
        else:
            pe_ratio = security['price_to_earnings']
        # Get pb_ratio
        if security['price_to_book'] == '--' or security['price_to_book'] is None:
            pb_ratio = None
        else:
            pb_ratio = security['price_to_book']
        # Get Dividend yield
        if security['dividend_yield'] == '--' or security['dividend_yield'] is None:
            dividend_yield = None
        else:
            if float(security['dividend_yield']):
                dividend_yield = round((float(security['dividend_yield']) / 100), 4)
            else:
                dividend_yield = None
        # Get Earning Per Share
        if security['earning_per_share'] == '--' or security['earning_per_share'] is None:
            eps = None
        else:
            eps = security['earning_per_share']

        security_ratio_body = {'security_isin': security_isin, 'pe_ratio': pe_ratio, 'pb_ratio': pb_ratio, 'eps': eps,
                               'dividend_yield': dividend_yield}
        mas_security_ratio_list.append(security_ratio_body)
    app_logger.info('Mas Securities - Ratios extraction is completed')
    return mas_security_ratio_list


if __name__ == "__main__":
    sql_logger.info('Mas Securities - Ratios extraction is started')
    security_ratio_list = get_security_ratio()
    mas_security_ratio_list = get_mas_security_ratio(security_ratio_list)
    try:
        put_mas_securities(mas_security_ratio_list)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        app_logger.info('Exception raised in queries : ' + str(error))
        sql_logger.info('Exception raised in queries : ' + str(error))
    finally:
        iq_session.close()
    sql_logger.info('Mas Securities - Ratios extraction is started')
