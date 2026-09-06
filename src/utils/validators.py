"""Input validation utilities."""

import re


def validate_ip(ip: str) -> bool:
    """Validate IP address (IPv4 or IPv6).
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid IP address
    """
    # IPv4
    ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    if re.match(ipv4_pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    # IPv6 (simplified)
    ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'
    return bool(re.match(ipv6_pattern, ip))


def validate_port(port: int) -> bool:
    """Validate port number.
    
    Args:
        port: Port number
        
    Returns:
        True if valid port (1-65535)
    """
    return 1 <= port <= 65535


def validate_hostname(hostname: str) -> bool:
    """Validate hostname.
    
    Args:
        hostname: Hostname string
        
    Returns:
        True if valid hostname
    """
    # Allow alphanumeric, hyphens, dots, and underscores
    pattern = r'^(?!-)[a-zA-Z0-9_-]{1,63}(?<!-)(\\.(?!-)[a-zA-Z0-9_-]{1,63}(?<!-))*$'
    return bool(re.match(pattern, hostname))
