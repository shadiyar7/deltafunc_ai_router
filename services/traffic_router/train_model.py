import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print("Training Smart TDS Predictive ML Model...")

# 1. Mock Data: 1000 clicks
# Columns: user_geo, device, time_of_day, offer_id, converted (0/1)
data = {
    'user_geo': ['US', 'DE', 'BR', 'CA', 'GB'] * 200,
    'device': ['Mobile', 'Desktop', 'Tablet'] * 333 + ['Mobile'],
    'time_of_day': ['Morning', 'Afternoon', 'Evening', 'Night'] * 250,
    'offer_id': ['ecom_nike', 'finance_cc', 'igaming_01', 'crypto_02', 'dating_app'] * 200,
    'converted': [0, 1, 0, 1, 0, 1, 0, 0, 1, 0] * 100
}

df = pd.DataFrame(data)

# 2. Preprocessing
le_geo = LabelEncoder()
le_device = LabelEncoder()
le_time = LabelEncoder()
le_offer = LabelEncoder()

df['user_geo_enc'] = le_geo.fit_transform(df['user_geo'])
df['device_enc'] = le_device.fit_transform(df['device'])
df['time_enc'] = le_time.fit_transform(df['time_of_day'])
df['offer_enc'] = le_offer.fit_transform(df['offer_id'])

X = df[['user_geo_enc', 'device_enc', 'time_enc', 'offer_enc']]
y = df['converted']

# 3. Train Model
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X, y)

# 4. Save Artifacts
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/tds_model.pkl')
joblib.dump(le_geo, 'models/le_geo.pkl')
joblib.dump(le_device, 'models/le_device.pkl')
joblib.dump(le_time, 'models/le_time.pkl')
joblib.dump(le_offer, 'models/le_offer.pkl')

print("Model trained and saved to models/tds_model.pkl!")
