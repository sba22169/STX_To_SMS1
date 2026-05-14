# STX to SMS Appointment Reminders

A Python automation tool that generates personalised appointment reminder 
SMS messages from STX salon management software exports, delivered via 
Apple iMessage / standard SMS.

## Problem

STX does not have a native SMS reminder feature . Manually texting appointment reminders to customers 
is time consuming and easy to miss.

## Solution

The script reads two STX exports — a calendar file containing appointment 
times and a contacts CSV with customer names and mobile numbers. It matches 
each customer to their earliest upcoming appointment and generates a 
personalised reminder message, dispatched via Apple iMessage / SMS.
In effect customers have a direct chat with front of house

## How It Works

1. Parses the STX calendar export for upcoming appointments
2. Reads customer contact details from the STX contacts CSV export
3. Matches each customer to their earliest appointment time
4. Generates a personalised SMS for each customer
5. Sends via Apple iMessage

## Usage

```bash
python stx_to_sms.py <calendar_export> <contacts.csv>
```

## Tech Stack
- Python
- Pandas
- Apple iMessage (via osascript)
