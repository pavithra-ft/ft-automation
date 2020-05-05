class FundRatios:
    def __init__(self):
        self.fund_code = None
        self.reporting_date = None
        self.top5_pe_ratio = None
        self.top10_pe_ratio = None
        self.top5_market_cap = None
        self.top10_market_cap = None
        self.standard_deviation = None
        self.median = None
        self.sigma = None
        self.sortino_ratio = None
        self.negative_excess_returns_risk_free = None
        self.fund_alpha = None
        self.updated_ts = None
        self.updated_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_reporting_date(self, reporting_date=None):
        self.reporting_date = reporting_date

    def get_reporting_date(self):
        return self.reporting_date

    def set_top5_pe_ratio(self, top5_pe_ratio=None):
        self.top5_pe_ratio = top5_pe_ratio

    def get_top5_pe_ratio(self):
        return self.top5_pe_ratio

    def set_top10_pe_ratio(self, top10_pe_ratio=None):
        self.top10_pe_ratio = top10_pe_ratio

    def get_top10_pe_ratio(self):
        return self.top10_pe_ratio

    def set_top5_market_cap(self, top5_market_cap=None):
        self.top5_market_cap = top5_market_cap

    def get_top5_market_cap(self):
        return self.top5_market_cap

    def set_top10_market_cap(self, top10_market_cap=None):
        self.top10_market_cap = top10_market_cap

    def get_top10_market_cap(self):
        return self.top10_market_cap

    def set_standard_deviation(self, standard_deviation=None):
        self.standard_deviation = standard_deviation

    def get_standard_deviation(self):
        return self.standard_deviation

    def set_median(self, median=None):
        self.median = median

    def get_median(self):
        return self.median

    def set_sigma(self, sigma=None):
        self.sigma = sigma

    def get_sigma(self):
        return self.sigma

    def set_sortino_ratio(self, sortino_ratio=None):
        self.sortino_ratio = sortino_ratio

    def get_sortino_ratio(self):
        return self.sortino_ratio

    def set_negative_excess_returns_risk_free(self, negative_excess_returns_risk_free=None):
        self.negative_excess_returns_risk_free = negative_excess_returns_risk_free

    def get_negative_excess_returns_risk_free(self):
        return self.negative_excess_returns_risk_free

    def set_fund_alpha(self, fund_alpha=None):
        self.fund_alpha = fund_alpha

    def get_fund_alpha(self):
        return self.fund_alpha

    def set_updated_ts(self, updated_ts=None):
        self.updated_ts = updated_ts

    def get_updated_ts(self):
        return self.updated_ts

    def set_updated_by(self, updated_by=None):
        self.updated_by = updated_by

    def get_updated_by(self):
        return self.updated_by

    def __repr__(self):
        return "<FundRatios(fund_code='{0}', reporting_date='{1}', top5_pe_ratio='{2}', top10_pe_ratio='{3}', " \
               "top5_market_cap='{4}', top10_market_cap='{5}', standard_deviation='{6}', median='{7}', sigma='{8}', " \
               "sortino_ratio='{9}', negative_excess_returns_risk_free='{10}', fund_alpha='{11}', updated_ts='{12}', " \
               "updated_by='{13}')>".format(self.fund_code, self.reporting_date, self.top5_pe_ratio,
                                            self.top10_pe_ratio, self.top5_market_cap, self.top10_market_cap,
                                            self.standard_deviation, self.median, self.sigma, self.sortino_ratio,
                                            self.negative_excess_returns_risk_free, self.fund_alpha, self.updated_ts,
                                            self.updated_by)
