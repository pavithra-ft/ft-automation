import calendar
from envparse import env
from datetime import datetime
import database.orm_model as model
from sqlalchemy.orm import sessionmaker
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine, and_, update, insert

fr_engine = create_engine('mysql://' + env('DB_USER') + ':' + env('DB_PASS') + '@' + env('DB_HOST') + '/fund_rating')
fr_db = sessionmaker(bind=fr_engine)
fr_session = fr_db()


def is_security_isin_exist(security_isin):
    """

    @param security_isin:
    @return:
    """
    is_security_isin = fr_session.query(model.MasSecurities).filter_by(security_isin=security_isin).count()
    return is_security_isin


def get_market_value(security_isin, previous_1y_end_date, reporting_date):
    """

    @param security_isin:
    @param previous_1y_end_date:
    @param reporting_date:
    @return:
    """
    market_value_query = fr_session.query(model.SecurityPrices.turnover).filter_by(security_isin=security_isin).\
        filter(and_(model.SecurityPrices.reporting_date >= previous_1y_end_date,
                    model.SecurityPrices.reporting_date <= reporting_date)).all()
    market_value_list = [float(value[0]) for value in market_value_query]
    return market_value_list


def is_security_rating(fund_code, security_isin, reporting_date):
    """

    @param fund_code:
    @param security_isin:
    @param reporting_date:
    @return:
    """
    is_security_isin_exist = fr_session.query(model.SecurityRating).filter_by(fund_code=fund_code).\
        filter_by(security_isin=security_isin).filter_by(reporting_date=reporting_date).count()
    return is_security_isin_exist


def is_fund_rating(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    is_fund_rating_exist = fr_session.query(model.FundRating).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=reporting_date).count()
    return is_fund_rating_exist


def get_maturity_date(security_isin):
    """

    @param security_isin:
    @return:
    """
    security_prices = fr_session.query(model.SecurityPrices.maturity_date).filter_by(security_isin=security_isin). \
        order_by(model.SecurityPrices.reporting_date)
    primary_issuance = fr_session.query(model.PrimaryIssuance.maturity_date).filter_by(security_isin=security_isin). \
        order_by(model.PrimaryIssuance.reporting_date)
    maturity_date = security_prices.union(primary_issuance).all()[-1][0]
    return maturity_date


def get_security_market_value(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    market_value = fr_session.query(model.SecurityRating.market_value).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=reporting_date).all()
    market_value_list = [float(value[0]) for value in market_value if value[0] is not None]
    return market_value_list


def get_previous_month_aum(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    previous_1m_date = datetime.strptime(str(reporting_date), '%Y-%m-%d') - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    previous_aum = fr_session.query(model.FundRating.current_aum).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=previous_1m_end_date).all()
    return previous_aum


def get_previous_nav_units(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    previous_1m_date = datetime.strptime(str(reporting_date), '%Y-%m-%d') - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    previous_2m_date = datetime.strptime(str(reporting_date), '%Y-%m-%d') - relativedelta(months=2)
    previous_2m_end_date = previous_2m_date.replace(day=calendar.monthrange(previous_2m_date.year,
                                                                            previous_2m_date.month)[1])
    previous_3m_date = datetime.strptime(str(reporting_date), '%Y-%m-%d') - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    previous_nav_units = []
    prev_1m_nav = fr_session.query(model.FundRating.nav_units).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=previous_1m_end_date).all()[0][0]
    prev_2m_nav = fr_session.query(model.FundRating.nav_units).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=previous_2m_end_date).all()[0][0]
    prev_3m_nav = fr_session.query(model.FundRating.nav_units).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=previous_3m_end_date).all()[0][0]
    previous_nav_units.extend([prev_1m_nav, prev_2m_nav, prev_3m_nav])
    return previous_nav_units


def get_security_rating_score(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    rating_score = fr_session.query(model.SecurityRating.rating_score).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=reporting_date).all()
    rating_score_list = [float(score[0]) for score in rating_score]
    return rating_score_list


def get_security_liquidity_score(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    liquidity_score = fr_session.query(model.SecurityRating.liquidity_score).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=reporting_date).all()
    liquidity_score_list = [float(score[0]) for score in liquidity_score]
    return liquidity_score_list


def get_security_maturity_score(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    maturity_score = fr_session.query(model.SecurityRating.maturity_score).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=reporting_date).all()
    maturity_score_list = [float(score[0]) for score in maturity_score]
    return maturity_score_list


def get_prev_1m_transition_score(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    previous_1m_date = datetime.strptime(str(reporting_date), '%Y-%m-%d') - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    prev_1m_transition_score = fr_session.query(model.FundRating.transition_score).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=previous_1m_end_date).all()[0][0]
    return prev_1m_transition_score


def get_fund_weights():
    """

    @return:
    """
    nav_weight = fr_session.query(model.FundWeights.nav_weight).all()[0][0]
    credit_weight = fr_session.query(model.FundWeights.credit_weight).all()[0][0]
    liquidity_weight = fr_session.query(model.FundWeights.liquidity_weight).all()[0][0]
    maturity_weight = fr_session.query(model.FundWeights.maturity_weight).all()[0][0]
    fund_weights = {'nav_weight': float(nav_weight), 'credit_weight': float(credit_weight),
                    'liquidity_weight': float(liquidity_weight), 'maturity_weight': float(maturity_weight)}
    return fund_weights


