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


class FundPerformance:
    def __init__(self):
        self.fund_code = None
        self.current_aum = None
        self.no_of_clients = None
        self.market_cap_type_code = None
        self.investment_style_type_code = None
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

    def set_investment_style_type_code(self, investment_style_type_code=None):
        self.investment_style_type_code = investment_style_type_code

    def get_investment_style_type_code(self):
        return self.investment_style_type_code

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
               " investment_style_type_code='{4}', portfolio_equity_allocation='{5}', portfolio_cash_allocation='{6}'" \
               ", portfolio_asset_allocation='{7}', portfolio_other_allocations='{8}', perf_1m='{9}', perf_3m='{10}'," \
               " perf_6m='{11}', perf_1y='{12}', perf_2y='{13}', perf_3y='{14}', perf_5y='{15}', perf_inception='{16}" \
               "', isLatest='{17}', effective_start_date='{18}', effective_end_date='{19}', created_ts='{20}', " \
               "created_by='{21}')>". \
            format(self.fund_code, self.current_aum, self.no_of_clients, self.market_cap_type_code,
                   self.investment_style_type_code, self.portfolio_equity_allocation, self.portfolio_cash_allocation,
                   self.portfolio_asset_allocation, self.portfolio_other_allocations, self.perf_1m, self.perf_3m,
                   self.perf_6m, self.perf_1y, self.perf_2y, self.perf_3y, self.perf_5y, self.perf_inception,
                   self.isLatest, self.effective_start_date, self.effective_end_date, self.created_ts, self.created_by)


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
               "benchmark_perf_5y='{7}', benchmark_perf_inception='{8}')>".\
            format(self.benchmark_index_code, self.benchmark_perf_1m, self.benchmark_perf_3m, self.benchmark_perf_6m,
                   self.benchmark_perf_1y, self.benchmark_perf_2y, self.benchmark_perf_3y, self.benchmark_perf_5y,
                   self.benchmark_perf_inception)


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
               "alt_benchmark_perf_inception='{8}')>".\
            format(self.alt_benchmark_index_code, self.alt_benchmark_perf_1m, self.alt_benchmark_perf_3m,
                   self.alt_benchmark_perf_6m, self.alt_benchmark_perf_1y, self.alt_benchmark_perf_2y,
                   self.alt_benchmark_perf_3y, self.alt_benchmark_perf_5y, self.alt_benchmark_perf_inception)


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
               "end_date='{4}', created_ts='{5}', action_by='{6}')>".\
            format(self.fund_code, self.type_market_cap, self.exposure, self.start_date, self.end_date, self.created_ts,
                   self.action_by)


class FundPortfolio:
    def __init__(self):
        self.fund_code = None
        self.security_isin = None
        self.exposure = None
        self.start_date = None
        self.end_date = None
        self.created_ts = None
        self.action_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_security_isin(self, security_isin=None):
        self.security_isin = security_isin

    def get_security_isin(self):
        return self.security_isin

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
        return "<FundPortfolio(fund_code='{0}', security_isin='{1}', exposure='{2}', start_date='{3}', " \
               "end_date='{4}', created_ts='{5}', action_by='{6}')>".\
            format(self.fund_code, self.security_isin, self.exposure, self.start_date, self.end_date, self.created_ts,
                   self.action_by)


class FundSector:
    def __init__(self):
        self.fund_code = None
        self.sector_type_name = None
        self.exposure = None
        self.start_date = None
        self.end_date = None
        self.created_ts = None
        self.action_by = None

    def set_fund_code(self, fund_code=None):
        self.fund_code = fund_code

    def get_fund_code(self):
        return self.fund_code

    def set_sector_type_name(self, sector_type_name=None):
        self.sector_type_name = sector_type_name

    def get_sector_type_name(self):
        return self.sector_type_name

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
        return "<FundSector(fund_code='{0}', sector_type_name='{1}', exposure='{2}', start_date='{3}', " \
               "end_date='{4}', created_ts='{5}', action_by='{6}')>".\
            format(self.fund_code, self.sector_type_name, self.exposure, self.start_date, self.end_date,
                   self.created_ts, self.action_by)


