def send_applescript_message(message,mobile):
    import os
    os.system(f"osascript sendSMS.app {mobile} {message}")
message = 'hihihihihi'
mobile = '0866034705'
send_applescript_message(message,mobile)

