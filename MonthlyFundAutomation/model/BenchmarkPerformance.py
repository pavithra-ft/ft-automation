class BenchmarkPerformance:
    def __init__(self):
        self.benchmark_index_code = None
        self.benchmark_perf_1m = None
        self.benchmark_perf_3m = None
        self.benchmark_perf_6m = None
        self.benchmark_perf_1y = None
        self.benchmark_perf_2y = None
        self.benchmark_perf_3y = None
        self.benchmark_perf_5y = None
        self.benchmark_perf_inception = None

    def set_benchmark_index_code(self, benchmark_index_code=None):
        self.benchmark_index_code = benchmark_index_code

    def get_benchmark_index_code(self):
        return self.benchmark_index_code

    def set_benchmark_perf_1m(self, benchmark_perf_1m=None):
        self.benchmark_perf_1m = benchmark_perf_1m

    def get_benchmark_perf_1m(self):
        return self.benchmark_perf_1m

    def set_benchmark_perf_3m(self, benchmark_perf_3m=None):
        self.benchmark_perf_3m = benchmark_perf_3m

    def get_benchmark_perf_3m(self):
        return self.benchmark_perf_3m

    def set_benchmark_perf_6m(self, benchmark_perf_6m=None):
        self.benchmark_perf_6m = benchmark_perf_6m

    def get_benchmark_perf_6m(self):
        return self.benchmark_perf_6m

    def set_benchmark_perf_1y(self, benchmark_perf_1y=None):
        self.benchmark_perf_1y = benchmark_perf_1y

    def get_benchmark_perf_1y(self):
        return self.benchmark_perf_1y

    def set_benchmark_perf_2y(self, benchmark_perf_2y=None):
        self.benchmark_perf_2y = benchmark_perf_2y

    def get_benchmark_perf_2y(self):
        return self.benchmark_perf_2y

    def set_benchmark_perf_3y(self, benchmark_perf_3y=None):
        self.benchmark_perf_3y = benchmark_perf_3y

    def get_benchmark_perf_3y(self):
        return self.benchmark_perf_3y

    def set_benchmark_perf_5y(self, benchmark_perf_5y=None):
        self.benchmark_perf_5y = benchmark_perf_5y

    def get_benchmark_perf_5y(self):
        return self.benchmark_perf_5y

    def set_benchmark_perf_inception(self, benchmark_perf_inception=None):
        self.benchmark_perf_inception = benchmark_perf_inception

    def get_benchmark_perf_inception(self):
        return self.benchmark_perf_inception

    def __repr__(self):
        return "<BenchmarkPerformance(benchmark_index_code='{0}', benchmark_perf_1m='{1}', benchmark_perf_3m='{2}', " \
               "benchmark_perf_6m='{3}', benchmark_perf_1y='{4}', benchmark_perf_2y='{5}', benchmark_perf_3y='{6}', " \
               "benchmark_perf_5y='{7}', benchmark_perf_inception='{8}')>".format(self.benchmark_index_code,
                                                                                  self.benchmark_perf_1m,
                                                                                  self.benchmark_perf_3m,
                                                                                  self.benchmark_perf_6m,
                                                                                  self.benchmark_perf_1y,
                                                                                  self.benchmark_perf_2y,
                                                                                  self.benchmark_perf_3y,
                                                                                  self.benchmark_perf_5y,
                                                                                  self.benchmark_perf_inception)
