import camelot
import warnings
from datetime import datetime
from config.base_logger import app_logger

warnings.simplefilter('ignore')


def get_nse_data(pdf_files):
    app_logger.info('Index Performance - NSE Ratios/Sector/Holding extraction is started')
    nse_list = []
    for pdf in pdf_files:
        nse_dict = {}
        index_code = pdf.split('\\')[-1].split('.')[0].replace("ind_", "").upper().replace("_", ""). \
            replace("MIDCAP", "MC").replace("SMALLCAP", "SC")
        sector = camelot.read_pdf(pdf)
        sector_table = sector[3].df
        sec_name = sector_table[0][0]
        if sec_name == 'Sector':
            sector_name = sector_table[0][1]
            sector_exposure = round((float(sector_table[1][1]) / 100), 4)
        elif sec_name == 'Statistics ##':
            sector_table = sector[5].df
            sector_name = sector_table[0][1]
            sector_exposure = round((float(sector_table[1][1]) / 100), 4)
        elif sec_name == 'Company’s Name':
            sector_table = sector[4].df
            sector_name = sector_table[0][1]
            sector_exposure = round((float(sector_table[1][1]) / 100), 4)
        else:
            sector_name = 'Healthcare Services'
            sector_exposure = 1

        portfolio = camelot.read_pdf(pdf, flavor='stream', table_areas=['320,286,577,116'])[0].df
        statistics = camelot.read_pdf(pdf, flavor='stream', table_areas=['321,446,577,375'])[0].df
        ratios = camelot.read_pdf(pdf, flavor='stream', table_areas=['323,344,565,320'])[0].df
        date = camelot.read_pdf(pdf, flavor='stream', table_areas=['495,737,571,724'])[0].df

        standard_deviation = round((float(statistics[1][3]) / 12), 4)
        pe_ratio = float(ratios[0][1])
        portfolio_name = portfolio[0][1]
        portfolio_exposure = round((float(portfolio[1][1]) / 100), 4)
        reporting_date = str(datetime.strptime(date[0][0], "%B %d, %Y").date())

        nse_dict.update({'index_code': index_code, 'standard_deviation': standard_deviation, 'pe_ratio': pe_ratio,
                         'top_sector_name': sector_name, 'top_sector_exposure': sector_exposure,
                         'top_holding_isin': portfolio_name, 'top_holding_exposure': portfolio_exposure,
                         'reporting_date': reporting_date})
        nse_list.append(nse_dict)
    app_logger.info('Index Performance - NSE Ratios/Sector/Holding extraction is completed')
    return nse_list
