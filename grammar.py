import re
import re
from nltk import CFG
from nltk.parse import ChartParser
from nltk.parse import RecursiveDescentParser
import nltk



# Define the combined regex pattern for phone numbers
phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\d{10}\b|\(\d{3}\) \d{3}-\d{4}'


# Defining the combined regex pattern for various date formats
date_pattern = (
    r'\b(20[0-2][0-9])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\b|'   # YYYY-MM-DD
    r'\b(20[0-2][0-9])/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])\b|'   # YYYY/MM/DD
    r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s(0?[1-9]|[12][0-9]|3[01])\s'
    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s(20[0-2][0-9])\b|'  # Day, DD Month YYYY
    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s'
    r'(0?[1-9]|[12][0-9]|3[01]),\s(20[0-2][0-9])\b'  # Month DD, YYYY
)   


# Time pattern
time_pattern = r'\b(2[0-3]|[01]?[0-9]):([0-5][0-9])(?::([0-5][0-9]))?\s?(AM|PM|am|pm)?\b'



# Methods 

def detect_phone_numbers(text):
    # Finding all matches in the text
    phones = re.findall(phone_pattern, text)
    return phones



def detect_dates(text):
    # Finding all matches in the text
    dates = re.findall(date_pattern, text)
    formatted_dates = []
    
    for date in dates:
        # YYYY-MM-DD
        if date[0]:
            formatted_dates.append(f"{date[0]}-{date[1]}-{date[2]}")
        # YYYY/MM/DD
        elif date[3]:
            formatted_dates.append(f"{date[3]}/{date[4]}/{date[5]}")
        # Day, DD Month YYYY
        elif date[6]:
            formatted_dates.append(f"{date[6]}, {date[7]} {date[8]} {date[9]}")
        # Month DD, YYYY
        elif date[10]:
            formatted_dates.append(f"{date[10]} {date[11]}, {date[12]}")
    
    return formatted_dates


def detect_times(text):
    """Detect times in the text."""
    times = re.findall(time_pattern, text)
    formatted_times = []
    for time in times:
        hour, minute, second, am_pm = time
        if am_pm:  # If AM/PM is present
            formatted_times.append(f"{hour}:{minute}{am_pm.upper()}")
        elif second:  # If seconds are present
            formatted_times.append(f"{hour}:{minute}:{second}")
        else:  # Standard 24-hour format
            formatted_times.append(f"{hour}:{minute}")
    return formatted_times


# Sample sentences
# Additional test sentences
test_sentences = [
    "You can reach me at 123-456-7890.",
    "Contact support at (987) 654-3210 for assistance.",
    "My old number was 1234567890, but it's no longer active.",
    "The event is scheduled for 2022-12-15.",
    "We met on December 25, 2020.",
    "The deadline is Friday, 1 January 2024.",
    "Our flight departs at 16:45.",
    "The train arrives at 08:30 AM.",
    "The alarm is set for 12:00:00 PM.",
    "Class starts at 23:59 sharp.",
    "Call me at 111-222-3333 on Monday, March 5, 2021, at 10:15 AM.",
    "The meeting is on 2024/07/20 at 02:15 PM. Call (444) 555-6666 for details.",
    "Let's schedule the interview on 2023-11-01 at 14:00."
]

# Processing each sentence and outputting in the required format
for sentence in test_sentences:
    print(f"Input: {sentence}")
    
    # Detect patterns
    detected_phones = detect_phone_numbers(sentence)
    detected_dates = detect_dates(sentence)
    detected_times = detect_times(sentence)
    
    # Print detected patterns
    for phone in detected_phones:
        print(f" - Detected phone number: {phone}")
    for date in detected_dates:
        print(f" - Detected date: {date}")
    for time in detected_times:
        print(f" - Detected time: {time}")
    print()



    # Defining a simple grammar for phone numbers 
    phone_grammar = CFG.fromstring("""
    S -> PHONE
    PHONE -> '123-456-7890' | '987-654-3210' | '1234567890'
    """)


    # Defining a simple grammar for dates (simplified for demonstration)
    date_grammar = CFG.fromstring("""
    S -> MONTH DAY ',' YEAR
    MONTH -> 'January' | 'February' | 'March' | 'April' | 'May' | 'June' | 'July' | 'August' | 'September' | 'October' | 'November' | 'December'
    DAY -> '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '26' | '27' | '28' | '29' | '30' | '31'
    YEAR -> '2020' | '2021' | '2022' | '2023' | '2024'
    """)

    # Defining a simple grammar for times
    time_grammar = CFG.fromstring("""
    S -> HOUR ':' MINUTE
    HOUR -> DIGIT DIGIT | DIGIT
    MINUTE -> DIGIT DIGIT
    DIGIT -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    """)



