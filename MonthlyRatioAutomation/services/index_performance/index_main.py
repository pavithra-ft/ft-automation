import calendar
from glob import glob
from datetime import datetime
from database.db_queries import iq_session
from dateutil.relativedelta import relativedelta
from config.base_logger import app_logger, sql_logger
from database.db_queries import get_mas_indices, put_index_performance
from services.index_performance.index_performance_calculation import get_index_performance


def get_indices_performance():
    app_logger.info('Index Performance - Indices calculation/extraction is started')
    mas_indices = get_mas_indices()
    del_indices = ['NIFVIX']
    mas_indices = [index for index in mas_indices if index not in del_indices]

    date = datetime.today().date() - relativedelta(months=1)
    reporting_date = date.replace(day=calendar.monthrange(date.year, date.month)[1])

    index_data_list = []
    for index_code in mas_indices:
        app_logger.info('Index Performance - Index code ' + '(' + index_code + ')')
        index_data = get_index_performance(index_code, reporting_date, pdf_files)
        index_data_list.append(index_data)
    try:
        put_index_performance(index_data_list)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        app_logger.info('Exception raised in queries : ' + str(error))
    finally:
        iq_session.close()
    app_logger.info(str(reporting_date) + ' Index Performance - Indices calculation/extraction is Completed')
    sql_logger.info(str(reporting_date) + ' Index Performance - Indices calculation/extraction is Completed')


if __name__ == "__main__":
    pdf_files = [file for file in glob(r"C:\Users\pavithra\Documents\fintuple-automation-projects\RatioExtraction"
                                       r"\ratio_extraction\ratio_extraction\pdf_files\*.pdf")]
    sql_logger.info('Index Performance - Started')
    get_indices_performance()
