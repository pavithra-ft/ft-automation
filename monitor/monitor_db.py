import MySQLdb as my
import smtplib
import schedule
import time
import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

mail = EMAIL_ADDRESS
pwd = EMAIL_PASSWORD
db_error = []
warning = []
exception = []


def connect_db():
    try:
        db = my.connect(host="aa16jknt7bsmtkj.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com",
                        user="wyzeread",
                        passwd=str("Tnnly2mVy6@o&NoYhel%"),
                        db=str("iq-new")
                        )
        cursor = db.cursor()
        sql = "select * from per_all_professionals"
        number_of_rows = cursor.execute(sql)
        print(number_of_rows, datetime.datetime.now())
        db.close()

    except my.DatabaseError as e:
        db_error.append(e)
    except my.Error as e:
        db_error.append(e)
    except my.InterfaceError as e:
        db_error.append(e)
    except my.InternalError as e:
        db_error.append(e)
    except my.DataError as e:
        db_error.append(e)
    except my.IntegrityError as e:
        db_error.append(e)
    except my.MySQLError as e:
        db_error.append(e)
    except my.ProgrammingError as e:
        db_error.append(e)
    except my.OperationalError as e:
        db_error.append(e)
    except my.NotSupportedError as e:
        db_error.append(e)
    except my.Warning as e:
        warning.append(e)
    except Exception as error:
        exception.append(error)


def notify():
    connect_db()
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = "DB IS DOWN!"
        body = "Database is down"
        err = "Database Error : " + ' '.join(map(str, db_error))
        w = "Occured Warnings : " + str(warning)
        emsg = "Captured Exception : " + str(exception)
        msg = f'Subject: {subject}\n\n{body}\n\n{str(err)}\n\n{str(w)}\n\n{str(emsg)}'
        if len(db_error) >= 1 or len(warning) >= 1 or len(exception) >= 1:
            smtp.sendmail(['notifications@fintuple.com'], ['pavithra@fintuple.com'], msg.encode("utf-8"))
            print(datetime.datetime.now(), ": Mail sent")
        db_error.clear()
        warning.clear()
        exception.clear()


connect_db()
schedule.every(1).hours.do(notify)
while True:
    schedule.run_pending()
    time.sleep(1)
