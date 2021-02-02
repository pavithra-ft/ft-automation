from glob import glob
from config.base_logger import sql_logger
from services.index_performance.service.index_performance import get_indices_performance


if __name__ == "__main__":
    pdf_files = [file for file in glob(r"C:\Users\pavithra\Documents\fintuple-automation-projects"
                                       r"\MonthlyRatioExtraction\ratio_extraction\ratio_extraction"
                                       r"\downloaded_files\*.pdf")]
    sql_logger.info('Index Performance - Started')
    get_indices_performance(pdf_files)
