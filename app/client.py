import json
import requests

# The server endpoints (local)
url = "http://localhost:8000/predict"

FEATURES = [
    "Income"
    "Education_2",
    "Education_3",
    "Family_2",
    "Family_3",
    "Family_4",
    "CD Account_1",
]


def ask_float(prompt):
    while True:
        try:
            val = float(input(prompt).strip())
            return val
        except ValueError:
            print("Please enter a valid number.")

def ask_in_in(prompt,allowed):
    while True:
        try:
            val = int(input(prompt).strip())
            if val in allowed:
                return val
            print(f"Please enter one of {allowed}.")
        except:
            print("Please enter an integer.")

def ask_yes_no(prompt):
    while True:
            val = input(prompt).strip().lower()
            if val in ["y","yes"]:
                return 1
            if val in ["n","no"]:
                return 0
            print("Please answer Y/N.")

def build_feature():
    print("\n=== Loan Acceptance Screening ===")

    # Income
    income = ask_float("Annual income (e.g., 110 for $110k)")

    # Education
    print("\nEducation level:")
    print("  1 = Undergraduate")
    print("  2 = Graduate")
    print("  3 = Advanced/Professional")
    edu = ask_int_in("Choose 1/2/3: ", {1, 2, 3})
    edu_2 = 1 if edu == 2 else 0
    edu_3 = 1 if edu == 3 else 0

    # Family size
    print("\nFamily size:")
    print("  1, 2, 3, or 4")
    fam = ask_int_in("Choose 1/2/3/4: ", {1, 2, 3, 4})
    fam_2 = 1 if fam == 2 else 0
    fam_3 = 1 if fam == 3 else 0
    fam_4 = 1 if fam == 4 else 0

    # CD Account (dummy column is "CD Account_1": 1 if has CD, else 0)
    cd = ask_yes_no("\nDo you have a Certificate of Deposit (CD) account? (Y/N): ")

    payload_features = {
        "Income": income,
        "Education_2": edu_2,
        "Education_3": edu_3,
        "Family_2": fam_2,
        "Family_3": fam_3,
        "Family_4": fam_4,
        "CD Account_1": cd,
    }
    return payload_features

# Wrap the features in the expected request format
payload = {"features": payload_features}

# Send the POST request
response = requests.post(url, json=payload)

# Handle the response
if response.status_code == 200:
    result = response.json()
    print("Prediction Probability:", result["probability"])
    print("Standard Decision:", result["decision_standard"])
    print("High Recall Decision:", result["decision_high_recall"])
    print("VIP Promo Decision:", result["decision_vip_promo"])
    print("Thresholds Used:", result["thresholds"])
else:
    print("Error:", response.status_code, response.text)


def tier_from_response(probability, thresholds, d_std, d_hr, d_vip):
    # Choose the highest tier satisfied
    if d_vip:
        return f"VIP Promo (p ≥ {thresholds.get('vip_promo', 0.8)})"
    if d_hr:
        return f"High Recall (p ≥ {thresholds.get('high_recall', 0.3)})"
    if d_std:
        return f"Standard (p ≥ {thresholds.get('standard', 0.5)})"
    return "No offer (below all thresholds)"
