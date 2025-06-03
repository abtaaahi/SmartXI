import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

d=pd.read_csv("data.csv")

d.drop_duplicates(inplace=True)
d.dropna(inplace=True)

l={}
for col in ["Club","Position","Formation","Style"]:
    if col in d.columns:
        le=LabelEncoder()
        d[col]=le.fit_transform(d[col])
        l[col]=le

x=d.drop(columns=["Name","Nationality","Position","Club"])
y=(
    d["Overall Rating"]*100000 +
    d["Pace"]*500 +
    d["Shooting"]*750 +
    d["Passing"]*400 +
    d["Dribbling"]*450 +
    d["Physical"]*300
)

xtr, xt, y_train, yt = train_test_split(x, y, test_size=0.2, random_state=42)

m = RandomForestRegressor()
m.fit(xtr, y_train)

y = m.predict(xt)
r2 = r2_score(yt, y)
mae = mean_absolute_error(yt, y)
rmse = np.sqrt(mean_squared_error(yt, y))

print(f"{r2:.4f}")
print(f"{mae:.2f}")
print(f"{rmse:.2f}")

with open("market.pkl", "wb") as f:
    pickle.dump((m, list(x.columns)), f)

with open("label.pkl", "wb") as f:
    pickle.dump(l, f)