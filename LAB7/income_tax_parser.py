import re

def clean_pan(pan):
    """
    Removes spaces from a PAN and upper-cases it.
    Returns None if input is not a valid non-empty string.
    """
    if not isinstance(pan, str):
        return None
    cleaned = pan.strip().replace(' ', '').upper()
    if not cleaned:
        return None
    return cleaned


def parse_amount(text):
    """
    Converts an amount such as 'Rs 12,50,000' into an int.
    Returns None if input cannot be safely parsed as a non-negative integer.
    """
    if not isinstance(text, str):
        return None
    cleaned = re.sub(r'(?i)\brs\.?', '', text).replace(',', '').replace(' ', '').strip()
    if not cleaned or not cleaned.isdigit():
        return None
    return int(cleaned)


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) tuple.
    Returns None if the line is not in valid 'LOW-HIGH:RATE' integer format.
    """
    if not isinstance(line, str):
        return None
    line = line.strip()
    if ':' not in line:
        return None
    parts = line.split(':')
    if len(parts) != 2:
        return None
    limits, rate_str = parts[0].strip(), parts[1].strip()
    limit_parts = limits.split('-')
    if len(limit_parts) != 2:
        return None
    low_str, high_str = limit_parts[0].strip(), limit_parts[1].strip()
    if not (low_str.isdigit() and high_str.isdigit() and rate_str.isdigit()):
        return None
    low, high, rate = int(low_str), int(high_str), int(rate_str)
    if low > high:
        return None
    return low, high, rate


def main():
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    print("Amount in rupees:", parse_amount(value))

    print("\n==== Running parse_tax_slab ====")
    value = input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    print("Tax slab (low, high, rate):", parse_tax_slab(value))


if __name__ == "__main__":
    main()