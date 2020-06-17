from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, extract, func, update, insert

from database.orm_model import IndexPrices, IndexPerformance, MasSectors, MasIndices, MasSecurities

# app_engine = create_engine('mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/app')
# fs_engine = create_engine('mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/fs')
# iq_engine = create_engine('mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/iq')

app_engine = create_engine('mysql://pavi:root@127.0.0.1/app')
fs_engine = create_engine('mysql://pavi:root@127.0.0.1/fs')
iq_engine = create_engine('mysql://pavi:root@127.0.0.1/iq')

app_db = sessionmaker(bind=app_engine)
fs_db = sessionmaker(bind=fs_engine)
iq_db = sessionmaker(bind=iq_engine)

app_session = app_db()
fs_session = fs_db()
iq_session = iq_db()


def get_mas_indices():
    mas_indices_query = iq_session.query(func.distinct(MasIndices.index_code)).all()
    mas_indices = [index[0] for index in mas_indices_query]
    return mas_indices


def get_index_start_price(index_code, start_date):
    start_index_price = iq_session.query(IndexPrices.index_price_close).filter_by(index_code=index_code).\
        filter_by(index_price_as_on_date=start_date).all()[0][0]
    return start_index_price


def get_index_start_date(index_code):
    start_date = iq_session.query(IndexPrices.index_price_as_on_date).filter_by(index_code=index_code).\
        order_by(IndexPrices.index_price_as_on_date.asc()).limit(1).all()[0][0]
    return start_date


def get_index_price_as_on_date(date, index_code):
    date_month = datetime.strptime(str(date), "%Y-%m-%d").month
    date_year = datetime.strptime(str(date), "%Y-%m-%d").year
    index_price = iq_session.query(IndexPrices.index_price_close).filter(IndexPrices.index_code == index_code). \
        filter(extract('year', IndexPrices.index_price_as_on_date) == date_year). \
        filter(extract('month', IndexPrices.index_price_as_on_date) == date_month).all()[-1][0]
    return index_price


def get_security_isin(security_name):
    security_isin = iq_session.query(MasSecurities.security_isin).filter_by(security_name=security_name).all()
    return security_isin


def get_all_isin():
    all_isin_list = iq_session.query().with_entities(MasSecurities.security_isin, MasSecurities.security_name).all()
    return all_isin_list


def get_security_sector(industry):
    sector = iq_session.query(MasSectors.sector).filter_by(industry=industry).all()[0][0]
    return sector


def is_index_performance_exist(index_code, reporting_date):
    is_index_performance = iq_session.query(IndexPerformance).filter_by(index_code=index_code).\
        filter_by(reporting_date=reporting_date).count()
    return is_index_performance


def put_index_performance(index_perf_data):
    for data in index_perf_data:
        if is_index_performance_exist(data['index_code'], data['reporting_date']):
            index_perf = update(IndexPerformance).where(IndexPerformance.index_code == data['index_code']).\
                where(IndexPerformance.reporting_date == data['reporting_date']).values(
                index_code=data['index_code'], standard_deviation=data['standard_deviation'], pe_ratio=data['pe_ratio'],
                top_sector_name=data['top_sector_name'], top_sector_exposure=data['top_sector_exposure'],
                top_holding_isin=data['top_holding_isin'], top_holding_exposure=data['top_holding_exposure'],
                perf_1m=data['perf_1m'], perf_3m=data['perf_3m'], perf_6m=data['perf_6m'], perf_1y=data['perf_1y'],
                perf_2y=data['perf_2y'], perf_3y=data['perf_3y'], perf_5y=data['perf_5y'],
                perf_inception=data['perf_inception'], reporting_date=data['reporting_date'])
        else:
            index_perf = insert(IndexPerformance).values(
                index_code=data['index_code'], standard_deviation=data['standard_deviation'], pe_ratio=data['pe_ratio'],
                top_sector_name=data['top_sector_name'], top_sector_exposure=data['top_sector_exposure'],
                top_holding_isin=data['top_holding_isin'], top_holding_exposure=data['top_holding_exposure'],
                perf_1m=data['perf_1m'], perf_3m=data['perf_3m'], perf_6m=data['perf_6m'], perf_1y=data['perf_1y'],
                perf_2y=data['perf_2y'], perf_3y=data['perf_3y'], perf_5y=data['perf_5y'],
                perf_inception=data['perf_inception'], reporting_date=data['reporting_date'])
        iq_engine.execute(index_perf)


def put_mas_securities(mas_security_ratio_list):
    for ratio in mas_security_ratio_list:
        mas_securities = update(MasSecurities).where(MasSecurities.security_isin == ratio['security_isin']).values(
            market_cap_value=ratio['market_cap_value'], pe_ratio=ratio['pe_ratio'], pb_ratio=ratio['pb_ratio'],
            eps=ratio['eps'], dividend_yield=ratio['dividend_yield'])
        iq_engine.execute(mas_securities)


def put_index_prices(index_price_data):
    for index in index_price_data:
        index_price = insert(IndexPrices).values(
            index_code=index['index_code'], index_price_open=index['Open'], index_price_high=index['High'],
            index_price_low=index['Low'], index_price_close=index['Close'], index_price_as_on_date=index['Date'])
        iq_engine.execute(index_price)
