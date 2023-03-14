


from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import pandas as pd
from func_connections import connect_dydx
from func_public import get_candles_historical
from constants import RESOLUTION

# Connect to client
try:
    print("Connecting to Client...")
    client = connect_dydx()
except Exception as e:
    print("Error connecting to client: ", e)
    exit(1)

symbol = "BTC-USD"
candels = client.public.get_candles(
    market= symbol,
    resolution=RESOLUTION,
    limit=100
  )
#print(candels.data["candles"])

df = pd.DataFrame(candels.data["candles"])

df["startedAt"] = pd.to_datetime(df["startedAt"])
df["close"] = pd.to_numeric(df["close"])
df["baseTokenVolume"] = pd.to_numeric(df["baseTokenVolume"])
df.set_index("startedAt", inplace=True)
df["close"] = pd.to_numeric(df["close"])
df["Diff"] = df["close"].diff()
df["SMA_2"] = df["close"].rolling(2).mean()
df["Force_Index"] = df["close"] * df["baseTokenVolume"]
df["y"] = df["Diff"].apply(lambda x: 1 if x > 0 else 0).shift(-1)

df = df.drop(
    ["updatedAt", "market", "resolution", "low", "high", "open", "close", "baseTokenVolume", "trades", "usdVolume", "startingOpenInterest"],
    axis=1,
).dropna()
#print(df.head())
X = df.drop(["y"], axis=1).values
y = df["y"].values
print(df["y"].dtype)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False,
)
clf = xgb.XGBClassifier()
clf.fit(
    X_train,
    y_train,
)
#y_pred = clf.predict(X_test)
#print(accuracy_score(y_test, y_pred))

y_proba = clf.predict_proba(X_test)
y_pred_proba = clf.predict_proba(X_test)[:,1]
y_pred = (y_pred_proba > 0.5).astype(int)
print(y_pred)
print("accuracy_score")
print(accuracy_score(y_test, y_pred))


