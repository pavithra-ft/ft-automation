class FundInfo:
    def __init__(self):
        self.fund_code = None
        self.fund_name = None
        self.reporting_date = None
        self.no_of_clients = None
        self.current_aum = None
        self.performance_1m = None
        self.market_cap_type_code = None

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

    def set_no_of_clients(self, no_of_clients=None):
        self.no_of_clients = no_of_clients

    def get_no_of_clients(self):
        return self.no_of_clients

    def set_current_aum(self, current_aum=None):
        self.current_aum = current_aum

    def get_current_aum(self):
        return self.current_aum

    def set_performance_1m(self, performance_1m=None):
        self.performance_1m = performance_1m

    def get_performance_1m(self):
        return self.performance_1m

    def set_market_cap_type_code(self, market_cap_type_code=None):
        self.market_cap_type_code = market_cap_type_code

    def get_market_cap_type_code(self):
        return self.market_cap_type_code

    def __repr__(self):
        return "<FundInfo(fund_code='{0}', fund_name='{1}', reporting_date='{2}', no_of_clients='{3}', " \
               "current_aum='{4}', performance_1m='{5}', market_cap_type_code='{6}')>".format(
                self.fund_code, self.fund_name, self.reporting_date, self.no_of_clients, self.current_aum,
                self.performance_1m, self.market_cap_type_code)


class FundAllocation:
    def __init__(self):
        self.allocation = None
        self.exposure = None

    def set_allocation(self, allocation=None):
        self.allocation = allocation

    def get_allocation(self):
        return self.allocation

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def __repr__(self):
        return "<FundAllocation(allocation='{0}', exposure='{1}')>".format(self.allocation, self.exposure)


class FundMarketCap:
    def __init__(self):
        self.type_market_cap = None
        self.exposure = None

    def set_type_market_cap(self, type_market_cap=None):
        self.type_market_cap = type_market_cap

    def get_type_market_cap(self):
        return self.type_market_cap

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def __repr__(self):
        return "<FundMarketCap(type_market_cap='{0}', exposure='{1}')>".format(self.type_market_cap, self.exposure)


class FundPortfolio:
    def __init__(self):
        self.security_name = None
        self.exposure = None

    def set_security_name(self, security_name=None):
        self.security_name = security_name

    def get_security_name(self):
        return self.security_name

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def __repr__(self):
        return "<FundPortfolio(security_name='{0}', exposure='{1}')>".format(self.security_name, self.exposure)


class FundSector:
    def __init__(self):
        self.sector_name = None
        self.exposure = None

    def set_sector_name(self, sector_name=None):
        self.sector_name = sector_name

    def get_sector_name(self):
        return self.sector_name

    def set_exposure(self, exposure=None):
        self.exposure = exposure

    def get_exposure(self):
        return self.exposure

    def __repr__(self):
        return "<FundSector(sector_name='{0}', exposure='{1}')>".format(self.sector_name, self.exposure)
