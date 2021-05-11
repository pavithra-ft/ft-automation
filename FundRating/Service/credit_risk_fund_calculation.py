import calendar
from datetime import datetime
import model.tables_model as model
import database.db_actions as query
from dateutil.relativedelta import relativedelta
from config.base_logger import app_logger, sql_logger


def get_rating_symbol(rating):
    """

    @param rating:
    @return:
    """
    unrating_list = ['SOV', 'Sovereign', 'SOVEREIGN', 'UNRATED']
    get_rating = rating.split(' ')
    for i in get_rating:
        if '(' in i[0]:
            get_rating.remove(i)
    if len(get_rating) > 1:
        if '(' in get_rating[-1]:
            grade_index = get_rating[-1].index('(')
            rating_symbol = get_rating[-1][:grade_index]
        else:
            rating_symbol = get_rating[-1]
    elif len(get_rating) == 1:
        if '[' in get_rating[0]:
            grade_index = get_rating[0].replace('[', '').replace(']', ' ')
            rating_symbol = grade_index.split(' ')[-1]
        elif get_rating[0] in unrating_list:
            rating_symbol = None
        else:
            rating_symbol = get_rating[0]
    else:
        rating_symbol = get_rating[0]
    return rating_symbol


def get_rating_type(rating):
    """

    @param rating:
    @return:
    """
    if '[' in rating:
        grade_index = rating.replace('[', '').replace(']', ' ')
        rating_type = grade_index.split(' ')[0]
    elif len(rating.split(' ')) > 1:
        rating_type = rating.split(' ')[0]
    else:
        rating_type = rating
    return rating_type


def get_rating_score(rating_symbol, exposure):
    """

    @param rating_symbol:
    @param exposure:
    @return:
    """
    if rating_symbol == 'AAA' or rating_symbol == 'LAAA':
        rating_grade = 1
        rating_score = round(float(1 * float(exposure)), 6)
    elif rating_symbol == 'AA+' or rating_symbol == 'LAA+':
        rating_grade = 2
        rating_score = round(float(2 * float(exposure)), 6)
    elif rating_symbol == 'AA' or rating_symbol == 'LAA':
        rating_grade = 3
        rating_score = round(float(3 * float(exposure)), 6)
    elif rating_symbol == 'AA-' or rating_symbol == 'LAA-':
        rating_grade = 4
        rating_score = round(float(4 * float(exposure)), 6)
    else:
        rating_grade = 5
        rating_score = round(float(5 * float(exposure)), 6)
    return rating_grade, rating_score


def get_total_turnover(security_isin, reporting_date):
    """

    @param security_isin:
    @param reporting_date:
    @return:
    """
    previous_1y_date = datetime.strptime(str(reporting_date), '%Y-%m-%d').date() - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    market_value_list = query.get_market_value(security_isin, previous_1y_end_date, reporting_date)
    total_turnover = sum(market_value_list)
    return total_turnover


def get_liquidity_grade(market_value, total_turnover):
    """

    @param market_value:
    @param total_turnover:
    @return:
    """
    if market_value and total_turnover:
        liquidity = float(float(float(market_value) / float(total_turnover)) * 100)
        if liquidity < 10:
            liquidity_grade = 1
        elif 10 < liquidity < 20:
            liquidity_grade = 2
        elif 20 < liquidity < 30:
            liquidity_grade = 3
        elif 30 < liquidity < 40:
            liquidity_grade = 4
        else:
            liquidity_grade = 5
    elif market_value == 0 or total_turnover == 0:
        liquidity_grade = 5
    else:
        liquidity_grade = 5
    return liquidity_grade


def get_maturity_years(maturity_date, reporting_date):
    """

    @param maturity_date:
    @param reporting_date:
    @return:
    """
    years = (datetime.strptime(str(maturity_date), '%Y-%m-%d').date() -
             datetime.strptime(str(reporting_date), '%Y-%m-%d').date()).days
    maturity_years = float(years) / 365
    return maturity_years


