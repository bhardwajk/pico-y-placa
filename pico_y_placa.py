# This is a python utility to check if a vehicle with plate number is allowed to run on a particular date/time depending upon the Pica Y Placa rules
# Correct Input Format python pico_y_placa <plate_number> <date> <time> 
# Example: python pico_y_placa 'abcd 09 8890' '29-04-2017' '08:00PM'
# Program prints if vehicle is allowed to run or not. 

# Current Restrictions (Mon to Fri) between 6AM to 8.30AM & 3PM to 7.30PM:
# Even digit cars on even days
# Odd digit cars on odd days
# No restrictions on other days or time (weekends)

import datetime, sys, unittest

class pico_y_placa():
    def __init__(self, plate_number, date, time):
        self.plate_number = plate_number.strip()
        self.date = date.strip()
        self.time = time.strip()
        self.validDateFormat = '%d-%m-%Y'
        self.validTimeFormat = '%I:%M%p'


    # Check whether inputs are in expected format or not
    def check_inputs(self):
        try:
            datetime.datetime.strptime (self.date, self.validDateFormat)
        except ValueError:
            return False, 'Error in format of date. Correct format is (%s), Example (%s)' % (self.validDateFormat, "28-04-2017")
        try:
            datetime.datetime.strptime (self.time, self.validTimeFormat)
        except ValueError:
            return False, 'Error in format of time. Correct format is (%s), Example (%s)' % (self.validTimeFormat, "4:40PM")
        if not (self.plate_number[-1]).isdigit():
            return False, 'Error in format of plate number. Last value should be a digit'
        return True, ''


    # Return whether vehicle is allowed to run on road on a particular date/time
    def on_or_off(self):
        correctInputs, msg = self.check_inputs()
        if not correctInputs:
            raise ValueError(msg)

        # Returns True if vehicle should be allowed depending on day/time

        # Current Restrictions (Mon to Fri) between 6AM to 8.30AM & 3PM to 7.30PM:
        # Even digit cars on even days
        # Odd digit cars on odd days
        # No restrictions on other days or time (weekends)
        date_object = datetime.datetime.strptime (self.date, self.validDateFormat)
        weekday = date_object.weekday()
        day = date_object.day

        # Weekend - no restrictions (5,6 = Saturday,Sunday)
        if weekday == 5 or weekday == 6:
            return True;

        time_object = datetime.datetime.strptime (self.time, self.validTimeFormat)
        time = time_object.time()

        morning_begin_time = datetime.time(6)
        morning_end_time = datetime.time(8,30)
        evening_begin_time = datetime.time(15)
        evening_end_time = datetime.time(19,30)


        if (time >= morning_begin_time and time <= morning_end_time) or (time >= evening_begin_time and time <= evening_end_time):
            # Only in peak time check vehicle number
            is_weekday_even = ((day % 2) == 0)
            is_plate_number_even = ((int(self.plate_number[-1]) % 2) == 0)

            return (is_plate_number_even == is_weekday_even)

        return True

def main():
    if len (sys.argv) == 4:
        plateStr = sys.argv[1]
        dateStr = sys.argv[2]
        timeStr = sys.argv[3]

        p = pico_y_placa(plateStr, dateStr, timeStr)
        if p.check_inputs()[0]:
            if p.on_or_off():
                print 'Vehicle %s is allowed to run on road on  %s %s'% (plateStr, dateStr, timeStr)
            else:
                print 'Vehicle %s is NOT allowed to run on road on  %s %s'% (plateStr, dateStr, timeStr)
            return
    print 'Error in command usage.\nCorrect Format: python pico_y_placa <plate_number> <date> <time> \nExample: python pico_y_placa \'abcd 09 8890\' \'29-04-2017\' \'08:00PM\''

if __name__ == "__main__":
    main()

class TestInputFormat(unittest.TestCase):

    # Current Restrictions (Mon to Fri) between 6AM to 8.30AM & 3PM to 7.30PM:
    # Even digit cars on even days
    # Odd digit cars on odd days
    # No restrictions on other days or time (weekends)
    def test_weekday_odd_peak_morning(self):
        self.assertEqual(pico_y_placa('abcd 89', '27-04-2017', '7:30AM').on_or_off(), True)
    def test_weekday_odd_peak_evening(self):
        self.assertEqual(pico_y_placa('abcd 89', '27-04-2017', '7:30PM').on_or_off(), True)
    def test_weekday_odd_non_peak(self):
        self.assertEqual(pico_y_placa('abcd 89', '27-04-2017', '12:00PM').on_or_off(), True)
    def test_weekday_even_peak_morning(self):
        self.assertEqual(pico_y_placa('abcd 88', '28-04-2017', '7:30AM').on_or_off(), True)
    def test_weekday_even_peak_evening(self):
        self.assertEqual(pico_y_placa('abcd 88', '25-04-2017', '7:29PM').on_or_off(), False)
    def test_weekday_even_non_peak(self):
        self.assertEqual(pico_y_placa('abcd 88', '28-04-2017', '12:00PM').on_or_off(), True)

    def test_weekend_odd_non_peak(self):
        self.assertEqual(pico_y_placa('abcd 81', '30-04-2017', '12:00PM').on_or_off(), True)
    def test_weekend_even_non_peak(self):
        self.assertEqual(pico_y_placa('abcd 88', '30-04-2017', '12:00PM').on_or_off(), True)
    def test_weekend_odd_peak(self):
        self.assertEqual(pico_y_placa('abcd 81', '30-04-2017', '7:00PM').on_or_off(), True)
    def test_weekend_even_peak(self):
        self.assertEqual(pico_y_placa('abcd 88', '30-04-2017', '7:12PM').on_or_off(), True)

    # Check formatting of date, plate_number, time strings
    def test_incorrect_plate_number(self):
        self.assertEqual(pico_y_placa('abcd 8a', '30-04-2017', '7:12PM').check_inputs()[0], False)
    def test_incorrect_date(self):
        self.assertEqual(pico_y_placa('abcd 88', '3004-2017', '7:12PM').check_inputs()[0], False)
    def test_incorrect_time(self):
        self.assertEqual(pico_y_placa('abcd 89', '30-04-2017', '7:12').check_inputs()[0], False)