def get_prev_2m_transition_score(fund_code, reporting_date):
    """

    @param fund_code:
    @param reporting_date:
    @return:
    """
    previous_2m_date = datetime.strptime(str(reporting_date), '%Y-%m-%d') - relativedelta(months=2)
    previous_2m_end_date = previous_2m_date.replace(day=calendar.monthrange(previous_2m_date.year,
                                                                            previous_2m_date.month)[1])
    prev_2m_transition_score = fr_session.query(model.FundRating.transition_score).filter_by(fund_code=fund_code).\
        filter_by(reporting_date=previous_2m_end_date).all()[0][0]
    return prev_2m_transition_score


def put_security_rating(security_rating_data):
    """

    @param security_rating_data:
    """
    if security_rating_data:
        if not is_security_rating(security_rating_data.fund_code, security_rating_data.security_isin,
                                  security_rating_data.reporting_date):
            security_rating_query = insert(model.SecurityRating).values(
                fund_code=security_rating_data.fund_code, security_isin=security_rating_data.security_isin,
                reporting_date=security_rating_data.reporting_date, exposure=security_rating_data.exposure,
                market_value=security_rating_data.market_value, rating_type=security_rating_data.rating_type,
                rating_symbol=security_rating_data.rating_symbol, rating_grade=security_rating_data.rating_grade,
                rating_score=security_rating_data.rating_score, total_turnover=security_rating_data.total_turnover,
                liquidity_grade=security_rating_data.liquidity_grade,
                liquidity_score=security_rating_data.liquidity_score,
                maturity_years=security_rating_data.maturity_years, maturity_score=security_rating_data.maturity_score,
                maturity_date=security_rating_data.maturity_date, created_ts=security_rating_data.created_ts,
                created_by=security_rating_data.created_by)
        else:
            security_rating_query = update(model.SecurityRating).where(
                model.SecurityRating.fund_code == security_rating_data.fund_code).where(
                model.SecurityRating.security_isin == security_rating_data.security_isin).where(
                model.SecurityRating.reporting_date == security_rating_data.reporting_date).values(
                fund_code=security_rating_data.fund_code, security_isin=security_rating_data.security_isin,
                reporting_date=security_rating_data.reporting_date, exposure=security_rating_data.exposure,
                market_value=security_rating_data.market_value, rating_type=security_rating_data.rating_type,
                rating_symbol=security_rating_data.rating_symbol, rating_grade=security_rating_data.rating_grade,
                rating_score=security_rating_data.rating_score, total_turnover=security_rating_data.total_turnover,
                liquidity_grade=security_rating_data.liquidity_grade,
                liquidity_score=security_rating_data.liquidity_score,
                maturity_years=security_rating_data.maturity_years, maturity_score=security_rating_data.maturity_score,
                maturity_date=security_rating_data.maturity_date, created_ts=security_rating_data.created_ts,
                created_by=security_rating_data.created_by)
        fr_session.execute(security_rating_query)
        # fr_session.commit()


def put_fund_rating(fund_rating_data):
    """

    @param fund_rating_data:
    """
    if not is_fund_rating(fund_rating_data.fund_code, fund_rating_data.reporting_date):
        fund_rating_query = insert(model.FundRating).values(
            fund_code=fund_rating_data.fund_code, reporting_date=fund_rating_data.reporting_date,
            current_aum=fund_rating_data.current_aum, nav_units=fund_rating_data.nav_units,
            nav_adj_aum_rating=fund_rating_data.nav_adj_aum_rating,
            credit_risk_score=fund_rating_data.credit_risk_score, liquidity_score=fund_rating_data.liquidity_score,
            maturity_score=fund_rating_data.maturity_score, transition_score=fund_rating_data.transition_score,
            fund_score=fund_rating_data.fund_score, created_ts=fund_rating_data.created_ts,
            created_by=fund_rating_data.created_by)
    else:
        fund_rating_query = update(model.FundRating).where(
            model.FundRating.fund_code == fund_rating_data.fund_code).where(
            model.FundRating.reporting_date == fund_rating_data.reporting_date).values(
            fund_code=fund_rating_data.fund_code, reporting_date=fund_rating_data.reporting_date,
            current_aum=fund_rating_data.current_aum, nav_units=fund_rating_data.nav_units,
            nav_adj_aum_rating=fund_rating_data.nav_adj_aum_rating,
            credit_risk_score=fund_rating_data.credit_risk_score, liquidity_score=fund_rating_data.liquidity_score,
            maturity_score=fund_rating_data.maturity_score, transition_score=fund_rating_data.transition_score,
            fund_score=fund_rating_data.fund_score, created_ts=fund_rating_data.created_ts,
            created_by=fund_rating_data.created_by)
    fr_session.execute(fund_rating_query)
    # fr_session.commit()
