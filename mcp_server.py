# -*- coding: utf-8 -*-
"""
GenPark Agentic Commerce Agent Gateway Verifier MCP Server
Exposes retailer Agent Gateway proof-of-delegation tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkAgenticCommerceAgentGatewayVerifier

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-agent-gateway-verifier", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "verify_agent_traffic",
                        "description": "Authenticates legitimate consumer shopping agents and prevents scraper abuse using cryptographic proof-of-delegation.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "agent_identifier": {"type": "string"},
                                "proof_of_delegation_token": {"type": "string"},
                                "requested_sku_count": {"type": "integer"}
                            },
                            "required": ["agent_identifier", "proof_of_delegation_token"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "verify_agent_traffic":
            verifier = GenParkAgenticCommerceAgentGatewayVerifier()
            res = verifier.verify_agent_traffic(
                agent_identifier=args.get("agent_identifier", "Agent-Copilot-99"),
                proof_of_delegation_token=args.get("proof_of_delegation_token", "POD-AUTH-TOKEN-1234567890"),
                requested_sku_count=args.get("requested_sku_count", 1)
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        v = GenParkAgenticCommerceAgentGatewayVerifier()
        test_res = v.verify_agent_traffic("Agent-Test", "POD-VALID-DELEGATION-TOKEN-99")
        print(f"Test Gateway Status: {test_res['gateway_status']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
