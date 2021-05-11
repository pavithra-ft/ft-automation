import model.fund_details_extraction as extract
from datetime import datetime
from config.base_logger import app_logger


def get_fund_info(df):
    """

    @param df:
    @return:
    """
    app_logger.info('Fund info - Started')
    fund_info = extract.FundInfo()
    fund_info.set_fund_name(df.iloc[0, 2])
    fund_info.set_fund_code(df.iloc[1, 2])
    date = df.iloc[2, 2]
    reporting_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
    fund_info.set_reporting_date(reporting_date)
    fund_info.set_current_aum(df.iloc[3, 2])
    app_logger.info('Fund info - Completed')
    return fund_info


def get_fund_portfolio_values(df):
    """

    @param df:
    @return:
    """
    app_logger.info('Portfolio values - Started')
    portfolio_values = []
    index = 7
    while df.iloc[index, 1] != "Total":
        if df.iloc[index, 1]:
            portfolio_body = extract.FundPortfolioExtraction()
            portfolio_body.set_security_name(df.iloc[index, 1].strip())
            portfolio_body.set_security_isin(df.iloc[index, 2].strip())
            rating = df.iloc[index, 3]
            if rating:
                portfolio_body.set_rating(df.iloc[index, 3].strip())
            market_value = df.iloc[index, 4]
            if market_value:
                portfolio_body.set_market_value(market_value.strip())
            exposure = df.iloc[index, 5]
            if not exposure:
                portfolio_body.set_exposure(0)
            else:
                portfolio_body.set_exposure(float(exposure))
            portfolio_values.append(portfolio_body)
        index += 1
    app_logger.info('Portfolio values - Completed')
    return portfolio_values
