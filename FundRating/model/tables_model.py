class SecurityRating:
    def __init__(self):
        self.fund_code = None
        self.security_isin = None
        self.reporting_date = None
        self.exposure = None
        self.market_value = None
        self.rating_type = None
        self.rating_symbol = None
        self.rating_grade = None
        self.rating_score = None
        self.total_turnover = None
        self.liquidity_grade = None
        self.liquidity_score = None
        self.maturity_years = None
        self.maturity_score = None
        self.maturity_date = None
        self.created_ts = None
        self.created_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_security_isin(self, security_isin=None):
        self.security_isin = security_isin

    def get_security_isin(self):
        return self.security_isin

    def set_reporting_date(self, reporting_date=None):
        self.reporting_date = reporting_date

    def get_reporting_date(self):
        return self.reporting_date

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def set_market_value(self, market_value=None):
        self.market_value = market_value

    def get_market_value(self):
        return self.market_value

    def set_rating_type(self, rating_type=None):
        self.rating_type = rating_type

    def get_rating_type(self):
        return self.rating_type

    def set_rating_symbol(self, rating_symbol=None):
        self.rating_symbol = rating_symbol

    def get_rating_symbol(self):
        return self.rating_symbol

    def set_rating_grade(self, rating_grade=None):
        self.rating_grade = rating_grade

    def get_rating_grade(self):
        return self.rating_grade

    def set_rating_score(self, rating_score=None):
        self.rating_score = rating_score

    def get_rating_score(self):
        return self.rating_score

    def set_total_turnover(self, total_turnover=None):
        self.total_turnover = total_turnover

    def get_total_turnover(self):
        return self.total_turnover

    def set_liquidity_grade(self, liquidity_grade=None):
        self.liquidity_grade = liquidity_grade

    def get_liquidity_grade(self):
        return self.liquidity_grade

    def set_liquidity_score(self, liquidity_score=None):
        self.liquidity_score = liquidity_score

    def get_liquidity_score(self):
        return self.liquidity_score

    def set_maturity_years(self, maturity_years=None):
        self.maturity_years = maturity_years

    def get_maturity_years(self):
        return self.maturity_years

    def set_maturity_score(self, maturity_score=None):
        self.maturity_score = maturity_score

    def get_maturity_score(self):
        return self.maturity_score

    def set_maturity_date(self, maturity_date=None):
        self.maturity_date = maturity_date

    def get_maturity_date(self):
        return self.maturity_date

    def set_created_ts(self, created_ts=None):
        self.created_ts = created_ts

    def get_created_ts(self):
        return self.created_ts

    def set_created_by(self, created_by=None):
        self.created_by = created_by

    def get_created_by(self):
        return self.created_by

    def __repr__(self):
        return "<SecurityRating(fund_code='{0}', security_isin='{1}', reporting_date='{2}', exposure='{3}', " \
               "market_value='{4}', rating_type='{5}', rating_symbol='{6}', rating_grade='{7}', rating_score='{8}', " \
               "total_turnover='{9}', liquidity_grade='{10}', liquidity_score='{11}', maturity_years='{12}', " \
               "maturity_score='{13}', maturity_date='{14}', created_ts='{15}', created_by='{16}')>".\
            format(self.fund_code, self.security_isin, self.reporting_date, self.exposure, self.market_value,
                   self.rating_type, self.rating_symbol, self.rating_grade, self.rating_score, self.total_turnover,
                   self.liquidity_grade, self.liquidity_score, self.maturity_years, self.maturity_score,
                   self.maturity_date, self.created_ts, self.created_by)


class FundRating:
    def __init__(self):
        self.fund_code = None
        self.reporting_date = None
        self.current_aum = None
        self.nav_units = None
        self.nav_adj_aum_rating = None
        self.credit_risk_score = None
        self.liquidity_score = None
        self.maturity_score = None
        self.transition_score = None
        self.fund_score = None
        self.created_ts = None
        self.created_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_reporting_date(self, reporting_date=None):
        self.reporting_date = reporting_date

    def get_reporting_date(self):
        return self.reporting_date

    def set_current_aum(self, current_aum=None):
        self.current_aum = current_aum

    def get_current_aum(self):
        return self.current_aum

    def set_nav_units(self, nav_units=None):
        self.nav_units = nav_units

    def get_nav_units(self):
        return self.nav_units

    def set_nav_adj_aum_rating(self, nav_adj_aum_rating=None):
        self.nav_adj_aum_rating = nav_adj_aum_rating

    def get_nav_adj_aum_rating(self):
        return self.nav_adj_aum_rating

    def set_credit_risk_score(self, credit_risk_score=None):
        self.credit_risk_score = credit_risk_score

    def get_credit_risk_score(self):
        return self.credit_risk_score

    def set_liquidity_score(self, liquidity_score=None):
        self.liquidity_score = liquidity_score

    def get_liquidity_score(self):
        return self.liquidity_score

    def set_maturity_score(self, maturity_score=None):
        self.maturity_score = maturity_score

    def get_maturity_score(self):
        return self.maturity_score

    def set_transition_score(self, transition_score=None):
        self.transition_score = transition_score

    def get_transition_score(self):
        return self.transition_score

    def set_fund_score(self, fund_score=None):
        self.fund_score = fund_score

    def set_created_ts(self, created_ts=None):
        self.created_ts = created_ts

    def get_created_ts(self):
        return self.created_ts

    def set_created_by(self, created_by=None):
        self.created_by = created_by

    def get_created_by(self):
        return self.created_by

    def __repr__(self):
        return "<FundRating(fund_code='{0}', reporting_date='{1}', current_aum='{2}', nav_units='{3}', " \
               "nav_adj_aum_rating='{4}', credit_risk_score='{5}', liquidity_score='{6}', maturity_score='{7}', " \
               "transition_score='{8}', fund_score='{9}', created_ts='{10}', created_by='{11}')>".\
            format(self.fund_code, self.reporting_date, self.current_aum, self.nav_units, self.nav_adj_aum_rating,
                   self.credit_risk_score, self.liquidity_score, self.maturity_score, self.transition_score,
                   self.fund_score, self.created_ts, self.created_by)
