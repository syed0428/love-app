import subprocess
import os
import sys

# 1. Get token securely from Git Credential Manager in memory (never written to file)
proc = subprocess.run(
    ["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n",
    text=True,
    capture_output=True,
    check=True
)

token = None
for line in proc.stdout.splitlines():
    if line.startswith("password="):
        token = line.split("=", 1)[1].strip()
        break

if not token:
    print("Could not retrieve token from Git Credential Manager.")
    sys.exit(1)

print("Retrieved token securely from Git Credential Manager.")

# 2. Re-initialize git repository
commands = [
    ["git", "init"],
    ["git", "config", "user.name", "Syed Umar"],
    ["git", "config", "user.email", "syedmohammedumar28@gmail.com"],
    ["git", "branch", "-M", "main"],
    ["git", "add", "."],
    ["git", "commit", "-m", "Initial commit: Love App romantic keepsake book"]
]

for cmd in commands:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Ran: {' '.join(cmd)}")
    if r.returncode != 0 and "nothing to commit" not in r.stderr:
        print("Error:", r.stderr)

# 3. Push to GitHub
push_url = f"https://syed0428:{token}@github.com/syed0428/love-app.git"
print("Pushing to https://github.com/syed0428/love-app.git (main)...")

push_proc = subprocess.run(
    ["git", "push", push_url, "main", "--force"],
    capture_output=True,
    text=True
)

print("Push return code:", push_proc.returncode)
if push_proc.stdout:
    print("STDOUT:", push_proc.stdout)
if push_proc.stderr:
    # Filter token from output just to be safe
    safe_err = push_proc.stderr.replace(token, "***")
    print("STDERR:", safe_err)

# Set clean origin url without token
subprocess.run(["git", "remote", "add", "origin", "https://github.com/syed0428/love-app.git"])
print("\nDone! Remote set to https://github.com/syed0428/love-app.git")
