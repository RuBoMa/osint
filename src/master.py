import argparse
import os
from tools.ip_address import lookup_ip, format_ip, resolve_target

OUTPUT_DIR = "output"

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
    result_text = None #store final printable output

    # Handle IP address lookup
    if args.ipaddress:
        resolved = resolve_target(args.ipaddress)
        if error := resolved.get("error"):
            print(f"Error: {error}")
            return
        
        output = lookup_ip(resolved["ip"])
        result = format_ip(output)
        print(result)
        result_text = result
        # print(f"IP Address search: {args.ipaddress}")
    
    # Handle username search
    elif args.username:
        print(f"Username search: {args.username}")
    
    # Handle domain enumeration
    elif args.domain:
        print(f"Domain enumeration: {args.domain}")
    
    else:
        print("No search criteria provided. Use -h for help.")


    if args.output and result_text:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_path = os.path.join(OUTPUT_DIR, args.output)

    with open(file_path, "w") as f:
        f.write(result_text)

    print(f"Results saved to {file_path}")

if __name__ == "__main__":
    main()