def get_maturity_score(maturity_years, exposure):
    """

    @param maturity_years:
    @param exposure:
    @return:
    """
    if maturity_years < 1:
        maturity_score = round(float(1 * float(exposure)), 6)
    elif 1 <= maturity_years < 2:
        maturity_score = round(float(2 * float(exposure)), 6)
    elif 2 <= maturity_years < 2.5:
        maturity_score = round(float(3 * float(exposure)), 6)
    elif 2.5 <= maturity_years < 3:
        maturity_score = round(float(4 * float(exposure)), 6)
    elif maturity_years >= 3:
        maturity_score = round(float(5 * float(exposure)), 6)
    else:
        maturity_score = round(float(5 * float(exposure)), 6)
    return maturity_score


def get_security_rating(fund_info, portfolio_values):
    """

    @param fund_info:
    @param portfolio_values:
    @return:
    """
    security_rating_list = []

    for portfolio in portfolio_values:
        isin_check = query.is_security_isin_exist(portfolio.get_security_isin())
        if isin_check:
            rating_symbol = get_rating_symbol(portfolio.get_rating())
            rating_type = get_rating_type(portfolio.get_rating())
            rating_grade, rating_score = get_rating_score(rating_symbol, portfolio.get_exposure())
            total_turnover = get_total_turnover(portfolio.get_security_isin(), fund_info.get_reporting_date())
            liquidity_grade = get_liquidity_grade(portfolio.get_market_value(), total_turnover)
            liquidity_score = round(float(float(liquidity_grade) * float(portfolio.get_exposure())), 6)
            maturity_date = query.get_maturity_date(portfolio.get_security_isin())
            maturity_years = get_maturity_years(maturity_date, fund_info.get_reporting_date())
            maturity_score = get_maturity_score(maturity_years, portfolio.get_exposure())
        else:
            if portfolio.get_rating() is not None:
                rating_symbol = get_rating_symbol(portfolio.get_rating())
            else:
                rating_symbol = None

            rating_grade = 5
            rating_score = round(float(5 * float(portfolio.get_exposure())), 6)
            rating_type = get_rating_type(portfolio.get_rating()) if portfolio.get_rating() is not None else None

            total_turnover = get_total_turnover(portfolio.get_security_isin(), fund_info.get_reporting_date())
            liquidity_grade = 5
            liquidity_score = round(float(float(liquidity_grade) * float(portfolio.get_exposure())), 6)
            maturity_date, maturity_years = None, None
            maturity_score = round(float(5 * float(portfolio.get_exposure())), 6)

        security_rating_data = model.SecurityRating()
        security_rating_data.set_fund_code(fund_info.get_fund_code())
        security_rating_data.set_security_isin(portfolio.get_security_isin())
        security_rating_data.set_reporting_date(fund_info.get_reporting_date())
        security_rating_data.set_exposure(round(portfolio.get_exposure(), 6))
        security_rating_data.set_market_value(portfolio.get_market_value())
        security_rating_data.set_rating_type(rating_type)
        security_rating_data.set_rating_symbol(rating_symbol)
        security_rating_data.set_rating_grade(rating_grade)
        security_rating_data.set_rating_score(rating_score)
        security_rating_data.set_total_turnover(total_turnover)
        security_rating_data.set_liquidity_grade(liquidity_grade)
        security_rating_data.set_liquidity_score(liquidity_score)
        security_rating_data.set_maturity_years(maturity_years)
        security_rating_data.set_maturity_score(maturity_score)
        security_rating_data.set_maturity_date(maturity_date)
        security_rating_data.set_created_ts(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        security_rating_data.set_created_by('ft-automation')
        security_rating_list.append(security_rating_data)
    return security_rating_list


def get_fund_rating(fund_info):
    """

    @param fund_info:
    @return:
    """
    previous_aum = query.get_previous_month_aum(fund_info.get_fund_code(), fund_info.get_reporting_date())[0][0]
    previous_nav_units = query.get_previous_nav_units(fund_info.get_fund_code(), fund_info.get_reporting_date())
    current_aum = sum(query.get_security_market_value(fund_info.get_fund_code(), fund_info.get_reporting_date()))
    nav_units = round(((float(current_aum) - float(previous_aum)) / float(current_aum)) * 100, 6)
    credit_risk_score = round(sum(query.get_security_rating_score(fund_info.get_fund_code(),
                                                                  fund_info.get_reporting_date())), 6)
    liquidity_score = round(sum(query.get_security_liquidity_score(fund_info.get_fund_code(),
                                                                   fund_info.get_reporting_date())), 6)
    maturity_score = round(sum(query.get_security_maturity_score(fund_info.get_fund_code(),
                                                                 fund_info.get_reporting_date())), 6)

    if nav_units > 0:
        nav_adj_aum_rating = 2
    elif 0 > nav_units > -5:
        nav_adj_aum_rating = 3
    elif -5 > nav_units > -10:
        nav_adj_aum_rating = 4
    elif nav_units < -10:
        nav_adj_aum_rating = 5
    elif nav_units < -3 and previous_nav_units[0] < 0 and previous_nav_units[1] < 0 and previous_nav_units[2] < 0:
        nav_adj_aum_rating = 5
    else:
        nav_adj_aum_rating = 5

    prev_1m_transition_score = query.get_prev_1m_transition_score(fund_info.get_fund_code(),
                                                                  fund_info.get_reporting_date())
    prev_2m_transition_score = query.get_prev_2m_transition_score(fund_info.get_fund_code(),
                                                                  fund_info.get_reporting_date())
    transition_score = round((float(prev_1m_transition_score) * 0.6 + float(prev_2m_transition_score) * 0.4), 6)

    fund_weights = query.get_fund_weights()
    fund_score = round(float(nav_adj_aum_rating * fund_weights['nav_weight'] +
                             credit_risk_score * fund_weights['credit_weight'] +
                             liquidity_score * fund_weights['liquidity_weight'] +
                             maturity_score * fund_weights['maturity_weight']), 6)

    fund_rating_data = model.FundRating()
    fund_rating_data.set_fund_code(fund_info.get_fund_code())
    fund_rating_data.set_reporting_date(fund_info.get_reporting_date())
    fund_rating_data.set_current_aum(current_aum)
    fund_rating_data.set_nav_units(nav_units)
    fund_rating_data.set_nav_adj_aum_rating(nav_adj_aum_rating)
    fund_rating_data.set_credit_risk_score(credit_risk_score)
    fund_rating_data.set_liquidity_score(liquidity_score)
    fund_rating_data.set_maturity_score(maturity_score)
    fund_rating_data.set_transition_score(transition_score)
    fund_rating_data.set_fund_score(fund_score)
    fund_rating_data.set_created_ts(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fund_rating_data.set_created_by('ft-automation')
    return fund_rating_data


def put_rating_record(fund_info, security_rating_list, fund_rating_data):
    """

    @param fund_info:
    @param security_rating_list:
    @param fund_rating_data:
    """
    try:
        for security_rating_data in security_rating_list:
            query.put_security_rating(security_rating_data)
        query.put_fund_rating(fund_rating_data)
        app_logger.info(str(fund_info.get_reporting_date()) + ' - ' + fund_info.get_fund_code() +
                        ' Record inserted successfully')
        sql_logger.info(str(fund_info.get_reporting_date()) + ' - ' + fund_info.get_fund_code() +
                        ' Record inserted successfully')
        query.fr_session.commit()
    except Exception as error:
        query.fr_session.rollback()
        app_logger.info('Exception raised in queries: '+str(error))
    finally:
        query.fr_session.close()
