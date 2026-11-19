# RiskOps Engine

**Cloud-deployed Risk Operations platform with automated CSV ingestion, real-time analytics, and an active FastAPI security middleware layer.**

RiskOps Engine combines operational risk data processing with defense-in-depth API security. Deployed on **AWS EC2** behind an **Nginx** reverse proxy, the platform processes structured CSV risk datasets through an interactive dashboard while actively inspecting incoming traffic for VPNs, proxies, and malicious payloads.

---

## Key Features

* **Risk Operations Dashboard:** Interactive interface for monitoring operational risk metrics, system status, and security telemetry.
* **Automated CSV Processing:** High-throughput ingestion and parsing pipeline for structured risk datasets.
* **Active Security Middleware (FastAPI):**
  * **VPN & Proxy Detection:** Identifies and flags anonymized or suspicious network origins before requests reach core application logic.
  * **Malicious Payload Inspection:** Scans incoming request payloads to block injection attempts and malformed inputs.
  * **Dynamic IP Blacklisting:** Mitigates repeated unauthorized access attempts by blacklisting offending IP addresses.
* **Production Cloud Architecture:** Deployed on AWS EC2 with Nginx handling reverse proxying and traffic routing to the FastAPI backend.

---

## System Architecture

```text
Client Request
      │
      ▼
[ Nginx Reverse Proxy (AWS EC2) ]
      │
      ▼
[ FastAPI Security Middleware ]
   ├── VPN / Proxy Detection
   ├── Malicious Payload Inspection
   └── Dynamic IP Blacklisting
      │ (Verified Traffic)
      ▼
[ Core RiskOps Engine ]
   ├── CSV Processing Pipeline
   └── RiskOps Dashboard API