class FundRatios:
    def __init__(self):
        self.fund_code = None
        self.reporting_date = None
        self.full_pe_ratio = None
        self.top5_pe_ratio = None
        self.top10_pe_ratio = None
        self.full_market_cap = None
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

    def set_full_pe_ratio(self, full_pe_ratio=None):
        self.full_pe_ratio = full_pe_ratio

    def get_full_pe_ratio(self):
        return self.full_pe_ratio

    def set_top5_pe_ratio(self, top5_pe_ratio=None):
        self.top5_pe_ratio = top5_pe_ratio

    def get_top5_pe_ratio(self):
        return self.top5_pe_ratio

    def set_top10_pe_ratio(self, top10_pe_ratio=None):
        self.top10_pe_ratio = top10_pe_ratio

    def get_top10_pe_ratio(self):
        return self.top10_pe_ratio

    def set_full_market_cap(self, full_market_cap=None):
        self.full_market_cap = full_market_cap

    def get_full_market_cap(self):
        return self.full_market_cap

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
               "updated_by='{13}')>".\
            format(self.fund_code, self.reporting_date, self.top5_pe_ratio, self.top10_pe_ratio, self.top5_market_cap,
                   self.top10_market_cap, self.standard_deviation, self.median, self.sigma, self.sortino_ratio,
                   self.negative_excess_returns_risk_free, self.fund_alpha, self.updated_ts, self.updated_by)


class Collaterals:
    def __init__(self):
        self.collateral_code = None
        self.view_code = None
        self.collateral_type_code = None
        self.entity_type = None
        self.entity_code = None
        self.collateral_title = None
        self.visibility_code = None
        self.template_code = None
        self.collateral_date = None
        self.collateral_status = None
        self.reporting_date = None
        self.effective_start_date = None
        self.is_premium = None
        self.is_published = None
        self.is_data_changed = None
        self.published_ts = None
        self.created_ts = None
        self.created_by = None

    def set_collateral_code(self, collateral_code=None):
        self.collateral_code = collateral_code

    def get_collateral_code(self):
        return self.collateral_code

    def set_view_code(self, view_code=None):
        self.view_code = view_code

    def get_view_code(self):
        return self.view_code

    def set_collateral_type_code(self, collateral_type_code=None):
        self.collateral_type_code = collateral_type_code

    def get_collateral_type_code(self):
        return self.collateral_type_code

    def set_entity_type(self, entity_type=None):
        self.entity_type = entity_type

    def get_entity_type(self):
        return self.entity_type

    def set_entity_code(self, entity_code=None):
        self.entity_code = entity_code

    def get_entity_code(self):
        return self.entity_code

    def set_collateral_title(self, collateral_title=None):
        self.collateral_title = collateral_title

    def get_collateral_title(self):
        return self.collateral_title

    def set_visibility_code(self, visibility_code=None):
        self.visibility_code = visibility_code

    def get_visibility_code(self):
        return self.visibility_code

    def set_template_code(self, template_code=None):
        self.template_code = template_code

    def get_template_code(self):
        return self.template_code

    def set_collateral_date(self, collateral_date=None):
        self.collateral_date = collateral_date

    def get_collateral_date(self):
        return self.collateral_date

    def set_collateral_status(self, collateral_status=None):
        self.collateral_status = collateral_status

    def get_collateral_status(self):
        return self.collateral_status

    def set_reporting_date(self, reporting_date=None):
        self.reporting_date = reporting_date

    def get_reporting_date(self):
        return self.reporting_date

    def set_effective_start_date(self, effective_start_date=None):
        self.effective_start_date = effective_start_date

    def get_effective_start_date(self):
        return self.effective_start_date

    def set_is_premium(self, is_premium=None):
        self.is_premium = is_premium

    def get_is_premium(self):
        return self.is_premium

    def set_is_published(self, is_published=None):
        self.is_published = is_published

    def get_is_published(self):
        return self.is_published

    def set_is_data_changed(self, is_data_changed=None):
        self.is_data_changed = is_data_changed

    def get_is_data_changed(self):
        return self.is_data_changed

    def set_published_ts(self, published_ts=None):
        self.published_ts = published_ts

    def get_published_ts(self):
        return self.published_ts

    def set_created_ts(self, created_ts=None):
        self.created_ts = created_ts

    def get_created_ts(self):
        return self.created_ts

    def set_created_by(self, created_by=None):
        self.created_by = created_by

    def get_created_by(self):
        return self.created_by

    def __repr__(self):
        return "<Collaterals(collateral_code='{0}', view_code='{1}', collateral_type_code='{2}', entity_type='{3}', " \
               "entity_code='{4}', collateral_title='{5}', visibility_code='{6}', template_code='{7}', " \
               "collateral_date='{8}', collateral_status='{9}', reporting_date='{10}', effective_start_date='{11}', " \
               "is_premium='{12}', is_published='{13}', is_data_changed='{14}', published_ts='{15}', " \
               "created_ts='{16}', created_by='{17}')>". \
            format(self.collateral_code, self.view_code, self.collateral_type_code, self.entity_type, self.entity_code,
                   self.collateral_title, self.visibility_code, self.template_code, self.collateral_date,
                   self.collateral_status, self.reporting_date, self.effective_start_date, self.is_premium,
                   self.is_published, self.is_data_changed, self.published_ts, self.created_ts, self.created_by)
