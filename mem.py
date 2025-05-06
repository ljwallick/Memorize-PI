from colorama import init, Fore, Style
from os import get_terminal_size as size
import requests as rq

# Initialize colorama
init()
# Get terminal width
W = size()[0]

def compare_numbers(correct, user):
    finished_output = ""
    colored = False
    # Add 10 because the prints 'Your try: ' and 'Correct:  ' are 10 characters each,
    # so need to compensate with the possible new line
    for line in range((len(correct) + 10) // W + 1):
        if line:
            # If it isn't the first line, add the whole line
            finished_output += correct[line*W-10:(line+1)*W-10] + '\n'
        else:
            # If it is, then remove 10 digits from the line and print correct and try as well
            finished_output += 'Correct:  ' + correct[0:W-10] + '\n'
            finished_output += 'Your try: '
        
        start = 0 if line == 0 else (W * line) - 10
        end = min(W * (line + 1) - 10, len(user))

        for char in range(start, end):
            if user[char] == correct[char]:
                # Make sure it isn't red and add the digit
                if colored: finished_output += Style.RESET_ALL; colored = False
                finished_output += user[char]
            else:
                # Make sure it is red and add the digit
                if not colored: finished_output += Fore.RED; colored = True
                finished_output += user[char]

        # Make sur eto reset the color before next line
        if colored: finished_output += Style.RESET_ALL; colored = False
        
        finished_output += '\n'
            
    return finished_output

def check_shifted_match(user_PI, window=5, match_level=2, extra_digs=5):
    """Check if numbers match when shifted by a few positions and align sequences"""
    # match_level is how many digits you want matched before telling if you skipped/added digits
    fixed_user = ""
    fixed_PI = ""
    i = 0
    j = 0

    # The int(... + 5) is to round to nearest integer instead of flooring
    PI_incr = window * 2 + extra_digs
    PI_size = len(user_PI) + PI_incr

    # It doesn't have the period '3.', just '314', so need to add it manually
    corr_PI = '3.' + rq.get(f'https://api.pi.delivery/v1/pi?start=0&numberOfDigits={PI_size}').json()['content'][1:]
    
    # Gives the correct starting point for additional digits from corr_PI
    add_digs = len(user_PI)

    # 0 means you don't want to shift digits, right?
    if match_level == 0:
        return corr_PI[:add_digs + extra_digs], user_PI
    
    while i < len(user_PI):
        if PI_size - j <= window:
            # Ate all the PI? Get More!
            corr_PI += rq.get(f'https://api.pi.delivery/v1/pi?start={PI_size}&numberOfDigits={(PI_incr)}').json()['content']
            PI_size += PI_incr
            
        # If it's correct, just add it
        if user_PI[i] == corr_PI[j]:
            fixed_user += user_PI[i]
            fixed_PI += corr_PI[j]
            i += 1; j += 1
            continue
        # Check 1 through 'window' digits ahead
        for k in range(1, window + 1):
            if j + k + match_level <= len(corr_PI) and user_PI[i:i+match_level] == corr_PI[j + k:j + k + match_level]:
                # Skipped digits placeholder
                shift = '-' * k
                # Add placeholders then just one digit
                fixed_user += shift + user_PI[i]
                fixed_PI += corr_PI[j: j + k + 1]
                i += 1; j += k + 1
                add_digs += k
                break
            if i + k + match_level <= len(user_PI) and corr_PI[j:j+match_level] == user_PI[i + k:i + k + match_level]:
                # Added digits placeholder
                shift = ' ' * k
                fixed_user += user_PI[i: i + k + 1]
                # Add placeholders then just one digit
                fixed_PI += shift + corr_PI[j]
                i += k + 1; j += 1
                add_digs -= k
                break
        else:
            # If match not found, just add the incorrect digit
            fixed_user += user_PI[i]
            fixed_PI += corr_PI[j]
            i += 1; j += 1

    return fixed_PI + corr_PI[add_digs: add_digs + extra_digs], fixed_user


print("Memorize PI! Enter as many digits as you can remember:")
print("\nNow enter your attempt (press Enter when done):")

user_input = input()
if user_input[:2] != "3.":
    user_input = "3." + user_input

# Check for shifted matches
fixed_PI, fixed_user = check_shifted_match(user_input)

# Show results
print("\nResults:")
results = compare_numbers(fixed_PI, fixed_user)

print(results)

# Calculate accuracy
correct_count = sum(1 for i in range(2, len(fixed_user)) if i < len(fixed_user) and fixed_user[i] == fixed_PI[i])
accuracy = (correct_count / (len(fixed_user) - 2)) * 100 if fixed_user else 0

print(f"\nAccuracy: {accuracy:.2f}%")
print(f"Correct digits: {correct_count}")
