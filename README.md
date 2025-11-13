# 🏦 Bank Personal Loan Campaign Analysis

**End-to-End ML Model Deployment with FastAPI, Docker & SendGrid Email Automation**

## 📘 Overview

This project predicts whether a bank customer is likely to accept a personal loan offer and automates personalized email campaigns based on the prediction tier. It covers the complete lifecycle of a data product — from EDA and model training to API deployment and email-based client engagement.

## 📊 Business Overview (Non-Technical)

This system helps a bank send the right loan offer to the right customer instead of using generic mass marketing.

### ⭐ Smarter Targeting

The model predicts how likely a customer is to accept a personal loan. Based on that score, the system places the customer into one of three groups:

* **VIP Promo** – very likely to accept
* **Standard Offer** – moderately likely
* **Basic/High-Recall** – low likelihood

This allows the bank to focus promotions where they will work best.

### ⭐ Automated Personalized Emails

For each tier, the system automatically sends a personalized email with the appropriate tone, benefits, and loan offer. This reduces manual work for marketing teams and improves customer engagement.

### ⭐ Better Customer Experience

Customers receive relevant, customized loan offers, rather than spam. This increases trust and leads to higher satisfaction.

### ⭐ Business Impact

* Higher loan acceptance rates
* Lower marketing costs
* Faster and consistent communication
* Scalable outreach to thousands of customers

## 🧠 Features

- **Machine Learning Pipeline**: Preprocessing → Feature Engineering → Model Training (XGBoost best performer)
- **FastAPI Server**: Exposes `/predict` endpoint for scoring new clients
- **Client Application**: CLI tool to collect user info and send POST requests
- **Automated Email System**: Tier-based email templates (VIP, Standard, High-Recall) using SendGrid API
- **Safe Credentials**: Managed through `.env` variables (no keys in source code)

## 📂 Project Structure

```
Loan-service_using-Bank-EDA-model/
│
├── app/
│   ├── main.py                # FastAPI backend (prediction API)
│   ├── client.py              # Client app for interacting with API
│   ├── send_email.py          # SendGrid integration (tier-based templates)
│   ├── schemas.py             # Request/response data models (Pydantic)
│   └── model/                 # Saved ML model + metadata
│       ├── loan_xgb.joblib
│       └── model_meta.json
│
├── email_templates/
│   ├── vip_promo.html
│   ├── standard.html
│   └── high_recall.html
│
├── requirements.txt
├── .env                       # Local environment file (keys, email)
├── Dockerfile
└── README.md
```

## ⚙️ Environment Configuration (.env)

Create a `.env` file in the project root (same level as `app/` and `email_templates/`):

```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=sanskarbajimaya12@gmail.com
DRY_RUN=0   # set to 1 for dry-run (no actual email send)
```

⚠️ **Never commit `.env` to GitHub. Add it to `.gitignore`.**

If you prefer PowerShell permanent variables:

```powershell
setx SENDGRID_API_KEY "SG.xxxxx"
setx SENDGRID_FROM_EMAIL "your_verified_sender@gmail.com"
```

## 🚀 Running the Project

### 1️⃣ Start the FastAPI Server

In your terminal:

```bash
cd app
uvicorn main:app --reload
```

Server starts at: ➡️ `http://127.0.0.1:8000`

You can test health:

```
GET http://127.0.0.1:8000/health
```

Response:

```json
{"status": "ok"}
```

### 2️⃣ Run the Client Application

In a new terminal:

```bash
cd app
python client.py
```

The client will:
1. Ask for inputs (income, education, family size, etc.)
2. Send data to `/predict`
3. Display the probability and eligible loan tier
4. Ask if you want to send an email to the client
5. If Y, it uses `send_email.py` to send the proper HTML template via SendGrid.

## 🧪 Sample Input / Output

### Input Prompt (Client)

```
=== Loan Acceptance Screening ===
Annual income (e.g., 110 for $110k): 120
Education level: 1=Undergrad, 2=Graduate, 3=Advanced → 2
Family size: 1/2/3/4 → 3
Do you have a CD Account? (Y/N): Y
```

### Response (from API)

```
Prediction Probability: 0.8123
Standard Decision: True
High Recall Decision: True
VIP Promo Decision: True
Thresholds Used: {"standard":0.5,"high_recall":0.3,"vip_promo":0.8}
✅ VIP Promo Tier selected.
```

### Email Sent (SendGrid)

- **Subject**: 🎉 VIP Promotional Loan Offer
- **Body**: Custom HTML from `/email_templates/vip_promo.html`

## 📧 SendGrid Demo Setup (Quick Guide)

1. Go to [SendGrid Dashboard](https://app.sendgrid.com/).
2. Navigate to **Settings → Sender Authentication**.
3. Choose **Single Sender Verification**.
4. Add your Gmail (e.g., `sanskarbajimaya12@gmail.com`).
5. Verify via email link.
6. Create an **API Key** with **Mail Send** scope.
7. Store it in `.env` → `SENDGRID_API_KEY`.

💡 **To confirm it works:**

```python
from sendgrid import SendGridAPIClient, Mail
import os

sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
msg = Mail(
    from_email=os.getenv("SENDGRID_FROM_EMAIL"),
    to_emails=os.getenv("SENDGRID_FROM_EMAIL"),
    subject="Test Email",
    html_content="<strong>It works!</strong>"
)
print(sg.send(msg).status_code)  # should print 202
```

## 🧩 Testing Scenarios

| Scenario | Expected Outcome |
|----------|------------------|
| Probability ≥ 0.8 | VIP email sent |
| 0.5 ≤ Prob < 0.8 | Standard email sent |
| 0.3 ≤ Prob < 0.5 | High-Recall email sent |
| Prob < 0.3 | No email sent |
| Invalid .env / key | Raises RuntimeError |
| Email declined by user | No email sent (graceful exit) |

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi`, `uvicorn` | REST API backend |
| `pandas`, `scikit-learn`, `xgboost` | Model training & prediction |
| `sendgrid` | Email delivery |
| `python-dotenv` | Environment variable loading |
| `joblib` | Model persistence |

**Install:**

```bash
pip install -r requirements.txt
```


## 💡 System Architecture

```
        ┌──────────────────────────┐
        │   FastAPI Model Server   │
        │  (predict loan chance)   │
        └──────────┬───────────────┘
                   │ JSON
                   ▼
        ┌──────────────────────────┐
        │      client.py CLI       │
        │ Collects user features   │
        │ Displays probability     │
        │ Sends tier email (VIP/..)│
        └──────────┬───────────────┘
                   │ SMTP/API
                   ▼
        ┌──────────────────────────┐
        │      SendGrid API        │
        │  Sends promotional email │
        └──────────────────────────┘
```

## 🧑‍💻 Author

**Sanskar Bajimaya**  
Bachelor of Science in IT & Business Administration  
Fairleigh Dickinson University – Vancouver

📧 [sanskarbajimaya12@gmail.com](mailto:sanskarbajimaya12@gmail.com)  
🔗 [GitHub](https://github.com/SanskarBajimaya)  
🔗 [Portfolio](https://sanskar-bajimaya.online/) 
🔗 [LinkedIn](https://www.linkedin.com/in/sanskar-bajimaya)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/SanskarBajimaya/Loan-service_using-Bank-EDA-model/issues).

## ⭐ Show your support

Give a ⭐️ if this project helped you!

