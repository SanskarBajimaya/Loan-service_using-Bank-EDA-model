import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from schemas import PredictRequest, PredictResponse

#Loading the artifacts 
Model_path = "model/loan_xgb.joblib"
Meta_path = "model/model_meta.json"

app = FastAPI(title="Loan Acceptance Scoring Service", version="1.0.0")

try:
    model = joblib.load(Model_path)
    with open(Meta_path,"r") as f:
        meta = json.load(f)
    thresholds = meta.get("thresholds", {"standard": 0.5, "high_recall": 0.3, "vip_promo": 0.8})
    train_features = meta.get("features")
except Exception as e:
    raise RuntimeError(f"Failed to load artifacts: {e}")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Build 1-row DataFrame in the exact training column order
    feats = req.features
    if train_features:
        missing = [c for c in train_features if c not in feats]
        if missing:
            raise HTTPException(400, f"Missing features: {missing[:10]} (and possibly more)")
    else:
        X = pd.DataFrame([feats])

    #Predit Probability
    try:
        proba = float(model.predict_proba(X)[0,1])
    except Exception as e:
        raise HTTPException(400, f"Prediction Failed: {e}")
    
    # Applying thresholds from meta
    p = proba
    t = thresholds
    return PredictResponse(
        probability=proba,
        decision_standard=int(p >= t["standard"]),
        decision_high_recall=int(p >= t["high_recall"]),
        decision_vip_promo=int(p >= t["vip_promo"]),
        thresholds=t,
        meta={"model_type": meta.get("model_type"), "created_at": meta.get("created_at")}
    )


