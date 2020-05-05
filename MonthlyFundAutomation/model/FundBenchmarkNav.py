class FundBenchmarkNav:
    def __init__(self):
        self.fund_code = None
        self.benchmark_index_code = None
        self.alt_benchmark_index_code = None
        self.fund_nav = None
        self.benchmark_nav = None
        self.alt_benchmark_nav = None
        self.effective_end_date = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_benchmark_index_code(self, benchmark_index_code=None):
        self.benchmark_index_code = benchmark_index_code

    def get_benchmark_index_code(self):
        return self.benchmark_index_code

    def set_alt_benchmark_index_code(self, alt_benchmark_index_code=None):
        self.alt_benchmark_index_code = alt_benchmark_index_code

    def get_alt_benchmark_index_code(self):
        return self.alt_benchmark_index_code

    def set_fund_nav(self, fund_nav=None):
        self.fund_nav = fund_nav

    def get_fund_nav(self):
        return self.fund_nav

    def set_benchmark_nav(self, benchmark_nav=None):
        self.benchmark_nav = benchmark_nav

    def get_benchmark_nav(self):
        return self.benchmark_nav

    def set_alt_benchmark_nav(self, alt_benchmark_nav=None):
        self.alt_benchmark_nav = alt_benchmark_nav

    def get_alt_benchmark_nav(self):
        return self.alt_benchmark_nav

    def set_effective_end_date(self, effective_end_date=None):
        self.effective_end_date = effective_end_date

    def get_effective_end_date(self):
        return self.effective_end_date

    def __repr__(self):
        return "<FundBenchmarkNav(fund_code='{0}', benchmark_index_code='{1}', alt_benchmark_index_code='{2}', " \
               "fund_nav='{3}', benchmark_nav='{4}', alt_benchmark_nav='{5}', effective_end_date='{6}')>".\
            format(self.fund_code, self.benchmark_index_code, self.alt_benchmark_index_code, self.fund_nav,
                   self.benchmark_nav, self.alt_benchmark_nav, self.effective_end_date)
