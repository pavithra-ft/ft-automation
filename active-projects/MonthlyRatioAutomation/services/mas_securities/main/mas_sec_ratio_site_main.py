from database.db_queries import iq_session
from config.base_logger import app_logger, sql_logger
from extraction.security_ratio_bse_500 import get_security_ratio
from database.db_queries import put_mas_securities
from services.mas_securities.service.mas_sec_ratio_site import get_mas_security_ratio

if __name__ == "__main__":
    sql_logger.info('Mas Securities - Ratios extraction from website is started')
    security_ratio_list = get_security_ratio()
    mas_security_ratio_list = get_mas_security_ratio(security_ratio_list)
    try:
        put_mas_securities(mas_security_ratio_list)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        app_logger.info('Exception raised in queries : ' + str(error))
        sql_logger.info('Exception raised in queries : ' + str(error))
    finally:
        iq_session.close()
    sql_logger.info('Mas Securities - Ratios extraction from website is completed')
