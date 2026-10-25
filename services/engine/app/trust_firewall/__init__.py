"""
Backward compatibility re-export shim: app.trust_firewall -> app.firewall
"""
from app.firewall.engine import ScientificTrustFirewallEngine
from app.firewall import engine, models

__all__ = ["ScientificTrustFirewallEngine", "engine", "models"]
