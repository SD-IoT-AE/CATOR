import argparse
import joblib
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, classification_report
import time
from datasets.loaders import DatasetLoader

def main():
    parser = argparse.ArgumentParser(description="Evaluate DYNEX ensemble model")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name in datasets_config.json")
    parser.add_argument("--config", type=str, default="config/datasets_config.json", help="Dataset config file")
    parser.add_argument("--model", type=str, default="models/dynex.pkl", help="Path to trained model")
    args = parser.parse_args()

    print(f"[Evaluation] Loading dataset: {args.dataset}")
    loader = DatasetLoader(args.config)
    X_train, X_test, y_train, y_test, kept_features = loader.load_dataset(args.dataset)

    print(f"[Evaluation] Loading trained model from {args.model}")
    saved = joblib.load(args.model)
    model = saved["model"]

    print(f"[Evaluation] Predicting on test set...")
    start_time = time.time()
    y_pred = [model.predict(x.reshape(1, -1)) for x in X_test.to_numpy()]
    elapsed_time = time.time() - start_time

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    atrt = elapsed_time / len(y_test)

    print("\n===== Evaluation Results =====")
    print(f"Detection Accuracy (DA): {acc:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Matthews Correlation Coefficient (MCC): {mcc:.4f}")
    print(f"Average Time to Respond per Traffic (ATRT): {atrt:.6f} sec")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()
