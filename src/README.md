# osint-master

A small OSINT helper project.

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

6) Deactivate when done

```zsh
deactivate
```

Notes & troubleshoot
- Prefer Homebrew or pyenv-managed Python over the Apple-supplied system Python.
- If you want a specific Python version, install it with `pyenv` and create the venv from that interpreter.
- If you see errors about "ensurepip" or "venv" missing, reinstall Python via Homebrew.

# osint-master

For this project VM is highly recommended for several reasons:

**IP Reputation Protection:** OSINT activities generate many queries to external services. Your personal IP could be flagged, rate-limited, or blocklisted by security systems if running directly on your main machine. A VM's IP is isolated and easier to reset if needed.

**Credential Isolation:** If your OSINT tool gets compromised or has a vulnerability, any API keys stored in the VM remain isolated from your personal system where you might have banking, email, or other critical credentials.

**System Safety:** OSINT tools might interact with potentially malicious or flagged domains/IPs. A VM prevents malware or network attacks from reaching your main system.

**Traffic Analysis:** VMs allow you to easily monitor what data the tool sends/receives without it being mixed with your personal traffic. Useful for debugging and auditing the tool's behavior.

**Clean State:** You can take snapshots and reset the VM to a known good state for testing, without affecting your actual working environment.

**Plausible Deniability:** In some jurisdictions, activities in a sandboxed VM are easier to justify as isolated research vs. personal system profiling.
