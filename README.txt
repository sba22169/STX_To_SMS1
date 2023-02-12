The aim of this program is to take customer data from Salon managment software package STX in the form of appointment calendar data STX-Appointments.vcs and customer name and phone numbers data exported as Untitled.txt file. 
By parsing data from both files into a look up table and using this to send individual appointment reminder sms to customer with date and time of appointment.
SMS messages are sent through the apple message app linked to an iPhone , this is done using a small AppleScript sendSMS.app. The customer data is error checked which gets reported out as dialogue boxed.


One  time set up of filter for customer phone numbers file:
log to STX with user permission to export reports.
Under Client marketing make a New Set and name it.
In the client filter section:
Operation = Keep matching clients
Dates = Between tomorrow and tomorrow
Appointment status = Exclude and Cancelled
Employees = Include All

In the output setting:
From type choose  Comma Separated Values 
Add: First and Middle and Last Name
Add: Cellular Phone Number
Click Save
The filter is now set up , just execute the filter and export the resulting file when ever required.

vCalender expire:
Go File>Print>Appointments>vCalender Export
Select Dates and export .vsc file

