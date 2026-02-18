import argparse
import os
from tools.domain import domain_enum
from tools.ip_address import lookup_ip
from tools.username import format_username_results, search_username
from utils.pdf import save_as_pdf
from utils.validators import resolve_target
from utils.formatters import format_ip

OUTPUT_DIR = "output"

def parse_args():
    usage_examples = """
Usage Examples:
    
  Search for information by IP address:
    python3 master.py -i 192.168.1.1 -o output_ip
    
  Search for information by username:
    python3 master.py -u @john_doe -o output_username
    
  Enumerate subdomains and check for takeover risks:
    python3 master.py -d example.com -o output_domain
    
  Generate PDF output:
    python3 master.py -i 192.168.1.1 -o output_ip --pdf
    """
    
    parser = argparse.ArgumentParser(
        description="Welcome to OSINT-Master",
        epilog=usage_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-i", "--ipaddress", help="Search for information by IP address")
    parser.add_argument("-u", "--username", help="Search for information by username")
    parser.add_argument("-d", "--domain", help="Enumerate subdomains and check for takeover risks")
    parser.add_argument("-o", "--output", help="Output file name (without extension)")
    parser.add_argument("-p", "--pdf", action="store_true", help="Export results as PDF instead of text")

    return parser.parse_args()


def main():
    args = parse_args()
    result_text = None  # store final printable output

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
    
    # Handle username search
    elif args.username:
        data = search_username(args.username)
        result_text = format_username_results(data)
        print(result_text)
        
    # Handle domain enumeration
    elif args.domain:
        results = domain_enum(args.domain)

        output_lines = []
        output_lines.append(f"Domain Enumeration Results for {args.domain}")
        output_lines.append("-" * 50)

        for r in results:
            output_lines.append(f"Subdomain: {r['subdomain']}")
            output_lines.append(f"  IP: {r['ip']}")
            output_lines.append(f"  Possible Takeover: {r['possible_takeover']}")

            ssl_info = r.get("ssl")
            if ssl_info:
                issuer = ssl_info.get('issuer', {})
                country = issuer.get('countryName', 'Unknown')
                org = issuer.get('organizationName', 'Unknown')
                cn = issuer.get('commonName', 'Unknown')
                issuer_str = f"{org} ({country}) - {cn}"
                output_lines.append(f"  SSL Issuer: {issuer_str}")
                output_lines.append(f"  SSL Expiry: {ssl_info.get('notAfter')}")

            output_lines.append("")

        result_text = "\n".join(output_lines)
        print(result_text)
    
    else:
        print("No search criteria provided. Use -h for help.")

    # Save output to file
    if args.output and result_text:
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            
            # Determine file extension based on --pdf flag
            if args.pdf:
                file_path = os.path.join(OUTPUT_DIR, f"{args.output}.pdf")
                save_as_pdf(file_path, result_text)
            else:
                file_path = os.path.join(OUTPUT_DIR, f"{args.output}.txt")
                with open(file_path, "w") as f:
                    f.write(result_text)
            
            print(f"Results saved to {file_path}")
        except (IOError, OSError, PermissionError) as e:
            print(f"Error writing file: {str(e)}")
        except ImportError as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
