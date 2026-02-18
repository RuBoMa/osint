# osint-master

A small OSINT helper project.

**Prerequisites**
Python 3.8+ (Recommended 3.11), pip, Homebrew.

## Setting up the environment

Follow these steps once to create and use a Python virtual environment for this project.

1) Check Python and venv availability

```zsh
python3 --version
python3 -m venv --help
```

2) (Optional) Install/upgrade Python via Homebrew

If you don't have a recent Python 3, install it with Homebrew:

```zsh
brew install python
```

3) Create a virtual environment (from the project root)

```zsh
cd /Users/roope/Desktop/osint
python3 -m venv .venv
```

4) Activate the virtual environment (zsh)

```zsh
source .venv/bin/activate
# prompt shows (.venv)
```

5) Upgrade pip and install dependencies

```zsh
pip install --upgrade pip
pip install -r src/requirements.txt
```
Configuration (.env / API keys)
--------------------------------

This project uses external APIs to gather OSINT data. Store all API keys in a `.env`
file in the repository root. The project reads these via `python-dotenv`.
**Important:** Never commit `.env` to version control. Add it to `.gitignore`.

### API Providers & Configuration

#### 1. IPinfo.io (IP Geolocation & ISP Data)
**Purpose:** Provides geolocation, ISP, AS, organization, proxy, and hosting status for IP addresses.

- **Signup:** https://ipinfo.io/signup
- **Free tier:** 50,000 requests/month
- **Paid tiers:** start at $8/month for 1M requests
- **Environment variable:** `IPINFO_TOKEN`
- **Used by:** `src/tools/ip_address.py` → `lookup_ipinfo()`

**Example curl:**
```bash
curl "https://ipinfo.io/1.1.1.1?token=YOUR_IPINFO_TOKEN"
```

**Sample response:**
```json
{
  "ip": "1.1.1.1",
  "city": "Los Angeles",
  "country": "US",
  "isp": "APNIC",
  "org": "AS13335 Cloudflare Inc",
  "as": "AS13335",
  "proxy": false,
  "hosting": true
}
```

#### 2. AbuseIPDB (IP Reputation & Abuse History)
**Purpose:** Provides abuse confidence score, historical reports, and last-reported-at timestamp.

- **Signup:** https://www.abuseipdb.com/register
- **Free tier:** 1,000 requests/day
- **Paid tiers:** start at $5/month for 10K requests/day
- **Environment variable:** `ABUSEIPDB_API_KEY`
- **Used by:** `src/tools/ip_address.py` → `lookup_abuse()`

**Example curl:**
```bash
curl -X GET "https://api.abuseipdb.com/api/v2/check" \
  -H "Key: YOUR_ABUSEIPDB_API_KEY" \
  -H "Accept: application/json" \
  -d "ipAddress=1.1.1.1&maxAgeInDays=90"
```

**Sample response (data field):**
```json
{
  "abuseConfidenceScore": 0,
  "totalReports": 0,
  "lastReportedAt": null,
  "usageType": "Content Delivery Network",
  "isp": "APNIC",
  "domain": "cloudflare.com"
}
```

#### 3. Social Platforms & Public APIs (Username Lookup)
**Purpose:** Check username presence and retrieve public profile info across platforms.

Platforms checked (no API key required for most):
- **GitHub API:** https://api.github.com/users/{username}
- **Reddit API:** https://www.reddit.com/user/{username}/about.json
- **StackOverflow:** https://api.stackexchange.com/2.3/users (rate: 300/day without key)
- **GitLab:** https://gitlab.com/api/v4/users
- **Dev.to:** https://dev.to/api/users/by_username

**Used by:** `src/tools/username.py` → `search_username()`, individual platform functions

**Rate limits:** Vary by platform (typically 10–300 requests/day for public endpoints without auth).

#### 4. Domain Enumeration & Certificate APIs
**Purpose:** Discover subdomains, retrieve SSL/TLS certificate metadata, and check for takeover risks.

**Data sources used:**
- DNS queries (dnspython library — no API key, direct protocol)
- SSL certificate transparency logs (via curl/requests — no API key)

**Used by:** `src/tools/domain.py` → `lookup_domain()`, helper functions

**Rate limits:** None (local DNS queries), but external WHOIS or CT log queries may have soft limits.
Store API keys and configuration in a `.env` file in the repository root. The
project reads these via `python-dotenv`. Example `.env` (do NOT commit secrets):

```env
IPINFO_TOKEN=your_ipinfo_token_here
ABUSEIPDB_API_KEY=your_abuseipdb_key_here
# Add other API keys if you use additional providers
```

For this project VM is highly recommended for several reasons:

**IP Reputation Protection:** OSINT activities generate many queries to external services. Your personal IP could be flagged, rate-limited, or blocklisted by security systems if running directly on your main machine. A VM's IP is isolated and easier to reset if needed.

**Credential Isolation:** If your OSINT tool gets compromised or has a vulnerability, any API keys stored in the VM remain isolated from your personal system where you might have banking, email, or other critical credentials.

