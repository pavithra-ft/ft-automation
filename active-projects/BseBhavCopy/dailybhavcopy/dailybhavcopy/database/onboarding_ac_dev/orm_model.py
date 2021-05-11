from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT, VARCHAR

Base = declarative_base()


class MasSecurities(Base):
    __tablename__ = 'mas_securities'
    security_isin = Column(VARCHAR, nullable=False, primary_key=True)
    security_name = Column(VARCHAR, nullable=False, primary_key=True)
    security_code = Column(VARCHAR)
    bse_security_symbol = Column(VARCHAR)
    nse_security_symbol = Column(VARCHAR)
    industry = Column(VARCHAR)
    share_class_type = Column(VARCHAR)
    bse_group = Column(VARCHAR)
    bse_prev_close_price = Column(DOUBLE)
    nse_prev_close_price = Column(DOUBLE)
    close_price_as_of = Column(DATE)
    is_active = Column(TINYINT)
