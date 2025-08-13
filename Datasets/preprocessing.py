import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split

class DatasetPreprocessor:
    """
    Handles dataset cleaning, normalization, and feature selection
    for IoT DDoS detection.
    """

    def __init__(self, config):
        self.config = config

    def load_csv(self, path):
        print(f"[Preprocessing] Loading dataset from {path}...")
        df = pd.read_csv(path)
        return df

    def clean_data(self, df):
        print("[Preprocessing] Cleaning dataset...")
        df = df.dropna()
        df = df.drop_duplicates()
        return df

    def normalize(self, df, feature_cols):
        print("[Preprocessing] Normalizing features...")
        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])
        return df, scaler

    def feature_selection(self, df, feature_cols, threshold=0.01):
        print(f"[Preprocessing] Removing features with variance < {threshold}...")
        selector = VarianceThreshold(threshold=threshold)
        reduced_features = selector.fit_transform(df[feature_cols])
        kept_features = [feature_cols[i] for i in range(len(feature_cols)) if selector.variances_[i] >= threshold]
        df_reduced = pd.DataFrame(reduced_features, columns=kept_features)
        return df_reduced, kept_features

    def split(self, df, target_col, train_size=0.8):
        print(f"[Preprocessing] Splitting dataset into {train_size*100:.0f}% train / {100-train_size*100:.0f}% test...")
        X = df.drop(columns=[target_col])
        y = df[target_col]
        return train_test_split(X, y, train_size=train_size, random_state=42, stratify=y)