**System Safety:** OSINT tools might interact with potentially malicious or flagged domains/IPs. A VM prevents malware or network attacks from reaching your main system.

**Traffic Analysis:** VMs allow you to easily monitor what data the tool sends/receives without it being mixed with your personal traffic. Useful for debugging and auditing the tool's behavior.

**Clean State:** You can take snapshots and reset the VM to a known good state for testing, without affecting your actual working environment.

**Plausible Deniability:** In some jurisdictions, activities in a sandboxed VM are easier to justify as isolated research vs. personal system profiling.

A compact OSINT helper written in Python. It contains setup and usage instructions, a troubleshooting
section.

**Table of contents**
- Project snapshot
- Setting up the environment
- Configuration (.env / API keys)
- Usage and examples
- Output and storage
- Troubleshooting and known issues
- Design & implementation notes
- Ethical and legal guidance
- Audit checklist (complete with mapping to repo artifacts)

**Project snapshot**
----------------
Purpose: collect public information about IP addresses, usernames and domains using
APIs and lightweight custom logic. This repository contains the source under
`src/` and example output under `src/output/`.

Repository structure (key files)
- `README.md` - this document (you are reading it)
- `src/` - application source
	- `master.py` - CLI entrypoint
	- `tools/` - modules for IP, username and domain lookups (e.g., `ip_address.py`)
	- `utils/` - helper utilities (e.g., `http_client.py`)
- `src/requirements.txt` - Python dependencies
- `src/output/` - default location for saved results (CLI `-o` option writes here)


**Usage**
-----
Run the CLI from the `src/` directory. Use `-h`/`--help` for all options:

```zsh
python3 master.py -h

options:
  -h, --help            show this help message and exit
  -i, --ipaddress 		Search for information by Ip address
  -u, --username 		Search for information by username
  -d, --domain 			Enumerate subdomains and check for takeover risks
  -o, --output 			Output file
```

Primary options (examples):
- IP lookup
	```zsh
	python3 master.py -i 1.1.1.1 -o output.txt
	```

- Username lookup
	```zsh
	python3 master.py -u someuser -o output.txt
	```

- Domain enumeration / subdomain checks
	```zsh
	python3 master.py -d example.com -o output.txt
	```

Output and format
-----------------
By default the CLI writes its formatted results to the file given with `-o`.
Typical output fields per tool:
- IP lookup: ip, country, city, isp, org, as, proxy, hosting, abuse_score, total_reports, last_reported
- Username lookup: platform checks, profile metadata (username found, display name/bio, follower counts when public)
- Domain enumeration: discovered subdomains, IP addresses, SSL certificate metadata, notes about potential takeover risk

Example: `output.txt` will contain a human-readable list like:

```
IP Address: 1.1.1.1
Country: US
City: ...
ISP: Cloudflare, Inc.
Abuse Score: 0
...
```

Troubleshooting & common issues
-------------------------------
- Warning about LibreSSL/urllib3: you may see a warning like
	``NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL'``.
	- Best fix: recreate the venv using a Homebrew or pyenv-built Python that's linked to OpenSSL. Example:

```zsh
brew install python
rm -rf .venv
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
```

- Missing API keys: If `IPINFO_TOKEN` or `ABUSEIPDB_API_KEY` are not set, the relevant
	calls will fail or return API error messages. Create a `.env` file as described above.

- Network/timeout errors: The code uses `requests` with short timeouts (5s). If you see
	timeouts, verify connectivity and try again later.

- JSON parse errors: If an API returns an HTML/web page (rate-limited or error page),
	the tool may raise JSON decode errors. The developer should check the
	HTTP status code and response body in that case.

**Design & implementation notes**
------------------------------
- The project implements custom logic to call APIs and format results.
**Modules of interest:**
	- `src/tools/ip_address.py` — validates IPs, calls ipinfo and AbuseIPDB, and formats output.
	- `src/tools/username.py` — checks social platforms for username presence.
	- `src/tools/domain.py` — enumerates subdomains and gathers metadata (DNS, SSL, takeover checks).
- Error handling: callers should expect `lookup_*` functions to return `{'error': '...'} on failure.
- Rate limits: the README documents known limitations (APIs may rate-limit) and suggests caching or staggered requests for large-scale scans.

**Ethical and legal guidance**
--------------------------
This tool only collects publicly available information. Responsible use is required.

**Guidelines:**
- Only run this tool against targets you own or have explicit permission to test.
- Do not use the tool to harass, stalk, or dox individuals.
- Respect API Terms of Service for each provider used.
- For audits or testing use an isolated environment (VM) and avoid running scans from
	production networks.


**Known limitations**
- API rate limits and request caps — the tool does not implement advanced rate-limiting or request scheduling.
- Data accuracy depends entirely on the external providers used (ipinfo, AbuseIPDB, platform APIs).
- Some features (e.g., full username profile scraping) depend on the public availability of the data and may be limited by API access.
