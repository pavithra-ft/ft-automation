class FundMarketCap:
    def __init__(self):
        self.fund_code = None
        self.type_market_cap = None
        self.exposure = None
        self.start_date = None
        self.end_date = None
        self.created_ts = None
        self.action_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_type_market_cap(self, type_market_cap=None):
        self.type_market_cap = type_market_cap

    def get_type_market_cap(self):
        return self.type_market_cap

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def set_start_date(self, start_date=None):
        self.start_date = start_date

    def get_start_date(self):
        return self.start_date

    def set_end_date(self, end_date=None):
        self.end_date = end_date

    def get_end_date(self):
        return self.end_date

    def set_created_ts(self, created_ts=None):
        self.created_ts = created_ts

    def get_created_ts(self):
        return self.created_ts

    def set_action_by(self, action_by=None):
        self.action_by = action_by

    def get_action_by(self):
        return self.action_by

    def __repr__(self):
        return "<FundMarketCap(fund_code='{0}', type_market_cap='{1}', exposure='{2}', start_date='{3}', " \
               "end_date='{4}', created_ts='{5}', action_by='{6}')>".format(self.fund_code, self.type_market_cap,
                                                                            self.exposure, self.start_date,
                                                                            self.end_date, self.created_ts,
                                                                            self.action_by)
