"""
ZMIE AI Context Firewall & Prompt Injection Defense Engine
Enforces:
- Sanitization of retrieved web / document content (treating all external text strictly as data, never instructions)
- Strips prompt injection attacks ('ignore previous instructions', system prompt extraction)
- Strict AI tool argument validation and loop budgets
- Level 0 to Level 4 autonomy boundaries (prohibits autonomous prescribing or diagnosing)
"""

import re
from typing import Dict, Any, List, Tuple


class AIContextFirewall:
    """
    Guards AI reasoning layers against malicious prompt injection and untrusted source manipulation.
    """

    # Adversarial prompt injection patterns
    INJECTION_PATTERNS = [
        r'ignore\s+(?:all\s+)?previous\s+instructions',
        r'disregard\s+(?:all\s+)?prior\s+prompts',
        r'reveal\s+(?:your\s+)?system\s+prompt',
        r'output\s+(?:your\s+)?initial\s+instructions',
        r'you\s+are\s+now\s+in\s+developer\s+mode',
        r'act\s+as\s+an\s+unrestricted\s+ai',
        r'bypass\s+(?:safety\s+)?filters'
    ]

    @classmethod
    def sanitize_untrusted_content(cls, raw_text: str) -> Tuple[str, bool]:
        """
        Cleans and defangs untrusted external sources.
        Returns: (sanitized_text, injection_detected)
        """
        injection_found = False
        cleaned_text = raw_text

        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, cleaned_text, re.IGNORECASE):
                injection_found = True
                cleaned_text = re.sub(pattern, "[UNTRUSTED_INSTRUCTION_STRIPPED_BY_ZMIE_FIREWALL]", cleaned_text, flags=re.IGNORECASE)

        # Strip dangerous HTML/executable tags
        cleaned_text = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
        cleaned_text = re.sub(r'<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>', '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)

        return cleaned_text, injection_found

    @classmethod
    def enforce_autonomy_boundary(cls, action_name: str) -> bool:
        """
        Hard block on prohibited autonomous clinical and administrative actions:
        ZMIE must never autonomously prescribe, diagnose, change medication, or approve knowledge releases.
        """
        prohibited_actions = [
            "prescribe_medication",
            "diagnose_patient",
            "sign_clinical_chart",
            "approve_treatment",
            "change_security_policy",
            "grant_admin_access"
        ]
        if action_name.lower() in prohibited_actions:
            return False  # Blocked by Level 2 autonomy boundary
        return True
