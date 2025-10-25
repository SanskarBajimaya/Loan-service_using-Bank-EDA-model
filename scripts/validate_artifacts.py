import json, joblib, pandas as pd
from sklearn.metrics import recall_score, precision_score, accuracy_score

model_add = "model/loan_xgb.joblib"
meta_add = "model/model_meta.json"
Xcsv = "model/X_test_preprocessed.csv"
Ycsv = "model/y_test.csv"

model = joblib.load(model_add)
meta = json.load(open(meta_add))
X = pd.read_csv(Xcsv)
y = pd.read_csv(Ycsv).squeeze() # Label as series

proba = model.predict_proba(X)[:,1] # Predicts the probability of the positive class
def binarize(p, t): return (p >= t).astype(int)

for name, t in meta["thresholds"].items():
    yhat = binarize(proba, t)
    print(f"[{name}] threshold = {t} | "
          f"Recall = {recall_score(y, yhat):.3f} | "
          f"Precision = {precision_score(y, yhat):.3f} | "
          f"Accuracy = {accuracy_score(y, yhat):.3f}")
    

