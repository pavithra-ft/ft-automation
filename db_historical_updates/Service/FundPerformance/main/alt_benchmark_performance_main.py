from config.basic_config import fund_code
from Service.FundPerformance.service.alt_benchmark_performance import get_alt_benchmark_performance


if __name__ == "__main__":
    fund_code_list = [fund_code[0]]
    get_alt_benchmark_performance(fund_code_list)
