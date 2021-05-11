from Service.FundBenchmarkNav.service.benchmark_nav import get_benchmark_nav
from config.basic_config import fund_code

if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_benchmark_nav(fund_code_list)
