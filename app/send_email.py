import sendgrid
import os
import re
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from pathlib import Path

# Fuction input yes or no
def ask_yes_no(prompt):
    while True:
            val = input(prompt).strip().lower()
            if val in ["y","yes"]:
                return 1
            if val in ["n","no"]:
                return 0
            print("Please answer Y/N.")
# Maps the templates
TEMPLATE_MAP = {
    "vip_promo": "vip_promo.html",
    "standard": "standard.html",
    "high_recall": "high_recall.html",  
}

# Navigate towards the correct template
def read_template_html(tier: str) -> str:
    fname = TEMPLATE_MAP.get(tier)
    if not fname:
        raise ValueError(f"Unknown tier '{tier}'. Expected one of {list(TEMPLATE_MAP)}")

    # Path of the current file (send_email.py)
    base = Path(__file__).resolve().parent

    # Templates folder is one level above /app
    template_path = base.parent / "email_templates" / fname

    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    return template_path.read_text(encoding="utf-8")


# Getting API key from OS environment
def _get_sg_client() -> SendGridAPIClient:
    api_key = os.getenv("SENDGRID_API_KEY", "").strip()
    if not api_key or not api_key.startswith("SG."):
        raise RuntimeError(
            "SENDGRID_API_KEY is missing/invalid. "
            "Create a restricted key with Mail Send scope and set it via environment variable."
        )
    return SendGridAPIClient(api_key)


def sendEmail(tier):
    email_consent = ask_yes_no("\nDo you want to send an email to this client? (Y/N): ")

    # Optional
    print("API Key loaded?", bool(os.getenv("SENDGRID_API_KEY")))
    print("From email:", os.getenv("SENDGRID_FROM_EMAIL"))


    if email_consent:
        try:
            name = input("Enter Your full name: ")
        except ValueError:
            print("Please enter a valid name")
            return  # Exit if name input fails

        valid = False
        while not valid:
            email = input("Enter Your email: ")
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None
            if not valid:
                print("Invalid email format. Please try again.")


        # Read HTML content from file
        try:
            html_content = read_template_html(tier)
        except Exception as e:
            print(f"Couldn't load template for tier '{tier}': {e}")
            return {"attempted": False, "error": str(e)}  

        # Construct and send the email
        from_email = os.getenv("SENDGRID_FROM_EMAIL", "").strip()
        # IMPORTANT: from_email MUST be a verified Single Sender or belong to an authenticated domain.
    #     # After creating a fresh API key with Mail Send scope
            # setx SENDGRID_API_KEY "SG.xxxxx.yyyyy"
            # setx SENDGRID_FROM_EMAIL "your_verified_sender@example.com"

        message = Mail(
            from_email=from_email,
            to_emails= email,
            subject='Loan Offer!!',
            plain_text_content='Please view this email in HTML.',
            html_content=html_content
        )

        try:
            sg = _get_sg_client()
            resp = sg.send(message)
            status = getattr(resp, "status_code", None)
            body = getattr(resp, "body", b"")
            body_text = body.decode() if hasattr(body, "decode") else str(body)
            print(f"SendGrid status: {status}")
            if body_text and status and status >= 400:
                print("SendGrid body:", body_text)
            headers = getattr(resp, "headers", None)
            if headers:
                print("SendGrid headers:", headers)
            return {"attempted": True, "status_code": status}
        except Exception as e:
            # This will also catch auth / 403 errors and show message
            print("Email send failed:", repr(e))
            return {"attempted": True, "error": repr(e)}

