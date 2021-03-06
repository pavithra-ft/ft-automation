import model.fund_details_extraction as extract
from datetime import datetime
from config.base_logger import app_logger


def get_fund_info(df):
    """
    This function extracts the basic Fund information of the Fund from the given excel file.

    :param df: A dataframe of the given excel data
    :return: A class object of basic fund information
    """
    app_logger.info('Fund info - Started')
    fund_info = extract.FundInfo()
    fund_info.set_fund_name(df.iloc[2, 2])
    fund_info.set_fund_code(df.iloc[3, 2])
    date = df.iloc[4, 2]
    reporting_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
    fund_info.set_reporting_date(reporting_date)
    fund_info.set_no_of_clients(df.iloc[5, 2])
    fund_info.set_current_aum(df.iloc[6, 2])
    fund_info.set_performance_1m(float(df.iloc[7, 2]))
    fund_info.set_market_cap_type_code(df.iloc[8, 2])
    fund_info.set_investment_style(df.iloc[9, 2])
    app_logger.info('Fund info - Completed')
    return fund_info


def get_fund_allocation_values(df):
    """
    This function extracts the Allocation values of the Fund from the given excel file.

    :param df: A dataframe of the given excel data
    :return: A class object of allocation values
    """
    app_logger.info('Allocation values - Started')
    fund_allocation = []
    index = 15
    while df.iloc[index, 4] != "TOTAL":
        if df.iloc[index, 5]:
            allocation_body = extract.FundAllocationExtraction()
            allocation_body.set_allocation(df.iloc[index, 4])
            allocation_body.set_exposure(df.iloc[index, 5])
            fund_allocation.append(allocation_body)
        index += 1
    app_logger.info('Allocation values - Completed')
    return fund_allocation


def get_market_cap_values(df):
    """
    This function extracts the Market cap values of the Fund from the given excel file.

    :param df: A dataframe of the given excel data
    :return: A class object of market cap values
    """
    app_logger.info('Market cap values - Started')
    cap_data = []
    index = 3
    while df.iloc[index, 4] != "TOTAL":
        if df.iloc[index, 5]:
            cap_data_body = extract.FundMarketCapExtraction()
            market_cap = df.iloc[index, 4].replace(" Cap", "")
            cap_data_body.set_type_market_cap(market_cap.capitalize())
            cap_data_body.set_exposure(float(df.iloc[index, 5]))
            cap_data.append(cap_data_body)
        index += 1
    app_logger.info('Market cap values - Completed')
    return cap_data


def get_fund_portfolio_values(df):
    """
    This function extracts the Portfolio values of the Fund from the given excel file.

    :param df: A dataframe of the given excel data
    :return: A class object of portfolio values
    """
    app_logger.info('Portfolio values - Started')
    portfolio_values = []
    index = 13
    while df.iloc[index, 1] != "TOTAL":
        if df.iloc[index, 1]:
            portfolio_body = extract.FundPortfolioExtraction()
            portfolio_body.set_security_name(df.iloc[index, 1].strip())
            exposure = df.iloc[index, 2]
            if not exposure:
                portfolio_body.set_exposure(0)
            else:
                portfolio_body.set_exposure(float(exposure))
            portfolio_values.append(portfolio_body)
        index += 1
    app_logger.info('Portfolio values - Completed')
    return portfolio_values


def get_fund_sector_values(df):
    """
    This function extracts the Sector values of the Fund from the given excel file.

    :param df: A dataframe of the given excel data
    :return: A class object of sector values
    """
    app_logger.info('Sector values - Started')
    sector_values = []
    index = 23
    while df.iloc[index, 4] != "TOTAL":
        if df.iloc[index, 4]:
            sector_body = extract.FundSectorExtraction()
            sector_body.set_sector_name(df.iloc[index, 4])
            exposure = df.iloc[index, 5]
            sector_body.set_exposure(float(exposure))
            sector_values.append(sector_body)
        index += 1
    app_logger.info('Sector values - Completed')
    return sector_values
