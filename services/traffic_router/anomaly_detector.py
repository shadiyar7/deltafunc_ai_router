import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_traffic_anomalies():
    print("Running Traffic Anomaly Detection (Isolation Forest)...")
    # Mock data representing affiliates traffic: clicks, conversions
    data = {
        'affiliate_id': [101, 102, 103, 104, 105],
        'clicks': [5000, 4500, 10000, 4800, 5100],
        'conversions': [100, 90, 0, 95, 110]
    }
    df = pd.DataFrame(data)
    df['conversion_rate'] = df['conversions'] / df['clicks']
    
    # Train Isolation Forest
    model = IsolationForest(contamination=0.2, random_state=42)
    df['anomaly'] = model.fit_predict(df[['clicks', 'conversion_rate']])
    
    anomalies = df[df['anomaly'] == -1]
    
    for idx, row in anomalies.iterrows():
        print(f"[ALERT] Affiliate {int(row['affiliate_id'])} flagged for FRAUD! Clicks: {int(row['clicks'])}, ConvRate: {row['conversion_rate']:.2%}")

if __name__ == '__main__':
    detect_traffic_anomalies()
