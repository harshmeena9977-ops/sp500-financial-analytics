import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_prediction_model(filepath):
    print("Loading processed data for modeling...")
    df = pd.read_csv(filepath)
    
    # Drop rows with NaN values resulting from rolling windows or shifts
    df = df.dropna().reset_index(drop=True)
    
    # Select features and target
    features = ['open', 'high', 'low', 'close', 'volume', 'daily_return', 'sma_20', 'sma_50', 'volatility_20']
    X = df[features]
    y = df['target']
    
    # Train-test split (chronological/random split for baseline demo)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    train_prediction_model("sp500_processed.csv")