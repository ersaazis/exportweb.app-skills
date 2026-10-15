#!/usr/bin/env python3
"""
ExportWeb MCP Server Connection & Tool Verification CLI

Usage:
    python3 test_connection.py --url https://exportweb.app --token ew_sec_...
    python3 test_connection.py --url http://localhost:8080 --token ew_sec_... --call dashboard_stats
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def make_jsonrpc_request(url: str, token: str, method: str, params: dict, msg_id: int = 1) -> dict:
    endpoint = url.rstrip("/")
    if not endpoint.endswith("/mcp"):
        endpoint += "/mcp"

    payload = {
        "jsonrpc": "2.0",
        "id": msg_id,
        "method": method,
        "params": params,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "ExportWeb-Skills-Tester/1.0",
    }

    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        raw_err = e.read().decode("utf-8", errors="ignore")
        print(f"❌ HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        if raw_err:
            print(f"   Details: {raw_err[:300]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Connection failed: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Test ExportWeb MCP connection and list registered tools.")
    parser.add_argument(
        "--url",
        default=os.environ.get("EXPORTWEB_URL", "https://exportweb.app"),
        help="ExportWeb server base URL or /mcp endpoint (default: https://exportweb.app)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("EXPORTWEB_MCP_TOKEN", ""),
        help="MCP Bearer token (ew_sec_...). Can also be set via EXPORTWEB_MCP_TOKEN environment variable.",
    )
    parser.add_argument(
        "--call",
        help="Optional tool name to execute (e.g. dashboard_stats, languages_list, products_search)",
    )
    parser.add_argument(
        "--args",
        default="{}",
        help="JSON string of arguments when using --call (default: '{}')",
    )

    args = parser.parse_args()

    token = args.token.strip()
    if not token:
        print("❌ Error: Missing MCP secret token.", file=sys.stderr)
        print("   Provide --token ew_sec_... or set EXPORTWEB_MCP_TOKEN environment variable.", file=sys.stderr)
        print("   Obtain your token in ExportWeb Admin: /admin/account-settings", file=sys.stderr)
        sys.exit(1)

    print("=================================================================")
    print("🔌 ExportWeb MCP Server Connection Test")
    print(f"   Target URL: {args.url}")
    print(f"   Token Mask: {token[:10]}...{token[-6:] if len(token) > 16 else ''}")
    print("=================================================================\n")

    # Step 1: tools/list discovery
    print("[1/2] Testing 'tools/list' discovery...")
    discovery_res = make_jsonrpc_request(args.url, token, "tools/list", {}, msg_id=1)

    if "error" in discovery_res and discovery_res["error"]:
        err = discovery_res["error"]
        print(f"❌ MCP Protocol Error [{err.get('code')}]: {err.get('message')}")
        sys.exit(1)

    tools = discovery_res.get("result", {}).get("tools", [])
    print(f"✅ Success! Connected and discovered {len(tools)} registered tools:\n")

    # Display discovered tools grouped by domain
    categories = {
        "Assets": [],
        "Products": [],
        "Galleries": [],
        "Articles": [],
        "Inquiries": [],
        "Settings": [],
        "Languages": [],
        "Dashboard": [],
        "Other": [],
    }

    for t in tools:
        name = t.get("name", "")
        desc = t.get("description", "")
        prefix = name.split("_")[0].capitalize()
        matched = False
        for cat in categories:
            if prefix.startswith(cat):
                categories[cat].append((name, desc))
                matched = True
                break
        if not matched:
            categories["Other"].append((name, desc))

    for cat, items in categories.items():
        if items:
            print(f"  • {cat} ({len(items)} tools):")
            for t_name, t_desc in items:
                print(f"    - {t_name:<30} {t_desc[:65]}...")
            print()

    # Step 2: Test tool execution
    target_tool = args.call if args.call else "dashboard_stats"
    try:
        call_args = json.loads(args.args)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in --args: {args.args}", file=sys.stderr)
        sys.exit(1)

    print(f"[2/2] Testing tool execution: '{target_tool}'...")
    call_payload = {
        "name": target_tool,
        "arguments": call_args,
    }
    tool_res = make_jsonrpc_request(args.url, token, "tools/call", call_payload, msg_id=2)

    if "error" in tool_res and tool_res["error"]:
        err = tool_res["error"]
        print(f"❌ Tool Execution Error [{err.get('code')}]: {err.get('message')}")
        sys.exit(1)

    print(f"✅ Success! Tool '{target_tool}' responded with valid output:")
    print(json.dumps(tool_res.get("result", {}), indent=2))

    print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY! ExportWeb MCP server is ready for AI Agents.")


if __name__ == "__main__":
    main()
