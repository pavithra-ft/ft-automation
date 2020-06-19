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


class FundMarketCapDetails:
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
