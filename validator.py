import re


def validate_ip(ip_address):
    """Validate the IP address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip_address) is not None


def validate_cidr(cidr):
    """Validate the CIDR format."""
    try:
        return 0 <= int(cidr) <= 32
    except ValueError:
        return False


def get_class_based_cidr(ip):
    """Validate the IP class and return CIDR; raise error if not class A, B, or C or if it's loopback."""
    first_octet = int(ip.split('.')[0])
    if first_octet == 127:
        raise ValueError("Loopback addresses are not allowed.")
    if first_octet < 128:
        return 8  # Class A
    elif first_octet < 192:
        return 16  # Class B
    elif first_octet < 224:
        return 24  # Class C
    else:
        raise ValueError("Please type an IP address which is A or B or C class")
