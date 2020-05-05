class AlternateBenchmarkPerformance:
    def __init__(self):
        self.alt_benchmark_index_code = None
        self.alt_benchmark_perf_1m = None
        self.alt_benchmark_perf_3m = None
        self.alt_benchmark_perf_6m = None
        self.alt_benchmark_perf_1y = None
        self.alt_benchmark_perf_2y = None
        self.alt_benchmark_perf_3y = None
        self.alt_benchmark_perf_5y = None
        self.alt_benchmark_perf_inception = None

    def set_alt_benchmark_index_code(self, alt_benchmark_index_code=None):
        self.alt_benchmark_index_code = alt_benchmark_index_code

    def get_alt_benchmark_index_code(self):
        return self.alt_benchmark_index_code

    def set_alt_benchmark_perf_1m(self, alt_benchmark_perf_1m=None):
        self.alt_benchmark_perf_1m = alt_benchmark_perf_1m

    def get_alt_benchmark_perf_1m(self):
        return self.alt_benchmark_perf_1m

    def set_alt_benchmark_perf_3m(self, alt_benchmark_perf_3m=None):
        self.alt_benchmark_perf_3m = alt_benchmark_perf_3m

    def get_alt_benchmark_perf_3m(self):
        return self.alt_benchmark_perf_3m

    def set_alt_benchmark_perf_6m(self, alt_benchmark_perf_6m=None):
        self.alt_benchmark_perf_6m = alt_benchmark_perf_6m

    def get_alt_benchmark_perf_6m(self):
        return self.alt_benchmark_perf_6m

    def set_alt_benchmark_perf_1y(self, alt_benchmark_perf_1y=None):
        self.alt_benchmark_perf_1y = alt_benchmark_perf_1y

    def get_alt_benchmark_perf_1y(self):
        return self.alt_benchmark_perf_1y

    def set_alt_benchmark_perf_2y(self, alt_benchmark_perf_2y=None):
        self.alt_benchmark_perf_2y = alt_benchmark_perf_2y

    def get_alt_benchmark_perf_2y(self):
        return self.alt_benchmark_perf_2y

    def set_alt_benchmark_perf_3y(self, alt_benchmark_perf_3y=None):
        self.alt_benchmark_perf_3y = alt_benchmark_perf_3y

    def get_alt_benchmark_perf_3y(self):
        return self.alt_benchmark_perf_3y

    def set_alt_benchmark_perf_5y(self, alt_benchmark_perf_5y=None):
        self.alt_benchmark_perf_5y = alt_benchmark_perf_5y

    def get_alt_benchmark_perf_5y(self):
        return self.alt_benchmark_perf_5y

    def set_alt_benchmark_perf_inception(self, alt_benchmark_perf_inception=None):
        self.alt_benchmark_perf_inception = alt_benchmark_perf_inception

    def get_alt_benchmark_perf_inception(self):
        return self.alt_benchmark_perf_inception

    def __repr__(self):
        return "<AlternateBenchmarkPerformance(alt_benchmark_index_code='{0}', alt_benchmark_perf_1m='{1}', " \
               "alt_benchmark_perf_3m='{2}', alt_benchmark_perf_6m='{3}', alt_benchmark_perf_1y='{4}', " \
               "alt_benchmark_perf_2y='{5}', alt_benchmark_perf_3y='{6}', alt_benchmark_perf_5y='{7}', " \
               "alt_benchmark_perf_inception='{8}')>".format(self.alt_benchmark_index_code, self.alt_benchmark_perf_1m,
                                                             self.alt_benchmark_perf_3m, self.alt_benchmark_perf_6m,
                                                             self.alt_benchmark_perf_1y, self.alt_benchmark_perf_2y,
                                                             self.alt_benchmark_perf_3y, self.alt_benchmark_perf_5y,
                                                             self.alt_benchmark_perf_inception)
