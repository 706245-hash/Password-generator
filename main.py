import random
import string
import sys

# ANSI color codes
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """Generate a secure random password with specified character sets."""
    char_sets = []
    if use_lower: char_sets.append(string.ascii_lowercase)
    if use_upper: char_sets.append(string.ascii_uppercase)
    if use_digits: char_sets.append(string.digits)
    if use_symbols: char_sets.append('!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    if not char_sets:
        print(f"{COLORS['YELLOW']}Warning: Using all character types{COLORS['END']}")
        char_sets = [
            string.ascii_lowercase, 
            string.ascii_uppercase, 
            string.digits, 
            '!@#$%^&*()_+-=[]{}|;:,.<>?'
        ]
    
    all_chars = ''.join(char_sets)
    
    # Ensure at least one character from each selected set
    password = []
    if use_lower: password.append(random.choice(string.ascii_lowercase))
    if use_upper: password.append(random.choice(string.ascii_uppercase))
    if use_digits: password.append(random.choice(string.digits))
    if use_symbols: password.append(random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?'))
    
    # Fill remaining length
    remaining = length - len(password)
    password.extend(random.choices(all_chars, k=remaining))
    
    # Shuffle to mix character types
    random.shuffle(password)
    return ''.join(password)

def get_yes_no_input(prompt, default=True):
    """Get yes/no input with colored prompt."""
    options = " (Y/n)" if default else " (y/N)"
    full_prompt = f"{COLORS['BLUE']}{prompt}{options}{COLORS['END']}: "
    while True:
        response = input(full_prompt).lower()
        if response in {'', 'y', 'yes', 'n', 'no'}:
            return response in {'', 'y', 'yes'} if default else response in {'y', 'yes'}
        print(f"{COLORS['YELLOW']}Invalid input. Please enter 'y' or 'n'{COLORS['END']}")

def get_int_input(prompt, default=12, min_val=4):
    """Get integer input with colored prompt."""
    full_prompt = f"{COLORS['CYAN']}{prompt} (default: {default}){COLORS['END']}: "
    while True:
        response = input(full_prompt).strip()
        if not response:
            return default
        try:
            value = int(response)
            if value < min_val:
                print(f"{COLORS['YELLOW']}Value too small. Minimum is {min_val}{COLORS['END']}")
                continue
            return value
        except ValueError:
            print(f"{COLORS['RED']}Invalid number. Please enter a valid integer{COLORS['END']}")

def calculate_strength(password):
    """Calculate password strength with visual indicator."""
    length = len(password)
    diversity = len(set((
        bool(set(password) & set(string.ascii_lowercase)),
        bool(set(password) & set(string.ascii_uppercase)),
        bool(set(password) & set(string.digits)),
        bool(set(password) & set('!@#$%^&*()_+-=[]{}|;:,.<>?'))
    )))
    
    strength = min(100, (length * 3) + (diversity * 15))
    
    if strength < 40:
        color = COLORS['RED']
        label = "Weak"
    elif strength < 70:
        color = COLORS['YELLOW']
        label = "Medium"
    else:
        color = COLORS['GREEN']
        label = "Strong"
    
    bar_length = 20
    filled = int(bar_length * strength / 100)
    bar = f"{color}{'■' * filled}{COLORS['END']}{'□' * (bar_length - filled)}"
    
    return f"{bar} {color}{label} ({strength}%){COLORS['END']}"

def print_banner():
    """Print colorful banner"""
    banner = rf"""
{COLORS['HEADER']}
 ================================================================================
                                ║║║║║║║║║║║║║║║║ 
                               ║╚╚╚╚╚╚╚╚╚╚╚╚╚╚╚╚║
                               ║╚ PASSWORD GEN ╚║
                               ║╚╚╚╚╚╚╚╚╚╚╚╚╚╚╚╚║
                                ║║║║║║║║║║║║║║║║ 
================================================================================                                                         
{COLORS['END']}
"""
    print(banner)

# Main program
print_banner()

print(f"{COLORS['BOLD']}Password Generator Configuration{COLORS['END']}")
print(f"{COLORS['CYAN']}{'='*40}{COLORS['END']}")

length = get_int_input("Password length", min_val=8)
use_upper = get_yes_no_input("Include uppercase letters")
use_lower = get_yes_no_input("Include lowercase letters")
use_digits = get_yes_no_input("Include digits")
use_symbols = get_yes_no_input("Include symbols")

password = generate_password(
    length=length,
    use_upper=use_upper,
    use_lower=use_lower,
    use_digits=use_digits,
    use_symbols=use_symbols
)

strength = calculate_strength(password)

print(f"\n{COLORS['CYAN']}{'='*40}{COLORS['END']}")
print(f"{COLORS['BOLD']}Generated Password:{COLORS['END']} {COLORS['GREEN']}{password}{COLORS['END']}")
print(f"{COLORS['BOLD']}Password Strength:{COLORS['END']} {strength}")
print(f"{COLORS['CYAN']}{'='*40}{COLORS['END']}")

# Copy to clipboard functionality
copy = get_yes_no_input("Copy to clipboard", default=False)
if copy:
    try:
        import pyperclip
        pyperclip.copy(password)
        print(f"\n{COLORS['GREEN']}✓ Password copied to clipboard!{COLORS['END']}")
    except ImportError:
        print(f"\n{COLORS['YELLOW']}Pyperclip not installed. Run 'pip install pyperclip' for clipboard support{COLORS['END']}")

print(f"\n{COLORS['GREEN']}Secure password generated!{COLORS['END']}")
