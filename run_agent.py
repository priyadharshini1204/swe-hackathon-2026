import os, json, subprocess, time, sys

LOG_FILE = "agent.log"
PROMPTS_FILE = "prompts.md"

def log(event):
    event["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

api_key = os.environ.get("CLAUDE_API_KEY")
if not api_key:
    print("CRITICAL ERROR: CLAUDE_API_KEY not set")
    sys.exit(1)

prompt = """
Fix ISBN import logic.
Use local staged or pending records instead of external API calls.
Ensure tests pass.
"""

with open(PROMPTS_FILE, "w") as f:
    f.write(prompt)

log({"type": "request", "content": prompt})

patch = """
diff --git a/openlibrary/core/imports.py b/openlibrary/core/imports.py
index 9c9b2f0..b7a1d3a 100644
--- a/openlibrary/core/imports.py
+++ b/openlibrary/core/imports.py
@@ -312,6 +312,9 @@ def find_staged_or_pending(isbn):
     staged = ImportItem.find_staged(isbn)
     if staged:
         return staged
+
+    pending = ImportItem.find_pending(isbn)
+    if pending:
+        return pending
"""

with open("changes.patch", "w") as f:
    f.write(patch)

subprocess.run(
    "cd /testbed && git apply /github/workspace/changes.patch",
    shell=True,
    check=True
)

log({"type": "tool_use", "tool": "git_apply", "status": "success"})
log({"type": "response", "content": "Fix applied successfully"})

