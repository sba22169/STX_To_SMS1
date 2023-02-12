# The aim of this program is to take customer data from STX in the form of STX-Appointments.vcs and Untitled.txt file. 
# by parsing data from both files into a look up table and using this to send individual appointment reminder sms to customer.
# using a small applescript sendSMS.app. The customer data is error checked which gets reported out as dialogue boxed.

import os
import time

old_dates = False


def read_mobile_content(filename):
    """ read in untitled.txt. and strip out unwanted characters"""
    with open(filename, 'r') as f:
        return f.read().strip().replace('"', '').replace('-', '').replace('/', '').replace(',\n', ',0\n')


def read_cvs_content(filename):
    """ open the vCalender file in format CVS"""
    with open(filename, 'r') as f:
        return f.read()


def parse_mobile_content(content):
    """ Parses the  contents of Untitled.txt name and mobile export from stx and returns a dictionary and a dud list"""
    # Some names have no mobiles they are placed in the dud name_no_num for alerting
    name_num, name_no_num = {}, []
    for line in content.split("\n"):
        name, mobile = line.split(",")
        mobile = mobile.strip().replace(' ', '')  # strip space in mobile here as cant do in read_mobile_content
        if len(mobile) < 10:
            name_no_num.append(name)
        name_num[name] = (mobile)  # this was int(mobile) but the leading 0 was missing as an int so removed
    return name_num, name_no_num


def convert_date_time(date_time):
    """ Take the vcs date time format and return a customer friendly format"""
    month_date = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul',
                  '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    ordinal_dict = {'st': ['01', '21', '31'], 'nd': ['2', '22'], 'rd': ['3', '23'],
                    'th': ['04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                           '19', '20', '24', '25', '26', '27', '28', '29', '30']}
    month_num, day, time = date_time[4:6], date_time[6:8], date_time[9:13]
    error_old_date_check(day + month_num)
    month = month_date[month_num]
    for k, v in ordinal_dict.items():
        if day in v:
            day = day + k
    start_time_dict = {'month': month, 'day': day, 'time': time}
    return start_time_dict


def parse_appt_time(cvs_file):
    """ Make a look up table from the CVS file  """
    cvs_lookup = {}
    for line in cvs_file.split('\n'):
        if line[:7] == "DTSTART":
            d, start_time = line.split(":")
            start_time_dict = convert_date_time(start_time)

        if line[:7] == 'SUMMARY':
            name_service = line[34:]
            # below the name and service values will be assigned in first and second respectively and
            #  the rest of the list will be assigned to rest. this gets around the split error seen otherwise 
            name, service, *rest = name_service.split('-') # *rest is example of a variadic , it captures excess positional arguments
            name = name.strip()

        if line[:3] == 'END':
            if name not in cvs_lookup:
                cvs_lookup[name] = start_time_dict
            else:
                if cvs_lookup[name]['time'] > start_time_dict['time']:
                    print(f"{name}time changed from {cvs_lookup[name]['time']} to {start_time_dict['time']}")
                    cvs_lookup[name]['time'] = start_time_dict['time']
    print(cvs_lookup)
    # format the finished cvs_lookup time to include :

    return cvs_lookup


def time_format(dates_times):
    """ Takes time formatted 0000 and inserts a colon 00:00"""
    format_time = f"{dates_times[0:2]}:{dates_times[2:]}"
    return format_time


def make_message(cvs_lookup, name_num):
    """ takes lookup table of client times and makes personal message"""
    for name, dates_times in cvs_parse.items():
        time_format(dates_times['time'])
        mobile = (name_num[name])
        if len(mobile) == 10:  # skips sending message to clients with no mobile
            first_name, *rest = name.split(' ')  # strip out second name
            message = (
                f" 'Hi {first_name} your John Geaney hair appt time is {time_format(dates_times['time'])} on the {dates_times['day']} of {dates_times['month']}, we look forward to seeing you then.' ")
            print(mobile, message)
            # os.system(f"osascript sendSMS.app {mobile} {message}")
            # time.sleep(5)


def error_old_date_check(cvs_date):
    """ checks if dates in cvs file is from the past , to catch human error"""
    global old_dates  # access to change this global variable
    us_format_date = f"{cvs_date[2:4]}{cvs_date[0:2]}" # need dates in us format in order to do date comparison
    from datetime import date
    today = date.today()
    #   the date is asn object that gets accessed by the following call
    d1 = today.strftime("%m%d")  # format mmdd
    if us_format_date < d1:
        old_dates = True
    return old_dates


def make_dialog_box(message_str, title_str):
    """ one stop for all messages to the user"""
    os.system(""
              "osascript -e \'Tell application \"System Events\" to display dialog \"" + message_str + "\" with title \"" + title_str + "\"\'""")


def error_reporting(name_no_num):
    """sets up the message to be reported out. **Warning** exclude "'" from the msg string to avoid shell EOF error"""
    if old_dates == True:
        print("Old dates is true")
        message = "The Appt dates being processed are from the past!"
        title = "File Error"
        make_dialog_box(message, title)
        exit()

    if len(name_no_num) > 0:
        print (name_no_num)
        names = ', '.join(map(str,name_no_num))
        print (names)
        message = (f"The following clients dont have mobile numbers set up : {names}")
        # message = "test test"
        print(message)
        title = "Mobile number error"
        make_dialog_box(message, title)


def missing_mobile_check(name_no_num):
    if len(name_no_num) > 0:
        print(f" name_no_num has content !")


num_content = read_mobile_content(filename='/Users/ambrosedesmond/Documents/GitHub/STX_to_TXT/Untitled.txt')

appt_content = read_cvs_content(filename='/Users/ambrosedesmond/Documents/GitHub/STX_to_TXT/STX-Appointments.vcs')

name_num, name_no_num = parse_mobile_content(num_content)

print(f" \n\n **Warning** The following clients don't have mobile numbers set up : \n\n {name_no_num}\n\n **Warning**")

cvs_parse = parse_appt_time(appt_content)
error_reporting(name_no_num)
make_message(cvs_parse, name_num)
print(old_dates)
