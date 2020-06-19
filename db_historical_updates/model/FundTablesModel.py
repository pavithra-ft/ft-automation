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
