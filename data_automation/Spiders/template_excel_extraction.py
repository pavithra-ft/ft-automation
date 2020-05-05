def get_fund_info(df):
    fund_info = {"fund_name": df.iloc[2, 2],
                 "fund_code": df.iloc[3, 2],
                 "effective_end_date": df.iloc[4, 2],
                 "no_of_clients": df.iloc[5, 2],
                 "current_aum": df.iloc[6, 2],
                 "performance_1m": df.iloc[7, 2]
                 }
    return fund_info


def get_fund_allocation_values(df):
    fund_allocation = {}
    index = 13
    while df.iloc[index, 4] != "TOTAL":
        allocation = df.iloc[index, 4]
        fund_allocation[allocation] = df.iloc[index, 5]
        index += 1
    return fund_allocation


def get_market_cap_values(df):
    cap_data = {}
    index = 3
    while df.iloc[index, 4] != "TOTAL":
        market_cap = df.iloc[index, 4].replace(" Cap", "")
        type_market_cap = market_cap.capitalize()
        cap_data[type_market_cap] = df.iloc[index, 5]
        index += 1
    return cap_data


def get_fund_portfolio_values(df):
    portfolio_values = []
    index = 11
    while df.iloc[index, 2] != "nan":
        portfolio_body = {}
        portfolio_body.update({"security_name": df.iloc[index, 1]})
        portfolio_body.update({"exposure": df.iloc[index, 2]})
        portfolio_values.append(portfolio_body)
        index += 1
    return portfolio_values


def get_fund_sector_values(df):
    sector_values = []
    index = 21
    while df.iloc[index, 4] != "nan":
        sector_body = {}
        sector_body.update({"sector_name": df.iloc[index, 4]})
        sector_body.update({"exposure": df.iloc[index, 5]})
        sector_values.append(sector_body)
        index += 1
    return sector_values
