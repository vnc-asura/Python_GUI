import datetime as dt


class DataMixin:
    def date_now(self):
        data = dt.datetime.now().strftime('%x').split('/')
        return f'{data[1]}/{data[0]}/{self.year_now()}'

    def datetime_now(self):
        return f'{self.date_now()} - {self.time_now()}'

    def day_now(self):
        return dt.datetime.now().day

    def month_now(self):
        return dt.datetime.now().month

    def year_now(self):
        return dt.datetime.now().year

    def time_now(self):
        return dt.datetime.now().strftime('%X')

    def seg_now(self):
        return dt.datetime.now().second
