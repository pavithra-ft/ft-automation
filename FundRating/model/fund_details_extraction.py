class FundInfo:
    def __init__(self):
        self.fund_code = None
        self.fund_name = None
        self.reporting_date = None
        self.current_aum = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_fund_name(self, fund_name=None):
        self.fund_name = fund_name

    def get_fund_name(self):
        return self.fund_name

    def set_reporting_date(self, reporting_date=None):
        self.reporting_date = reporting_date

    def get_reporting_date(self):
        return self.reporting_date

    def set_current_aum(self, current_aum=None):
        self.current_aum = current_aum

    def get_current_aum(self):
        return self.current_aum

    def __repr__(self):
        return "<FundInfo(fund_code='{0}', fund_name='{1}', reporting_date='{2}', current_aum='{3}')>".format(
                self.fund_code, self.fund_name, self.reporting_date, self.current_aum)


class FundPortfolioExtraction:
    def __init__(self):
        self.security_name = None
        self.security_isin = None
        self.rating = None
        self.market_value = None
        self.exposure = None

    def set_security_name(self, security_name=None):
        self.security_name = security_name

    def get_security_name(self):
        return self.security_name

    def set_security_isin(self, security_isin=None):
        self.security_isin = security_isin

    def get_security_isin(self):
        return self.security_isin

    def set_rating(self, rating=None):
        self.rating = rating

    def get_rating(self):
        return self.rating

    def set_market_value(self, market_value=None):
        self.market_value = market_value

    def get_market_value(self):
        return self.market_value

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def __repr__(self):
        return "<FundPortfolioExtraction(security_name='{0}', security_isin='{1}', rating='{2}', market_value='{3}', " \
               "exposure='{4}')>".format(self.security_name, self.security_isin, self.rating, self.market_value,
                                         self.exposure)
