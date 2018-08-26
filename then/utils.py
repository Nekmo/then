

def split_host_port(address, default_port=None):
    parts = list(address.split(':', 1))
    if len(parts) == 1:
        parts.append(default_port)
    return parts
