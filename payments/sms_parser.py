import re

def parse_mpesa_sms(sms_text):
    """
    Parses an M-Pesa SMS and extracts transaction details.

    Args:
        sms_text: The raw M-Pesa SMS message.

    Returns:
        A dictionary containing the extracted details (e.g., transaction_id, amount, balance),
        or None if the SMS format is not recognized.
    """
    # Regex for "Send Money" confirmation
    send_money_pattern = re.compile(
        r'(?P<transaction_id>\w+) Confirmed. Ksh(?P<amount>[\d,]+\.\d{2}) sent to (?P<recipient>.+?) on (?P<date>.+?) at (?P<time>.+?)\. New M-PESA balance is Ksh(?P<balance>[\d,]+\.\d{2})\.'
    )

    # Regex for "Receive Money" notification
    receive_money_pattern = re.compile(
        r'(?P<transaction_id>\w+) Confirmed\. You have received Ksh(?P<amount>[\d,]+\.\d{2}) from (?P<sender>.+?) on (?P<date>.+?) at (?P<time>.+?)\. New M-PESA balance is Ksh(?P<balance>[\d,]+\.\d{2})\.'
    )

    # Regex for "Pay Bill" confirmation
    pay_bill_pattern = re.compile(
        r'(?P<transaction_id>\w+) Confirmed\. Ksh(?P<amount>[\d,]+\.\d{2}) sent to (?P<business>.+?) for account (?P<account_no>.+?) on (?P<date>.+?) at (?P<time>.+?)\. New M-PESA balance is Ksh(?P<balance>[\d,]+\.\d{2})\.'
    )

    patterns = [send_money_pattern, receive_money_pattern, pay_bill_pattern]

    for pattern in patterns:
        match = pattern.match(sms_text)
        if match:
            return match.groupdict()

    return None
