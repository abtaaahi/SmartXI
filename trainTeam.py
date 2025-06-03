import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle

d = pd.read_csv("data.csv")
d.fillna(0, inplace=True)

features=['Overall Rating', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical', 'Age']
market_column='Market Value'

estimated_value = (
    d['Overall Rating'] * 0.4 +
    d['Shooting'] * 0.2 +
    d['Dribbling'] * 0.15 +
    d['Passing'] * 0.1 +
    d['Pace'] * 0.05 +
    d['Defending'] * 0.05 +
    d['Physical'] * 0.03 - 
    d['Age'] * 0.02
) * 1.5

d[market_column] = np.round(estimated_value, 2)
d.to_csv("data2.csv", index=False)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(d[features])

X_train, X_test, y_train, y_test = train_test_split(X_scaled, estimated_value, test_size=0.2, random_state=42)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"R² Score       : {r2:.4f} / 1")
print(f"MAE            : {mae:.2f} / {y_test.max():.2f}")
print(f"RMSE           : {rmse:.2f} / {y_test.max():.2f}")

cv_scores = cross_val_score(model, X_scaled, estimated_value, cv=5, scoring='neg_mean_squared_error')

pickle.dump(model, open("value_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))


def team(budget, formation, style):
    d = pd.read_csv("data2.csv")

    fm = {
        "4-3-3": {"DEF": 4, "MID": 3, "FWD": 3},
        "4-4-2": {"DEF": 4, "MID": 4, "FWD": 2},
        "3-4-3": {"DEF": 3, "MID": 4, "FWD": 3}
    }

    sw = {
        "Attacking": {"Shooting": 0.4, "Dribbling": 0.3, "Passing": 0.2},
        "Balanced": {"Shooting": 0.3, "Dribbling": 0.2, "Passing": 0.3, "Defending": 0.1, "Physical": 0.1},
        "Defensive": {"Defending": 0.4, "Physical": 0.3, "Passing": 0.2}
    }

    def map_position(pos):
        pos=pos.lower()
        if "goalkeeper" in pos:
            return "GK"
        if "defender" in pos:
            return "DEF"
        if "midfielder" in pos:
            return "MID"
        return "FWD"

    d['Role'] = d['Position'].apply(map_position)

    d['Score']=sum(d[attr] * weight for attr, weight in sw[style].items())
    d=d.sort_values(by='Score', ascending=False)

    s=[]

    gk_pool = d[d['Role'] == 'GK'].sort_values(by='Market Value')
    for _, p in gk_pool.iterrows():
        if p['Market Value'] <= budget:
            s.append(p.to_dict())
            budget -= p['Market Value']
            break

    for e, count in fm[formation].items():
        a = d[(d['Role']==e)&(~d['Name'].isin([p['Name'] for p in s]))]
        for _, p in a.iterrows():
            if len([p for p in s if p['Role']==e])<count and p['Market Value']<=budget:
                s.append(p.to_dict())
                budget-=p['Market Value']

    team=pd.DataFrame(s)

    for column in ['Role', 'Score']:
        if column in team.columns:
            team=team.drop(columns=[column])

    return team