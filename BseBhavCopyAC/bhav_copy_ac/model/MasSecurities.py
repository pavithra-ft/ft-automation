class MasSecurities:
    def __init__(self):
        self.security_isin = None
        self.security_name = None
        self.security_code = None
        self.bse_security_symbol = None
        self.nse_security_symbol = None
        self.industry = None
        self.share_class_type = None
        self.bse_group = None
        self.bse_prev_close_price = None
        self.nse_prev_close_price = None
        self.close_price_as_of = None
        self.is_active = None

    def set_security_isin(self, security_isin=None):
        self.security_isin = security_isin

    def get_security_isin(self):
        return self.security_isin

    def set_security_name(self, security_name=None):
        self.security_name = security_name

    def get_security_name(self):
        return self.security_name

    def set_security_code(self, security_code=None):
        self.security_code = security_code

    def get_security_code(self):
        return self.security_code

    def set_bse_security_symbol(self, bse_security_symbol=None):
        self.bse_security_symbol = bse_security_symbol

    def get_bse_security_symbol(self):
        return self.bse_security_symbol

    def set_nse_security_symbol(self, nse_security_symbol=None):
        self.nse_security_symbol = nse_security_symbol

    def get_nse_security_symbol(self):
        return self.nse_security_symbol

    def set_industry(self, industry=None):
        self.industry = industry

    def get_industry(self):
        return self.industry

    def set_share_class_type(self, share_class_type=None):
        self.share_class_type = share_class_type

    def get_share_class_type(self):
        return self.share_class_type

    def set_bse_group(self, bse_group=None):
        self.bse_group = bse_group

    def get_bse_group(self):
        return self.bse_group

    def set_bse_prev_close_price(self, bse_prev_close_price=None):
        self.bse_prev_close_price = bse_prev_close_price

    def get_bse_prev_close_price(self):
        return self.bse_prev_close_price

    def set_nse_prev_close_price(self, nse_prev_close_price=None):
        self.nse_prev_close_price = nse_prev_close_price

    def get_nse_prev_close_price(self):
        return self.nse_prev_close_price

    def set_close_price_as_of(self, close_price_as_of=None):
        self.close_price_as_of = close_price_as_of

    def get_close_price_as_of(self):
        return self.close_price_as_of

    def set_is_active(self, is_active=None):
        self.is_active = is_active

    def get_is_active(self):
        return self.is_active

    def __repr__(self):
        return "<MasSecurities(security_isin='{0}', security_name='{1}', security_code='{2}', " \
               "bse_security_symbol='{3}', nse_security_symbol='{4}', industry='{5}', share_class_type='{6}'," \
               "bse_group='{7}', bse_prev_close_price='{8}', nse_prev_close_price='{9}', close_price_as_of='{10}', " \
               "is_active='{11}')>". \
            format(self.security_isin, self.security_name, self.security_code, self.bse_security_symbol,
                   self.nse_security_symbol, self.industry, self.share_class_type, self.bse_group,
                   self.bse_prev_close_price, self.nse_prev_close_price, self.close_price_as_of, self.is_active)
