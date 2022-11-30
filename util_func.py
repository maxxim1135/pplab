"""
File with utility function that help with validation, especially with time
"""


from datetime import datetime
from schemas import *
from models import *


def check_if_past_time(date):
    now = str(datetime.now())
    res = False
    year = int(date[0] + date[1] + date[2] + date[3]) - int(now[0] + now[1] + now[2] + now[3])
    month = int(date[5] + date[6]) - int(now[5] + now[6])
    day = int(date[8] + date[9]) - int(now[8] + now[9])
    if year == 0:
        if month == 0:
            if day > 0:
                res = True
        elif month > 0:
            res = True
    elif 0 < year < 5:
        res = True
    return res


def check_time_diff(start, end):
    year1 = int(start[0] + start[1] + start[2] + start[3]) - int(end[0] + end[1] + end[2] + end[3])
    if year1 != 0:
        month1 = int(end[5] + end[6]) - int(start[5] + start[6])
        day = int(end[8] + end[9]) - int(start[8] + start[9])
        if month1 == 0 and day <= 5:
            if day == 0:
                hour = int(end[11][12] - start[11][12])
                if hour < 1:
                    return False
            return True
    return False


def check_valid_time(start, end):
    year = int(end[0] + end[1] + end[2] + end[3]) - \
           int(start[0] + start[1] + start[2] + start[3])           # TODO make func work
    month = int(end[5] + end[6]) - int(start[5] + start[6])
    day = int(end[8] + end[9]) - int(start[8] + start[9])
    if year > 0:
        return True
    if year == 0:
        if month > 0:
            return True
        elif month == 0:
            if day > 0:
                return True
            elif day < 0:
                return False
            else:
                hour = int(end[11] + end[12]) - int(start[11] + start[12])
                if hour < 0:
                    return False
                else:
                    return True
        else:
            return False
    else:
        return False


def check_time(audience_id, end_time, start_time):
    if session.query(Order).filter(Order.id_audience == audience_id).count() > 0:

        if not session.query(Order).filter(Order.id_audience == audience_id). \
                       filter(start_time >= Order.start_time,
                              end_time <= Order.end_time).count() == 0:
            raise ValidationError("Order exists")
        elif not session.query(Order).filter(Order.id_audience == audience_id). \
                         filter(start_time < Order.start_time,
                                end_time >= Order.start_time).count() == 0:
            raise ValidationError("Order exists")

        elif not session.query(Order).filter(Order.id_audience == audience_id). \
                         filter(start_time <= Order.end_time, end_time > Order.end_time).count() == 0:
            raise ValidationError("Order exists")

        elif not check_if_past_time(start_time):
            raise ValidationError("We live in the present and not in the past")

        elif not session.query(Order).filter(Order.id_audience == audience_id). \
                         filter(start_time <= str(datetime.now())[:9]).count() == 0:
            raise ValidationError("We live in the present and not in the past")

    return True
