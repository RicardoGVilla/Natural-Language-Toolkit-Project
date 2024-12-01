import re


# Regular expression patterns 

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