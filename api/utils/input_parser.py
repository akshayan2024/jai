"""
Utility module for parsing flexible input formats for birth data
"""
import re
import logging
import json
from datetime import datetime
from typing import Tuple, Optional

logger = logging.getLogger("jai-api.input_parser")

def parse_date(date_input: str) -> str:
    """
    Parse date from various formats into YYYY-MM-DD
    
    Supported formats:
    - YYYY-MM-DD (standard ISO)
    - DD-MM-YYYY
    - MM-DD-YYYY
    - DD/MM/YYYY
    - MM/DD/YYYY
    - DD MMM YYYY (e.g., 01 Dec 1988)
    - MMM DD YYYY (e.g., Dec 01 1988)
    
    Returns:
        ISO formatted date string (YYYY-MM-DD)
    """
    if not date_input:
        raise ValueError("Date input is required")
    
    date_input = date_input.strip()
    
    # Clean up input
    date_input = re.sub(r'\s+', ' ', date_input)
    
    # Try ISO format first (YYYY-MM-DD)
    iso_pattern = r'^(\d{4})[/-](\d{1,2})[/-](\d{1,2})$'
    match = re.match(iso_pattern, date_input)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    
    # Try DD-MM-YYYY or MM-DD-YYYY
    dmy_pattern = r'^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$'
    match = re.match(dmy_pattern, date_input)
    if match:
        first, second, year = match.groups()
        # Assume DD-MM-YYYY format (international standard)
        return f"{int(year):04d}-{int(second):02d}-{int(first):02d}"
    
    # Try DD MMM YYYY or MMM DD YYYY (with text month)
    month_names = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    # Try DD MMM YYYY pattern
    dmy_text_pattern = r'^(\d{1,2})\s+([a-zA-Z]{3,9})\s+(\d{4})$'
    match = re.match(dmy_text_pattern, date_input)
    if match:
        day, month_str, year = match.groups()
        month_num = month_names.get(month_str.lower()[:3])
        if month_num:
            return f"{int(year):04d}-{month_num:02d}-{int(day):02d}"
    
    # Try MMM DD YYYY pattern
    mdy_text_pattern = r'^([a-zA-Z]{3,9})\s+(\d{1,2})\s+(\d{4})$'
    match = re.match(mdy_text_pattern, date_input)
    if match:
        month_str, day, year = match.groups()
        month_num = month_names.get(month_str.lower()[:3])
        if month_num:
            return f"{int(year):04d}-{month_num:02d}-{int(day):02d}"
    
    # If none of the above patterns match, try to parse with datetime
    try:
        # Try common formats
        for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', '%d/%m/%Y', '%m/%d/%Y', 
                    '%d %b %Y', '%b %d %Y', '%d %B %Y', '%B %d %Y'):
            try:
                dt = datetime.strptime(date_input, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
    except Exception as e:
        logger.error(f"Failed to parse date '{date_input}': {str(e)}")
    
    # If we get here, we couldn't parse the date
    raise ValueError(f"Could not parse date from '{date_input}'. Please use YYYY-MM-DD format.")

def parse_time(time_input: str) -> str:
    """
    Parse time from various formats into HH:MM:SS
    
    Supported formats:
    - HH:MM:SS (standard)
    - HH:MM
    - HHMM
    - HH.MM
    - HH:MM AM/PM
    - HH AM/PM
    
    Returns:
        Formatted time string (HH:MM:SS)
    """
    if not time_input:
        raise ValueError("Time input is required")
    
    time_input = time_input.strip()
    
    # Clean up input
    time_input = re.sub(r'\s+', ' ', time_input)
    
    # Check for AM/PM indicator
    is_pm = False
    if re.search(r'[pP][mM]$', time_input):
        is_pm = True
        time_input = re.sub(r'\s*[pP][mM]$', '', time_input)
    elif re.search(r'[aA][mM]$', time_input):
        time_input = re.sub(r'\s*[aA][mM]$', '', time_input)
    
    # Try HH:MM:SS pattern
    time_pattern = r'^(\d{1,2}):(\d{1,2}):(\d{1,2})$'
    match = re.match(time_pattern, time_input)
    if match:
        hour, minute, second = map(int, match.groups())
        if is_pm and hour < 12:
            hour += 12
        if hour == 12 and not is_pm:
            hour = 0
        return f"{hour:02d}:{minute:02d}:{second:02d}"
    
    # Try HH:MM pattern
    time_pattern = r'^(\d{1,2}):(\d{1,2})$'
    match = re.match(time_pattern, time_input)
    if match:
        hour, minute = map(int, match.groups())
        if is_pm and hour < 12:
            hour += 12
        if hour == 12 and not is_pm:
            hour = 0
        return f"{hour:02d}:{minute:02d}:00"
    
    # Try HHMM pattern (without separators)
    time_pattern = r'^(\d{3,4})$'
    match = re.match(time_pattern, time_input)
    if match:
        time_str = match.group(1)
        if len(time_str) == 3:
            time_str = "0" + time_str
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        if is_pm and hour < 12:
            hour += 12
        if hour == 12 and not is_pm:
            hour = 0
        return f"{hour:02d}:{minute:02d}:00"
    
    # Try HH.MM pattern
    time_pattern = r'^(\d{1,2})\.(\d{1,2})$'
    match = re.match(time_pattern, time_input)
    if match:
        hour, minute = map(int, match.groups())
        if is_pm and hour < 12:
            hour += 12
        if hour == 12 and not is_pm:
            hour = 0
        return f"{hour:02d}:{minute:02d}:00"
    
    # Try just HH pattern
    time_pattern = r'^(\d{1,2})$'
    match = re.match(time_pattern, time_input)
    if match:
        hour = int(match.group(1))
        if is_pm and hour < 12:
            hour += 12
        if hour == 12 and not is_pm:
            hour = 0
        return f"{hour:02d}:00:00"
    
    # If we get here, we couldn't parse the time
    raise ValueError(f"Could not parse time from '{time_input}'. Please use HH:MM:SS format.")

def clean_json_string(raw_input: str) -> str:
    """
    Clean up raw JSON-like input to make it valid JSON
    Handles cases where users input data without proper quotes or syntax
    
    Example:
        Input: '"birth_date": 01 dec 1988, "birth_time": "2147"'
        Output: '{"birth_date": "01 dec 1988", "birth_time": "2147"}'
    """
    # If input is already valid JSON, return it as is
    if raw_input.strip().startswith('{') and raw_input.strip().endswith('}'):
        try:
            # Check if it's already valid JSON
            json.loads(raw_input)
            return raw_input
        except json.JSONDecodeError:
            # If not valid, continue with cleaning
            pass
    
    # Add missing braces
    if not raw_input.strip().startswith('{'):
        raw_input = "{" + raw_input
    if not raw_input.strip().endswith('}'):
        raw_input = raw_input + "}"
    
    # Ensure property names are quoted
    raw_input = re.sub(r'(?<={|,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', raw_input)
    
    # Replace multiple spaces with a single space
    raw_input = re.sub(r'\s+', ' ', raw_input)
    
    # Handle unquoted string values
    # First, we'll build a new string
    result = ""
    i = 0
    in_key = False
    in_string = False
    key_start = 0
    
    while i < len(raw_input):
        if raw_input[i:i+1] == '"':
            # Toggle string state
            in_string = not in_string
            result += raw_input[i]
        elif raw_input[i:i+1] == ":" and not in_string:
            # We've just finished a key
            in_key = True
            result += raw_input[i]
        elif raw_input[i:i+1] == "," and not in_string:
            # End of a value
            if in_key:
                # Check if the value before this comma is unquoted
                value = result[result.rfind(":") + 1:].strip()
                if not (value.startswith('"') or value.startswith("[") or 
                        value.startswith("{") or value.strip().isdigit() or 
                        value.strip() in ["true", "false", "null"]):
                    # Replace the unquoted value with a quoted one
                    result = result[:result.rfind(":") + 1] + ' "' + value.strip() + '"'
                in_key = False
            result += raw_input[i]
        elif raw_input[i:i+1] == "}" and not in_string and in_key:
            # End of the last value in the object
            value = result[result.rfind(":") + 1:].strip()
            if not (value.startswith('"') or value.startswith("[") or 
                    value.startswith("{") or value.strip().isdigit() or 
                    value.strip() in ["true", "false", "null"]):
                # Replace the unquoted value with a quoted one
                result = result[:result.rfind(":") + 1] + ' "' + value.strip() + '"'
            in_key = False
            result += raw_input[i]
        else:
            result += raw_input[i]
        i += 1
    
    # Simple approach as a fallback - Try to convert known problematic patterns
    # Convert unquoted string values to quoted string values
    try:
        json.loads(result)
        return result
    except json.JSONDecodeError:
        # If we still can't parse it, try using a simpler approach
        # This is less accurate but may catch some common patterns
        pattern = r'"([^"]+)"\s*:\s*([^",}{]+)(?=[,}])'
        
        def quote_value(match):
            key = match.group(1)
            value = match.group(2).strip()
            
            # If it looks like a number, boolean, or null, leave it unquoted
            if (re.match(r'^-?\d+(\.\d+)?$', value) or 
                value.lower() in ['true', 'false', 'null']):
                return f'"{key}": {value}'
            else:
                # Escape any quotes in the value
                value = value.replace('"', '\\"')
                return f'"{key}": "{value}"'
        
        raw_input = re.sub(pattern, quote_value, raw_input)
        
        # Try to parse the result as JSON
        try:
            json.loads(raw_input)
            return raw_input
        except json.JSONDecodeError as e:
            # If we still can't parse it, raise an error
            logger.error(f"Failed to clean JSON string: {e}")
            raise ValueError(f"Could not clean JSON string: {str(e)}") 