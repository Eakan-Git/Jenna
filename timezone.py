from datetime import timezone, timedelta

ICT = timezone(timedelta(hours=7))
DAY_HOUR = '%d/%m %H:%M'
DAYWEEK_DAY_IN_YEAR = '%a %b %d %Y'

def to_ict(datetime, to_string=None):
    datetime = datetime.replace(tzinfo=timezone.utc).astimezone(ICT)
    if to_string:
        datetime = datetime.strftime(to_string)
    return datetime
        