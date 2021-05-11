from bhav_copy_ni.database import orm_model as model
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, update, insert

ni_on_engine = create_engine(
    'mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/onboarding_ni_dev')
ni_on_db = sessionmaker(bind=ni_on_engine)
ni_on_session = ni_on_db()


def is_security_isin_symbol_exist(security_isin, nse_security_symbol):
    is_security_isin_symbol = ni_on_session.query(model.MasSecurities).filter_by(security_isin=security_isin). \
        filter_by(nse_security_symbol=nse_security_symbol).count()
    return is_security_isin_symbol


def put_mas_securities_price(security_info):
    for security in security_info:
        if is_security_isin_symbol_exist(security.security_isin, security.nse_security_symbol):
            sec_isin_symbol_query = update(model.MasSecurities).where(
                model.MasSecurities.security_isin == security.security_isin).where(
                model.MasSecurities.nse_security_symbol == security.nse_security_symbol).values(
                nse_prev_close_price=security.nse_prev_close_price, close_price_as_of=security.close_price_as_of)
            ni_on_engine.execute(sec_isin_symbol_query)
        else:
            print(security)


def put_mas_securities_list(security_info):
    for security in security_info:
        if not is_security_isin_symbol_exist(security.security_isin, security.nse_security_symbol):
            sec_isin_symbol_query = insert(model.MasSecurities).values(
                security_isin=security.security_isin, security_name=security.security_name,
                nse_security_symbol=security.nse_security_symbol, is_active=security.is_active)
            ni_on_engine.execute(sec_isin_symbol_query)
