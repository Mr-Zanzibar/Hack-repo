import socket
import common_ports # may have problems
import re


def check_valid_ip(ip_address: str):
    """ This tool will run a port scan in the given target and port range. """
    valid_ip = False
    error = None

    try:
        socket.inet_aton(ip_address)
        valid_ip = True

    except Exception:
        error = "Error: Invalid IP address"

    return valid_ip, error


def connection_check(target: str, port: str) -> bool:

    # Initialize the socket.
    socket.setdefaulttimeout(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    found = False

    try:
        sock.connect((target, port))
        found = True

    except ConnectionRefusedError:
        pass

    except socket.timeout:
        pass

    finally:
        sock.close()

    return found


def verbose_output(ip_address: str, hostname: str, open_ports: list) -> str:

    if hostname != "":
        response = f"Open ports for {hostname} ({ip_address})"
    else:
        response = f"Open ports for {ip_address}"
        
    response += f"\nPORT     SERVICE"

    for port in open_ports:
        try:
            response += f"\n{port:<5}    {common_ports.ports_and_services[port]}"
        except KeyError:
            response += f"\n{port:<5}"

    return response


def get_hostname_and_address(target: str):

    regex = r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"

    ip_address = ""
    hostname = ""
    error = None

    # Check the target is IP or hostname
    if re.search(regex, target):

        # Use the validator for IP of socket
        valid_ip, error = check_valid_ip(target)

        if valid_ip:
            ip_address = target

            # Try to retrieve the hostname for the IP provided
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
            except socket.herror:
                pass

    else:
        try:
            ip_address = socket.gethostbyname(target)
            hostname = target

        except socket.gaierror:
            error = "Error: Invalid hostname"

    return ip_address, hostname, error


def get_open_ports(target: str, port_range: list, verbose=False):


    open_ports = []

    ip_address, hostname, error = get_hostname_and_address(target)

    if error:
        return error

    # Run the port scanner for port range
    for port in range(port_range[0], port_range[1]+1):

        # If successful append to open port list
        if connection_check(ip_address, port):
            open_ports.append(port)

    if verbose:
        return verbose_output(ip_address, hostname, open_ports)
    else:
        return(open_ports)
