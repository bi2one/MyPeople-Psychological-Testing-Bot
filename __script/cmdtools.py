import os

def get_yes_or_no(message, default_yes = False) :
    print message,
    user_input = raw_input()
    if default_yes :
        if user_input.strip() == '' :
            return True
    if user_input.lower() == 'yes' :
        return True
    else :
        return False
    
