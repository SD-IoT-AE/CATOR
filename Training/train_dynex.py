import argparse
import joblib
from datasets.loaders import DatasetLoader
from src.dynex import DYNEX

def main():
    parser = argparse.ArgumentParser(description="Train DYNEX ensemble model")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name in datasets_config.json")
    parser.add_argument("--config", type=str, default="config/datasets_config.json", help="Dataset config file")
    parser.add_argument("--output", type=str, default="models/dynex.pkl", help="Output model path")
    args = parser.parse_args()

    print(f"[Training] Loading dataset: {args.dataset}")
    loader = DatasetLoader(args.config)
    X_train, X_test, y_train, y_test, kept_features = loader.load_dataset(args.dataset)

    print(f"[Training] Training DYNEX...")
    model = DYNEX(alpha=0.2, adaptation_threshold=0.5)
    model.fit(X_train, y_train)

    print(f"[Training] Saving model to {args.output}")
    joblib.dump({
        "model": model,
        "features": kept_features
    }, args.output)

    print("[Training] Done.")

if __name__ == "__main__":
    main()
