from colorama import init, Fore, Style

from os import get_terminal_size as size

# Initialize colorama
init()
W = size()[0]

# Get first 1000 digits of pi
PI = "3.\
14159265358979323846264338327950288419716939937510\
58209749445923078164062862089986280348253421170679\
82148086513282306647093844609550582231725359408128\
48111745028410270193852110555964462294895493038196\
44288109756659334461284756482337867831652712019091\
45648566923460348610454326648213393607260249141273\
72458700660631558817488152092096282925409171536436\
78925903600113305305488204665213841469519415116094\
33057270365759591953092186117381932611793105118548\
07446237996274956735188575272489122793818301194912\
98336733624406566430860213949463952247371907021798\
60943702770539217176293176752384674818467669405132\
00056812714526356082778577134275778960917363717872\
14684409012249534301465495853710507922796892589235\
42019956112129021960864034418159813629774771309960\
51870721134999999837297804995105973173281609631859\
50244594553469083026425223082533446850352619311881\
71010003137838752886587533208381420617177669147303\
59825349042875546873115956286388235378759375195778\
18577805321712268066130019278766111959092164201989"

def compare_numbers(correct, user):
    finished_output = ""
    colored = False
    for line in range((len(correct) + 10) // W + 1):
        if line:
            finished_output += correct[line*W-10:(line+1)*W-10] + '\n'
        else:
            finished_output += 'Correct:  ' + correct[0:W-10] + '\n'
            finished_output += 'Your try: '
        
        start = 0 if line == 0 else (W * line) - 10
        end = min(W * (line + 1) - 10, len(user))
        for char in range(start, end):
            if user[char] == correct[char]:
                if colored: finished_output += Style.RESET_ALL; colored = False
                finished_output += user[char]
            else:
                if not colored: finished_output += Fore.RED; colored = True
                finished_output += user[char]

        if colored: finished_output += Style.RESET_ALL; colored = False
        
        finished_output += '\n'
            
    return finished_output

def check_shifted_match(corr_PI, user_PI, window=5, match_level=2):
    """Check if numbers match when shifted by a few positions and align sequences"""
    # match_level is how many digits you want matched before telling if you skipped/added digits
    fixed_user = ""
    fixed_PI = ""
    i = 0
    j = 0
    # Gives the correct starting point for additional digits from corr_PI
    add_digs = len(user_PI)
    
    while i < len(user_PI):
        if user_PI[i] == corr_PI[j]:
            fixed_user += user_PI[i]
            fixed_PI += corr_PI[j]
            i += 1; j += 1
            continue
        for k in range(1, window + 1):
            if j + k + match_level <= len(corr_PI) and user_PI[i:i+match_level] == corr_PI[j + k:j + k + match_level]:
                shift = '-' * k
                fixed_user += shift + user_PI[i]
                fixed_PI += corr_PI[j: j + k + 1]
                i += 1; j += k + 1
                add_digs += k
                break
            elif i + k + match_level <= len(user_PI) and corr_PI[j:j+match_level] == user_PI[i + k:i + k + match_level]:
                shift = ' ' * k
                fixed_user += user_PI[i: i + k + 1]
                fixed_PI += shift + corr_PI[j]
                i += k + 1; j += 1
                add_digs -= k
                break
        else:
            fixed_user += user_PI[i]
            fixed_PI += corr_PI[j]
            i += 1; j += 1

    return fixed_PI + corr_PI[add_digs: add_digs + 5], fixed_user


print("Memorize PI! Enter as many digits as you can remember:")
print("\nNow enter your attempt (press Enter when done):")

user_input = input()
if user_input[:2] != "3.":
    user_input = "3." + user_input

# Check for shifted matches
fixed_PI, fixed_user = check_shifted_match(PI, user_input)


# Show results
print("\nResults:")
results = compare_numbers(fixed_PI, fixed_user)

print(results)

# Calculate accuracy
correct_count = sum(1 for i in range(2, min(len(fixed_user), len(PI))) if i < len(fixed_user) and fixed_user[i] == fixed_PI[i])
accuracy = (correct_count / (len(fixed_user) - 2)) * 100 if fixed_user else 0

print(f"\nAccuracy: {accuracy:.2f}%")
print(f"Correct digits: {correct_count}")