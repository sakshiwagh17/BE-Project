import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from xgboost import XGBRegressor

X = np.load("features/X.npy")
y = np.load("features/y.npy")

print("X shape:", X.shape)
print("y shape:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# scale properly
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# save scaler
with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

model = MultiOutputRegressor(
    XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        random_state=42
    )
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("R2 score:", r2_score(y_test, pred))

with open("models/personality_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model + scaler saved")