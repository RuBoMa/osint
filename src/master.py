import argparse
from tools.ip_address import lookup_ip, format_ip

def parse_args():
    usage_examples = """
Usage Examples:
    
  Search for information by IP address:
    python3 OSINT-Master.py -i 192.168.1.1
    
  Search for information by username:
    python3 OSINT-Master.py -u @john_doe
    
  Enumerate subdomains and check for takeover risks:
    python3 OSINT-Master.py -d example.com
    """
    
    parser = argparse.ArgumentParser(
        description="Welcome to OSINT-Master",
        epilog=usage_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-i", "--ipaddress", help="Search for information by Ip address")

    parser.add_argument("-u", "--username", help="Search for information by username")

    parser.add_argument("-d", "--domain", help="Enumerate subdomains and check for takeover risks")

    parser.add_argument("-o", "--output", help="Output file")


    return parser.parse_args()


def main():
    args = parse_args()
    
    # Handle IP address lookup
    if args.ipaddress:
        result = lookup_ip(args.ipaddress)
        output = format_ip(result)
        print(output)
        # print(f"IP Address search: {args.ipaddress}")
    
    # Handle username search
    elif args.username:
        print(f"Username search: {args.username}")
    
    # Handle domain enumeration
    elif args.domain:
        print(f"Domain enumeration: {args.domain}")
    
    else:
        print("No search criteria provided. Use -h for help.")


    if getattr(args, "output", None):
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()