def get_fund_info(df):
    # Extraction of Fund attributes
    fund_info = {"fund_name": df.iloc[2, 2],
                 "fund_code": df.iloc[3, 2],
                 "reporting_date": df.iloc[4, 2],
                 "no_of_clients": df.iloc[5, 2],
                 "current_aum": df.iloc[6, 2],
                 "performance_1m": float(df.iloc[7, 2]),
                 "market_cap_type_code": df.iloc[8, 2],
                 "investment_style": df.iloc[9, 2]}
    return fund_info


def get_fund_allocation_values(df):
    # Extraction of Fund allocations
    fund_allocation = {}
    index = 15
    while df.iloc[index, 4] != "TOTAL":
        allocation = df.iloc[index, 4]
        fund_allocation[allocation] = df.iloc[index, 5]
        index += 1
    return fund_allocation


def get_market_cap_values(df):
    # Extraction of Market capitalization
    cap_data = {}
    index = 3
    while df.iloc[index, 4] != "TOTAL":
        market_cap = df.iloc[index, 4].replace(" Cap", "")
        type_market_cap = market_cap.capitalize()
        exposure = df.iloc[index, 5]
        if exposure is not None:
            cap_data[type_market_cap] = float(exposure)
        index += 1
    return cap_data


def get_fund_portfolio_values(df):
    # Extraction of Fund portfolio
    portfolio_values = []
    index = 13
    while df.iloc[index, 1] is not None:
        portfolio_body = {}
        portfolio_body.update({"security_name": df.iloc[index, 1]})
        exposure = df.iloc[index, 2]
        if exposure is None:
            portfolio_body.update({"exposure": 0})
        else:
            portfolio_body.update({"exposure": float(exposure)})
        portfolio_values.append(portfolio_body)
        index += 1
    return portfolio_values


def get_fund_sector_values(df):
    # Extraction of Sector allocations
    sector_values = []
    index = 23
    while df.iloc[index, 4] is not None:
        sector_body = {}
        sector_body.update({"sector_name": df.iloc[index, 4]})
        sector_body.update({"exposure": float(df.iloc[index, 5])})
        sector_values.append(sector_body)
        index += 1
    return sector_values
