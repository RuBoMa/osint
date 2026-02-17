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

