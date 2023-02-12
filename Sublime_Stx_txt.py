# The aim of this program is to take data from STX vcs file and numbers file and create a look up table
# and out put the name txt number and time of appointment for the customer.

import os
import time

def read_mobile_content(filename):
    """ read in untitled.txt. and strip out unwanted characters"""
    with open(filename, 'r') as f:
        return f.read().strip().replace('"', '').replace('-', '').replace('/', '').replace(',\n', ',0\n')


def read_cvs_content(filename):
    """ open the vCalender file in format CVS"""
    with open(filename, 'r') as f:
        return f.read()



def parse_mobile_content(content):
    """ Parces the  contents of Untitled.txt name and mobile export from stx and returns a dictionary and a dud list"""
        # Some names have no mobiles they are placed in the dud name_no_num for alerting
    name_num, name_no_num  = {}, []

    for line in content.split("\n"):
        name, mobile = line.split(",")
        print (mobile)
        mobile = mobile.strip().replace(' ','') # strip space in mobile here as cant do in read_mobile_content

        if int(mobile) == 0:
            name_no_num.append(name)
        name_num[name] = (mobile) # this was int(mobile) but the leading 0 was missing as an int so removed

    return name_num, name_no_num



def convert_date_time(date_time):
    """ Take the vcs date time formatt and return a customer friendly format"""
    month_date = {'01' : 'Jan','02' : 'Feb','03' : 'Mar','04' : 'Apr','05' : 'May','06' : 'Jun','07' : 'Jul','08' : 'Aug','09' : 'Sep','10' : 'Oct','11' : 'Nov','12' : 'Dec'}
    ordinal_dict = {'st' : ['01','21','31'], 'nd' : ['2','22'], 'rd' : ['3','23'], 'th' : ['04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','24','25','26','27','28','29','30']}
    month_num, day, time = date_time[4:6],date_time[6:8],date_time[9:13]
    month = month_date[month_num]
    for k , v in ordinal_dict.items():
        if day in v:
            day = day + k
    start_time_dict = {'month': month, 'day' : day, 'time' : time}
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
            name , service, *rest = name_service.split('-')
            name = name.strip()

        if line[:3] == 'END':
            if name not in cvs_lookup:
                cvs_lookup[name] = start_time_dict
            else:
                if cvs_lookup[name]['time'] > start_time_dict['time']:
                    print(f"{name}time changed from {cvs_lookup[name]['time']} to {start_time_dict['time']}")
                    cvs_lookup[name]['time'] = start_time_dict['time']
    print(cvs_lookup)

    return cvs_lookup



def make_message(cvs_lookup,name_num):
    """ takes lookup table of client times and makes personal message"""
    for name, dates_times in cvs_parse.items():
        mobile = (name_num[name])
        message = (f" 'Hi {name} your John Geaney hair appt time is {dates_times['time']} on the {dates_times['day']} of {dates_times['month']}.' ")
        print(mobile,message)
        #os.system(f"osascript sendSMS.app {mobile} {message}")
        #time.sleep(5)



def send_applescript_message(message,mobile):

    #os.system(f"osascript sendSMS.app {mobile} {message}")
    print(f"sending message {message} \n to mobile {mobile}\n\n")






num_content = read_mobile_content(filename='Untitled.txt')

appt_content = read_cvs_content(filename='STX-Appointments.vcs')

name_num, name_no_num = parse_mobile_content(num_content)

print(f" \n\n **Warning** The following clients don't have mobile numbers set up : \n\n {name_no_num}\n\n **Warning**")

#print(f" Ready to txt out the following good clients : \n\n{name_num}")

cvs_parse = parse_appt_time(appt_content)

make_message(cvs_parse,name_num)





