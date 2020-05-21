# Industry : Sector

sector_dictionary = {'2/3 Wheelers': 'Automobile',
                     'Advertising & Media': 'Services',
                     'Aerospace': 'Services',
                     'Agrochemicals': 'Chemicals',
                     'Airlines': 'Services',
                     'Airport Services': 'Services',
                     'Aluminium': 'Chemicals',
                     'Asset Management Cos.': 'Financial Services',
                     'Banks': 'Financial Services',
                     'Auto Parts & Equipment': 'Automobile',
                     'Auto Tyres & Rubber Products': 'Automobile',
                     'Biotechnology': 'Pharma & Healthcare',
                     'BPO/KPO': 'Services',
                     'Breweries & Distilleries': 'FMCG',
                     'Broadcasting & Cable TV': 'Services',
                     'Carbon Black': 'Chemicals',
                     'Coal': 'Energy',
                     'Cars & Utility Vehicles': 'Automobile',
                     'Cement & Cement Products': 'Construction',
                     'Cigarettes-Tobacco Products': 'FMCG',
                     'Comm.Printing/Stationery': 'Services',
                     'Comm.Trading  & Distribution': 'Energy',
                     'Commercial Vehicles': 'Automobile',
                     'Commodity Chemicals': 'Chemicals',
                     'Computer Hardware': 'Technology',
                     'Copper': 'Chemicals',
                     'Construction & Engineering': 'Construction',
                     'Construction Materials': 'Construction',
                     'Consulting Services': 'Construction',
                     'Consumer Electronics': 'Consumer Goods',
                     'Containers & Packaging': 'Chemicals',
                     'Data Processing Services': 'Services',
                     'Defence': 'Services',
                     'Department Stores': 'Services',
                     'Distributors': 'Energy',
                     'Diversified': 'Diversified',
                     'Edible Oils': 'Energy',
                     'Education': 'Services',
                     'Electric Utilities': 'Consumer Goods',
                     'Electronic Components': 'Engineering',
                     'Exploration & Production': 'Engineering',
                     'Fertilizers': 'Chemicals',
                     'Footwear': 'FMCG',
                     'Fibres & Plastics': 'Chemicals',
                     'Finance (including NBFCs)': 'Financial Services',
                     'Financial Institutions': 'Financial Services',
                     'Food & Drugs Retailing': 'Pharma & Healthcare',
                     'Forest Products': 'FMCG',
                     'Furniture-Furnishing-Paints': 'Chemicals',
                     'Hotels': 'Services',
                     'General Insurance': 'FMCG',
                     'Gift Articles-Toys & Cards': 'FMCG',
                     'Cash': 'Cash & Equiv.',
                     'Healthcare Facilities': 'Pharma & Healthcare',
                     'Healthcare Services': 'Pharma & Healthcare',
                     'Healthcare services': 'Pharma & Healthcare',
                     'Healthcare Supplies': 'Pharma & Healthcare',
                     'Houseware': 'Consumer Goods',
                     'Mining': 'Metals',
                     'Heavy Electrical Equipment': 'Engineering',
                     'Holding Companies': 'Financial Services',
                     'Household Appliances': 'Consumer Goods',
                     'Household Products': 'Consumer Goods',
                     'Housing Finance': 'Financial Services',
                     'Industrial Gases': 'Energy',
                     'Publishing': 'Services',
                     'Industrial Machinery': 'Engineering',
                     'Integrated Oil & Gas': 'Energy',
                     'Oil & Gas': 'Energy',
                     'Internet & Catalogue Retail': 'Services',
                     'Internet Software & Services': 'Technology',
                     'Investment Companies': 'Financial Services',
                     'Iron & Steel Products': 'Engineering',
                     'Iron & Steel/Interm.Products': 'Engineering',
                     'IT Consulting & Software': 'Technology',
                     'IT Networking Equipment': 'Engineering',
                     'IT Software Products': 'Technology',
                     'IT Training Services': 'Technology',
                     'Jute & Jute Products': 'Textiles',
                     'Life Insurance': 'FMCG',
                     'Marine Port & Services': 'Services',
                     'Restaurants': 'Services',
                     'Medical Equipment': 'Pharma & Healthcare',
                     'Misc.Commercial Services': 'Others',
                     'Movies & Entertainment': 'Services',
                     'Non-alcoholic Beverages': 'FMCG',
                     'Non-Durable Household Prod.': 'Consumer Goods',
                     'Refineries/ Petro-Products': 'Energy',
                     'Oil Equipment & Services': 'Energy',
                     'Oil Marketing & Distribution': 'Energy',
                     'Other Agricultural Products': 'FMCG',
                     'Other Apparels & Accessories': 'Textiles',
                     'Other Elect.Equip./ Prod.': 'Engineering',
                     'Other Financial Services': 'Financial Services',
                     'Other Food Products': 'FMCG',
                     'Other Industrial Goods': 'Engineering',
                     'ETFs': 'ETFs',
                     'ETF': 'ETFs',
                     'Other Industrial Products': 'Engineering',
                     'Other Leisure Facilities': 'Services',
                     'Other Leisure Products': 'Services',
                     'Other Non-Ferrous Metals': 'Metals',
                     'Other Telecom Services': 'Telecom',
                     'Telecom': 'Telecom',
                     'Packaged Foods': 'FMCG',
                     'Sugar': 'FMCG',
                     'Paper & Paper Products': 'FMCG',
                     'Personal Products': 'FMCG',
                     'Petrochemicals': 'Chemicals',
                     'Pharmaceuticals': 'Pharma & Healthcare',
                     'Photographic Products': 'Engineering',
                     'Plastic Products': 'Chemicals',
                     'Realty': 'Services',
                     'Telecom Cables': 'Telecom',
                     'Real Estate Investment': 'Construction',
                     'Storage Media & Peripherals': 'Services',
                     'Roads & Highways': 'Services',
                     'Shipping': 'Services',
                     'Surface Transportation': 'Services',
                     'Sp.Consumer Services': 'Consumer Goods',
                     'Specialty Chemicals': 'Chemicals',
                     'Specialty Retail': 'Services',
                     'Tea & Coffee': 'FMCG',
                     'Telecom Services': 'Telecom',
                     'Telecom - Alternate Carriers': 'Telecom',
                     'Telecom Equipment': 'Telecom',
                     'Textiles': 'Textiles',
                     'Transport Related Services': 'Services',
                     'Zinc': 'Chemicals',
                     'Transportation - Logistics': 'Services',
                     'Travel Support Services': 'Services',
                     'Utilities:Non-Elec.': 'Consumer Goods',
                     'Unknown': 'Unknown',
                     'Others': 'Others',
                     'Others ': 'Others',
                     'Mutual Funds': 'MFs',
                     'Consumer Durables': 'Consumer Goods',
                     'Cosumer Goods': 'Consumer Goods',
                     'Chemicals': 'Chemicals',
                     'Finance': 'Financial Services',
                     'Construction': 'Construction',
                     'Auto Ancillaries': 'Automobile',
                     'Petroleum Products': 'Energy',
                     'Software': 'Technology',
                     'Textile Products': 'Textiles',
                     'Media & Entertainment': 'Services',
                     'Construction Project': 'Construction',
                     'Auto': 'Automobile',
                     'Ferrous Metals': 'Metals',
                     'Metals': 'Metals',
                     'Paper': 'FMCG',
                     'FMCG': 'FMCG',
                     'Consumer staples': 'Consumer Goods',
                     'Consumer discretionary': 'Consumer Goods',
                     'Pharma & Healthcare': 'Pharma & Healthcare',
                     'Healhcare Services': 'Pharma & Healthcare',
                     'Healthcare': 'Pharma & Healthcare',
                     'Financials': 'Financial Services',
                     'Home building Materials': 'Construction',
                     'Financial Services': 'Financial Services',
                     'Financial services': 'Financial Services',
                     'Consumer Goods': 'Consumer Goods',
                     'Consumer goods': 'Consumer Goods',
                     'Consumer': 'Consumer Goods',
                     'Consumer Tech': 'Consumer Goods',
                     'IT': 'Technology',
                     'Technology': 'Technology',
                     'Techology': 'Technology',
                     'Pharma': 'Pharma & Healthcare',
                     'Industrial Manufacturing': 'Industrial Manufacturing',
                     'Energy': 'Energy',
                     'Services': 'Services',
                     'Materials': 'Construction',
                     'Automobile': 'Automobile',
                     'Industrial Manufacting': 'Engineering',
                     'Engineering': 'Engineering',
                     'Miscellaneous': 'Others',
                     'Cash & Cash Equivalents': 'Cash & Equiv.',
                     'Cash & Equiv.': 'Cash & Equiv.'}
