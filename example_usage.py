# -*- coding: utf-8 -*-
"""
Example usage of GenParkAgenticCommerceAgentGatewayVerifier
Demonstrates retailer gateway authentication across legitimate agents and scraper bots.
"""

from client import GenParkAgenticCommerceAgentGatewayVerifier

def main():
    verifier = GenParkAgenticCommerceAgentGatewayVerifier()

    requests = [
        {
            "name": "Traffic A: Authenticated Perplexity Shopping Agent with Delegation Token",
            "agent_id": "PERPLEXITY-COMMERCE-AGENT-X",
            "token": "POD-SECURE-USER-DELEGATED-2026-X89",
            "latencies": [320.0, 740.0, 510.0, 1100.0, 480.0],
            "skus": 2
        },
        {
            "name": "Traffic B: Malicious Scraper with Robotic Constant Latency & No Token",
            "agent_id": "UNKNOWN-SCRAPER-BOT",
            "token": "",
            "latencies": [50.0, 50.0, 50.0, 50.0, 50.0],
            "skus": 2500
        }
    ]

    print("================================================================")
    print("GenPark Agentic Commerce Agent Gateway Verifier - Live Runs")
    print("================================================================\n")

    for r in requests:
        res = verifier.verify_agent_traffic(
            agent_identifier=r["agent_id"],
            proof_of_delegation_token=r["token"],
            request_latency_history_ms=r["latencies"],
            requested_sku_count=r["skus"]
        )
        print(f"[{r['name']}]")
        print(f"  Agent Identifier      : {res['agent_identifier']}")
        print(f"  Gateway Verdict       : {res['gateway_status']} [{res['traffic_classification']}]")
        print(f"  Proof of Delegation   : {res['proof_of_delegation_verified']}")
        print(f"  Allowance Tier        : {res['rate_limit_allowance_tier']} ({res['allocated_rate_limit_rps']} RPS)")
        print(f"  Arrival Entropy       : {res['arrival_entropy_score']}")
        print(f"  Access Ticket ID      : {res['gateway_access_ticket_id']}\n")

if __name__ == "__main__":
    main()
