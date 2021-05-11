class IndexPerformance:
    def __init__(self):
        self.index_code = None
        self.standard_deviation = None
        self.pe_ratio = None
        self.top_sector_name = None
        self.top_sector_exposure = None
        self.top_holding_isin = None
        self.top_holding_exposure = None
        self.perf_1m = None
        self.perf_3m = None
        self.perf_6m = None
        self.perf_1y = None
        self.perf_2y = None
        self.perf_3y = None
        self.perf_5y = None
        self.perf_inception = None
        self.reporting_date = None

    def set_index_code(self, index_code=None):
        self.index_code = index_code

    def get_index_code(self):
        return self.index_code

    def set_standard_deviation(self, standard_deviation=None):
        self.standard_deviation = standard_deviation

    def get_standard_deviation(self):
        return self.standard_deviation

    def set_pe_ratio(self, pe_ratio=None):
        self.pe_ratio = pe_ratio

    def get_pe_ratio(self):
        return self.pe_ratio

    def set_top_sector_name(self, top_sector_name=None):
        self.top_sector_name = top_sector_name

    def get_top_sector_name(self):
        return self.top_sector_name

    def set_top_sector_exposure(self, top_sector_exposure=None):
        self.top_sector_exposure = top_sector_exposure

    def get_top_sector_exposure(self):
        return self.top_sector_exposure

    def set_top_holding_isin(self, top_holding_isin=None):
        self.top_holding_isin = top_holding_isin

    def get_top_holding_isin(self):
        return self.top_holding_isin

    def set_top_holding_exposure(self, top_holding_exposure=None):
        self.top_holding_exposure = top_holding_exposure

    def get_top_holding_exposure(self):
        return self.top_holding_exposure

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

    def set_reporting_date(self, reporting_date=None):
        self.reporting_date = reporting_date

    def get_reporting_date(self):
        return self.reporting_date

    def __repr__(self):
        return "<IndexPerformance(index_code='{0}', standard_deviation='{1}', pe_ratio='{2}', top_sector_name='{3}'," \
               " top_sector_exposure='{4}', top_holding_isin='{5}', top_holding_exposure='{6}', perf_1m='{7}', " \
               "perf_3m='{8}', perf_6m='{9}', perf_1y='{10}', perf_2y='{11}', perf_3y='{12}', perf_5y='{13}', " \
               "perf_inception='{14}', reporting_date='{15}')>". \
            format(self.index_code, self.standard_deviation, self.pe_ratio, self.top_sector_name,
                   self.top_sector_exposure, self.top_holding_isin, self.top_holding_exposure, self.perf_1m,
                   self.perf_3m, self.perf_6m, self.perf_1y, self.perf_2y, self.perf_3y, self.perf_5y,
                   self.perf_inception, self.reporting_date)
