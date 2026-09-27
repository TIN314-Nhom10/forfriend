"""Patch @react-router/dev to fix Bun restart loop on Windows.

Bug: @react-router/dev v8.4.0 uses Node.js --conditions flag which Bun
doesn't support, causing an infinite restart loop and crash.

Fix: Replace `if (developmentConditionEnabled)` with `if (true)` in the
CLI index.js to bypass the restart mechanism entirely.
"""
from pathlib import Path

CLI_PATH = (
    Path(__file__).parent
    / ".web"
    / "node_modules"
    / "@react-router"
    / "dev"
    / "dist"
    / "cli"
    / "index.js"
)

TARGET = "if (developmentConditionEnabled) {"
REPLACEMENT = "if (true) { // PATCHED: bypass Bun --conditions bug"


VITE_CONFIG_PATH = Path(__file__).parent / ".web" / "vite.config.js"


def patch_vite_lan():
    if not VITE_CONFIG_PATH.exists():
        return False
    content = VITE_CONFIG_PATH.read_text(encoding="utf-8")
    if 'host: "0.0.0.0"' in content:
        print("[patch] Vite already configured for LAN (0.0.0.0)")
        return True
    
    target_server = "server: {"
    replacement_server = 'server: {\n    host: "0.0.0.0",'
    if target_server in content:
        patched = content.replace(target_server, replacement_server, 1)
        VITE_CONFIG_PATH.write_text(patched, encoding="utf-8")
        print("[patch] Successfully added host: 0.0.0.0 to vite.config.js for LAN access")
        return True
    return False


def patch():
    if not CLI_PATH.exists():
        print("[patch] react-router CLI not found — skipping (run reflex init first)")
    else:
        content = CLI_PATH.read_text(encoding="utf-8")
        if TARGET not in content:
            if "if (true)" in content:
                print("[patch] react-router already patched — skipping")
            else:
                print("[patch] WARNING: Could not find target string to patch")
        else:
            patched = content.replace(TARGET, REPLACEMENT, 1)
            CLI_PATH.write_text(patched, encoding="utf-8")
            print("[patch] Successfully patched @react-router/dev for Bun compatibility")

    patch_vite_lan()
    return True


if __name__ == "__main__":
    patch()
