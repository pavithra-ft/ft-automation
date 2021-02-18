from bhav_copy_ac.database import orm_model as model
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, update, insert

ac_on_engine = create_engine(
    'mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/onboarding_ac_dev')
ac_on_db = sessionmaker(bind=ac_on_engine)
ac_on_session = ac_on_db()


def is_security_isin_code_exist(security_isin, security_code):
    is_security_isin_code = ac_on_session.query(model.MasSecurities).filter_by(security_isin=security_isin). \
        filter_by(security_code=security_code).count()
    return is_security_isin_code


def is_security_code_exist(security_code):
    is_security_code = ac_on_session.query(model.MasSecurities).filter_by(security_code=security_code).count()
    return is_security_code


def put_mas_securities_price(security_info):
    for security in security_info:
        if is_security_isin_code_exist(security.security_isin, security.security_code):
            sec_isin_code_query = update(model.MasSecurities).where(
                model.MasSecurities.security_isin == security.security_isin).where(
                model.MasSecurities.security_code == security.security_code).values(
                bse_prev_close_price=security.bse_prev_close_price, close_price_as_of=security.close_price_as_of)
            ac_on_engine.execute(sec_isin_code_query)
        elif is_security_code_exist(security.security_code):
            sec_code_query = update(model.MasSecurities).where(
                model.MasSecurities.security_code == security.security_code).values(
                security_isin=security.security_isin, bse_security_symbol=security.bse_security_symbol,
                bse_prev_close_price=security.bse_prev_close_price, close_price_as_of=security.close_price_as_of)
            ac_on_engine.execute(sec_code_query)
        else:
            print(security)


def put_mas_securities_list(security_info):
    for security in security_info:
        if not is_security_isin_code_exist(security.security_isin, security.security_code):
            sec_isin_code_query = insert(model.MasSecurities).values(
                security_isin=security.security_isin, security_name=security.security_name,
                security_code=security.security_code, bse_security_symbol=security.bse_security_symbol,
                industry=security.industry, bse_group=security.bse_group, is_active=security.is_active)
            ac_on_engine.execute(sec_isin_code_query)
        else:
            print(security)
