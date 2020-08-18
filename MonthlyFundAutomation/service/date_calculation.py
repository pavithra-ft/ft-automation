import calendar
from dateutil.relativedelta import relativedelta


def get_effective_start_end_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Start date and end date of the given reporting date
    """
    effective_start_date = reporting_date.replace(day=1)
    effective_end_date = reporting_date.replace(
        day=calendar.monthrange(effective_start_date.year, effective_start_date.month)[1])
    return effective_start_date, effective_end_date


def get_1m_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date of the Previous month
    """
    previous_1m_date = reporting_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_3m_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date before 3 months from the given reporting date
    """
    previous_3m_date = reporting_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    return previous_3m_end_date


def get_6m_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date before 6 months from the given reporting date
    """
    previous_6m_date = reporting_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1])
    return previous_6m_end_date


def get_1y_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date before 1 year from the given reporting date
    """
    previous_1y_date = reporting_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    return previous_1y_end_date


def get_2y_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date before 2 years from the given reporting date
    """
    previous_2y_date = reporting_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1])
    return previous_2y_end_date


def get_3y_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date before 3 years from the given reporting date
    """
    previous_3y_date = reporting_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1])
    return previous_3y_end_date


def get_5y_date(reporting_date):
    """

    :param reporting_date: Reporting date of the Fund
    :return: Reporting date before 5 years from the given reporting date
    """
    previous_5y_date = reporting_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1])
    return previous_5y_end_date
