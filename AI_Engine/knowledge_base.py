# This file holds our "rules" - the knowledge the AI uses to reason.
# Think of each rule as: IF (condition) THEN (conclusion)

def classify_attack(attack_type: str, failed_attempts: int) -> str:
    """
    Determines the specific classification of the attack
    based on simple facts we know about it.
    """
    if attack_type.lower() == "brute force" and failed_attempts and failed_attempts > 10:
        return "Brute Force Attack (confirmed)"

    if attack_type.lower() == "sql injection":
        return "SQL Injection Attempt"

    if attack_type.lower() == "malware":
        return "Malware Detected"

    if attack_type.lower() == "ddos":
        return "DDoS Attack"

    if attack_type.lower() == "port scan":
        return "Port Scanning Activity"

    if attack_type.lower() == "phishing":
        return "Phishing Attempt"

    return "Unclassified Incident"


def determine_severity(classification: str, target_asset: str) -> str:
    """
    Decides how severe the incident is, based on what
    it was classified as and what it targeted.
    """
    high_risk_targets = ["admin", "root", "database", "server"]

    is_high_value_target = False
    if target_asset:
        is_high_value_target = any(word in target_asset.lower() for word in high_risk_targets)

    if "confirmed" in classification.lower() and is_high_value_target:
        return "CRITICAL"

    if "confirmed" in classification.lower():
        return "HIGH"

    if classification == "Unclassified Incident":
        return "LOW"

    return "MEDIUM"