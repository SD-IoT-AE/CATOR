import json
import os
from .preprocessing import DatasetPreprocessor

class DatasetLoader:
    """
    Loads datasets as per the config file (datasets_config.json).
    """

    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)["datasets"]
        self.preprocessor = DatasetPreprocessor(self.config)

    def load_dataset(self, dataset_name):
        if dataset_name not in self.config:
            raise ValueError(f"Dataset {dataset_name} not found in config.")
        
        dataset_cfg = self.config[dataset_name]
        path = dataset_cfg["path"]

        # Load dataset
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset path {path} not found.")

        # Load all CSV files in the folder
        df_list = []
        for file in os.listdir(path):
            if file.endswith(".csv"):
                df_list.append(self.preprocessor.load_csv(os.path.join(path, file)))
        df = pd.concat(df_list, ignore_index=True)

        # Clean data
        df = self.preprocessor.clean_data(df)

        # Identify features (everything except "Label")
        feature_cols = [col for col in df.columns if col != "Label"]

        # Normalize features
        df, _ = self.preprocessor.normalize(df, feature_cols)

        # Feature selection
        df_reduced, kept_features = self.preprocessor.feature_selection(df, feature_cols)

        # Add back the label
        df_reduced["Label"] = df["Label"]

        # Train/test split
        X_train, X_test, y_train, y_test = self.preprocessor.split(df_reduced, "Label", train_size=dataset_cfg.get("train_split", 0.8))

        return X_train, X_test, y_train, y_test, kept_features
