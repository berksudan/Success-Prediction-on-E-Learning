from datetime import datetime


class TimeOperations:
    def __init__(self, time_format, date_format):
        self.time_format = time_format
        self.date_format = date_format

    def str_to_time(self, str_time):
        return datetime.strptime(str_time, self.time_format)

    def str_to_date(self, str_date):
        return datetime.strptime(str_date, self.date_format)

    def calc_time_diff(self, list2, list1, date_idx, time_idx):
        d2 = list2[date_idx]
        t2 = list2[time_idx]
        d1 = list1[date_idx]
        t1 = list1[time_idx]

        secs_in_a_day = 86400

        t_diff = abs(self.str_to_time(t2) - self.str_to_time(t1))
        secs_diff = t_diff.seconds  # + t_diff.microseconds / pow(10, 9) ---> add it if necessary.
        if d1 == d2:  # Same day
            return secs_diff

        days_diff = (self.str_to_date(d2) - self.str_to_date(d1)).days
        if days_diff > 1:  # DIFFERENCE = more than 1 day!
            return secs_in_a_day + 1
        elif days_diff == 1:
            return secs_in_a_day - secs_diff
        else:  # days difference is negative
            print('Error in input data, Dates are not ordered')
            print('days_dif: ' + str(days_diff))
            exit(-1)
