#!/usr/bin/env python3
"""
Auto-generated eval script for: DM Variation Generator
DO NOT MODIFY during autoresearch loop — this is the read-only judge.

Assertions:
1. First line under 100 characters
2. Contains a personalization token (name, company, role, or specific detail)
3. Ends with a question (not a statement)
4. Under 300 words total
5. No buzzwords from banned list
"""

import sys
import os
import re
import json


# --- Assertion Functions ---

def check_first_line_length(text, test_case=None):
    """Is the first line (hook) under 100 characters?"""
    lines = text.strip().split('\n')
    first_line = lines[0].strip() if lines else ""
    return len(first_line) <= 100


def check_personalization(text, test_case=None):
    """Does the DM contain a personalization signal?
    Proxy: references a specific detail from the test case (name, company, role, industry, or recent activity).
    At least 1 signal must appear.
    """
    if not test_case:
        return False
    signals = 0
    text_lower = text.lower()
    # Check if lead name appears
    lead_name = test_case.get("lead_name", "")
    if lead_name and lead_name.lower().split()[0] in text_lower:
        signals += 1
    # Check if company name appears
    company = test_case.get("company", "")
    if company and company.lower() in text_lower:
        signals += 1
    # Check if role/title keywords appear
    role = test_case.get("role", "")
    if role:
        role_words = [w.lower() for w in role.split() if len(w) > 3]
        if any(w in text_lower for w in role_words):
            signals += 1
    # Check if industry appears
    industry = test_case.get("industry", "")
    if industry and industry.lower() in text_lower:
        signals += 1
    return signals >= 1


def check_ends_with_question(text, test_case=None):
    """Does the DM end with a question (not a statement)?"""
    stripped = text.strip()
    # Find the last substantive sentence
    sentences = [s.strip() for s in re.split(r'[.!?]', stripped) if s.strip()]
    if not sentences:
        return False
    # The last sentence of the text should end with a question mark
    return stripped.endswith("?")


def check_word_count(text, test_case=None):
    """Is the DM under 300 words?"""
    words = text.split()
    return len(words) <= 300


def check_no_buzzwords(text, test_case=None):
    """Does the DM avoid overused buzzwords?"""
    buzzwords = [
        "synergy", "leverage", "utilize", "paradigm", "scalable", "disruptive",
        "revolutionary", "game-changer", "game changer", "cutting-edge",
        "best-in-class", "world-class", "thought leader", "thought leadership",
        "circle back", "move the needle", "bandwidth", "low-hanging fruit",
        "boil the ocean", "deep dive", "pivot", "ecosystem", "holistic",
        "seamless", "robust", "dynamic", "innovative solution", "value-add",
        "empower", "proactive", "actionable", "streamline"
    ]
    text_lower = text.lower()
    found = [b for b in buzzwords if b in text_lower]
    return len(found) == 0


# --- Main Eval ---

ASSERTIONS = [
    "first_line_length",
    "personalization",
    "ends_with_question",
    "word_count",
    "no_buzzwords",
]


def evaluate_output(text, test_case):
    """Run all assertions on a single output. Returns dict of assertion_name: bool."""
    return {
        "first_line_length": check_first_line_length(text, test_case),
        "personalization": check_personalization(text, test_case),
        "ends_with_question": check_ends_with_question(text, test_case),
        "word_count": check_word_count(text, test_case),
        "no_buzzwords": check_no_buzzwords(text, test_case),
    }


def main():
    outputs_dir = sys.argv[1] if len(sys.argv) > 1 else "outputs"

    # Load test cases
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_cases_path = os.path.join(script_dir, "test_cases.json")
    if not os.path.exists(test_cases_path):
        test_cases_path = "test_cases.json"

    with open(test_cases_path) as f:
        test_cases = json.load(f)

    total_pass = 0
    total = 0
    assertion_totals = {a: 0 for a in ASSERTIONS}

    for i, tc in enumerate(test_cases):
        # Handle both .md and .txt output extensions
        output_file = os.path.join(outputs_dir, f"output_{i:02d}.md")
        if not os.path.exists(output_file):
            output_file = os.path.join(outputs_dir, f"output_{i:02d}.txt")
        if not os.path.exists(output_file):
            continue

        with open(output_file) as f:
            text = f.read().strip()

        results = evaluate_output(text, tc)
        all_pass = all(results.values())

        if all_pass:
            total_pass += 1
        total += 1

        for a, passed in results.items():
            if passed:
                assertion_totals[a] += 1

        status = "PASS" if all_pass else "FAIL"
        failed = [k for k, v in results.items() if not v]
        print(f"  Output {i:02d}: {status}" + (f"  (failed: {', '.join(failed)})" if failed else ""))

    if total == 0:
        print("ERROR: No output files found")
        sys.exit(1)

    pass_rate = total_pass / total
    print(f"\n--- Assertion Breakdown ({total} outputs) ---")
    for a in ASSERTIONS:
        pct = assertion_totals[a] / total * 100
        print(f"  {a}: {assertion_totals[a]}/{total} ({pct:.0f}%)")

    print(f"\n--- Result ---")
    print(f"DETAIL {total_pass}/{total} outputs passed ALL assertions")
    print(f"METRIC pass_rate={pass_rate:.4f}")


if __name__ == "__main__":
    main()
