class FundPerformance:
    def __init__(self):
        self.fund_code = None
        self.current_aum = None
        self.no_of_clients = None
        self.market_cap_type_code = None
        self.portfolio_equity_allocation = None
        self.portfolio_cash_allocation = None
        self.portfolio_asset_allocation = None
        self.portfolio_other_allocations = None
        self.perf_1m = None
        self.perf_3m = None
        self.perf_6m = None
        self.perf_1y = None
        self.perf_2y = None
        self.perf_3y = None
        self.perf_5y = None
        self.perf_inception = None
        self.isLatest = None
        self.effective_start_date = None
        self.effective_end_date = None
        self.created_ts = None
        self.created_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_current_aum(self, current_aum=None):
        self.current_aum = current_aum

    def get_current_aum(self):
        return self.current_aum

    def set_no_of_clients(self, no_of_clients=None):
        self.no_of_clients = no_of_clients

    def get_no_of_clients(self):
        return self.no_of_clients

    def set_market_cap_type_code(self, market_cap_type_code=None):
        self.market_cap_type_code = market_cap_type_code

    def get_market_cap_type_code(self):
        return self.market_cap_type_code

    def set_portfolio_equity_allocation(self, portfolio_equity_allocation=None):
        self.portfolio_equity_allocation = portfolio_equity_allocation

    def get_portfolio_equity_allocation(self):
        return self.portfolio_equity_allocation

    def set_portfolio_cash_allocation(self, portfolio_cash_allocation=None):
        self.portfolio_cash_allocation = portfolio_cash_allocation

    def get_portfolio_cash_allocation(self):
        return self.portfolio_cash_allocation

    def set_portfolio_asset_allocation(self, portfolio_asset_allocation=None):
        self.portfolio_asset_allocation = portfolio_asset_allocation

    def get_portfolio_asset_allocation(self):
        return self.portfolio_asset_allocation

    def set_portfolio_other_allocations(self, portfolio_other_allocations=None):
        self.portfolio_other_allocations = portfolio_other_allocations

    def get_portfolio_other_allocations(self):
        return self.portfolio_other_allocations

    def set_perf_1m(self, perf_1m=None):
        self.perf_1m = perf_1m

    def get_perf_1m(self):
        return self.perf_1m

    def set_perf_3m(self, perf_3m=None):
        self.perf_3m = perf_3m

    def get_perf_3m(self):
        return self.perf_3m

    def set_perf_6m(self, perf_6m=None):
        self.perf_6m = perf_6m

    def get_perf_6m(self):
        return self.perf_6m

    def set_perf_1y(self, perf_1y=None):
        self.perf_1y = perf_1y

    def get_perf_1y(self):
        return self.perf_1y

    def set_perf_2y(self, perf_2y=None):
        self.perf_2y = perf_2y

    def get_perf_2y(self):
        return self.perf_2y

    def set_perf_3y(self, perf_3y=None):
        self.perf_3y = perf_3y

    def get_perf_3y(self):
        return self.perf_3y

    def set_perf_5y(self, perf_5y=None):
        self.perf_5y = perf_5y

    def get_perf_5y(self):
        return self.perf_5y

    def set_perf_inception(self, perf_inception=None):
        self.perf_inception = perf_inception

    def get_perf_inception(self):
        return self.perf_inception

    def set_isLatest(self, isLatest=None):
        self.isLatest = isLatest

    def get_isLatest(self):
        return self.isLatest

    def set_effective_start_date(self, effective_start_date=None):
        self.effective_start_date = effective_start_date

    def get_effective_start_date(self):
        return self.effective_start_date

    def set_effective_end_date(self, effective_end_date=None):
        self.effective_end_date = effective_end_date

    def get_effective_end_date(self):
        return self.effective_end_date

    def set_created_ts(self, created_ts=None):
        self.created_ts = created_ts

    def get_created_ts(self):
        return self.created_ts

    def set_created_by(self, created_by=None):
        self.created_by = created_by

    def get_created_by(self):
        return self.created_by

    def __repr__(self):
        return "<FundPerformance(fund_code='{0}', current_aum='{1}', no_of_clients='{2}', market_cap_type_code='{3}'," \
               " portfolio_equity_allocation='{4}', portfolio_cash_allocation='{5}', portfolio_asset_allocation='{6}'" \
               ", portfolio_other_allocations='{7}', perf_1m='{8}', perf_3m='{9}', perf_6m='{10}', perf_1y='{11}', " \
               "perf_2y='{12}', perf_3y='{13}', perf_5y='{14}', perf_inception='{15}', isLatest='{16}', " \
               "effective_start_date='{17}', effective_end_date='{18}', created_ts='{19}', created_by='{20}')>". \
            format(self.fund_code, self.current_aum, self.no_of_clients, self.market_cap_type_code,
                   self.portfolio_equity_allocation, self.portfolio_cash_allocation, self.portfolio_asset_allocation,
                   self.portfolio_other_allocations, self.perf_1m, self.perf_3m, self.perf_6m, self.perf_1y,
                   self.perf_2y, self.perf_3y, self.perf_5y, self.perf_inception, self.isLatest,
                   self.effective_start_date, self.effective_end_date, self.created_ts, self.created_by)
