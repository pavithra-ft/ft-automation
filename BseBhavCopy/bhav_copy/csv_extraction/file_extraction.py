from datetime import datetime
from bhav_copy.model.FwMasSecurities import MasSecurities


def get_bse_security_list(df):
    security_list = []
    for index, row in df.iterrows():
        equity_body = MasSecurities()
        equity_body.set_security_isin(row['ISIN No'].strip())
        if row['Security Name'].endswith("-$"):
            equity_body.set_security_name(row['Security Name'].replace("-$", " ").strip().upper())
        else:
            equity_body.set_security_name(row['Security Name'].strip().upper())
        equity_body.set_security_code(row['Security Code'].strip())
        equity_body.set_bse_security_symbol(row['Security Id'].strip())
        equity_body.set_is_active('1')
        security_list.append(equity_body)
    return security_list


def get_security_info(df):
    security_info = []
    for index, row in df.iterrows():
        security_body = MasSecurities()
        security_body.set_security_isin(row['ISIN_CODE'].strip())
        security_body.set_security_code(row['SC_CODE'].strip())
        security_body.set_bse_security_symbol(row['SC_NAME'].strip())
        security_body.set_bse_prev_close_price(row['PREVCLOSE'].strip())
        security_body.set_close_price_as_of(datetime.strptime(row['TRADING_DATE'], '%d-%b-%y').date())
        security_body.set_is_active('1')
        security_info.append(security_body)
    return security_info