def parse_phone_number(grammar, text):
    parser = ChartParser(grammar)
    # Using regular expression to extract phone number directly
    phone_match = re.search(r'\d{3}-\d{3}-\d{4}|\d{10}', text)
    if phone_match:
        phone_number = phone_match.group()
        print("Extracted Phone Number:", phone_number)  
        tokens = [phone_number]  
        try:
            trees = list(parser.parse(tokens))
            for tree in trees:
                tree.pretty_print()  
            print("No valid parse found.")
    else:
        print("No phone number found in the text.")


def parse_date(grammar, text):
    parser = ChartParser(grammar)
    # Regular expression to extract dates in "Month Day, Year" format
    date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, (2020|2021|2022|2023|2024)', text)
    if date_match:
        date_str = date_match.group()
        print("Extracted Date:", date_str)  # Debug: print extracted date
        # Split into tokens but preserve the comma as a separate token
        tokens = date_str.replace(',', ' ,').split()
        try:
            trees = list(parser.parse(tokens))
            if trees:
                for tree in trees:
                    print(tree)  # Print the tree structure
                    tree.pretty_print()  # Visualize the tree in a readable format
            else:
                print("Parsed but no trees generated.")
        except ValueError:
            print("No valid parse found.")
    else:
        print("No date found in the text.")



def parse_time(grammar, text):
    parser = ChartParser(grammar)
    time_match = re.search(r'([01]?\d|2[0-3]):[0-5]\d', text)  
        time_str = time_match.group()
        print("Extracted Time:", time_str)  
        # Tokenize into individual digits and the colon
        tokens = list(time_str.replace(':', ' : ').replace('', ' ').split())
        try:
            # Parse the tokens
            trees = list(parser.parse(tokens))
            if trees:
                for tree in trees:
                    print("Parse Tree:")
                    tree.pretty_print()  # Visualize the tree in a readable format
            else:
                print("Parsed but no trees generated.")
        except Exception as e:
            print(f"Parsing failed: {e}")
    else:
        print("No time found in the text.")




# # Testing dates
parse_date(date_grammar, 'Meet me on July 4, 2024.')
parse_date(date_grammar, 'The event is on July 4, 2024.') 
parse_date(date_grammar, 'I was born on January 1, 2020.') 
# parse_date(date_grammar, 'We have a meeting on March 15, 2022.') 
# parse_date(date_grammar, 'The deadline is February 28, 2023.') 
# parse_date(date_grammar, 'Independence Day is July 4, 2024.')  
# parse_date(date_grammar, 'April 30, 2021 was a Friday.') 
# parse_date(date_grammar, 'The launch is planned for November 11, 2024.')  

# Testing phone numbers within different sentences
parse_phone_number(phone_grammar, '987-654-3210')  
parse_phone_number(phone_grammar, '1234567890')  
parse_phone_number(phone_grammar, 'You can reach me at 123-456-7890 anytime.')  
# parse_phone_number(phone_grammar, 'Please call 987-654-3210.') 
# parse_phone_number(phone_grammar, '1234567890 is my office phone number.')  
# parse_phone_number(phone_grammar, 'For inquiries, please contact us at 123-456-7890 or email us.') 
# parse_phone_number(phone_grammar, 'Our numbers are 987-654-3210, 123-456-7890, and 1234567890; call any.') 

# # Testing times
parse_time(time_grammar, 'The meeting starts at 14:30.')
parse_time(time_grammar, 'The day starts at 00:00.')
parse_time(time_grammar, 'Lunch is served at 12:00.')
# parse_time(time_grammar, 'We should meet by 18:45.')
# parse_time(time_grammar, 'The deadline is 23:59.')
# parse_time(time_grammar, 'Dinner is planned for 5:30.')
# parse_time(time_grammar, 'The first train leaves at 06:00, and the last train departs at 22:15.')








    