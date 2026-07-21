import os
import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from langchain.tools import tool

@tool
def analyze_csv(filepath: str) -> str:
    """Perform Exploratory Data Analysis (EDA) directly on a CSV file path."""
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return f"Error reading file: {e}"

    report = f"""
==============================
DATASET OVERVIEW
==============================

First 5 Rows:
{df.head().to_string()}

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Column Names:
{list(df.columns)}

Data Types:
{df.dtypes.to_string()}

Missing Values:
{df.isnull().sum().to_string()}

Duplicate Rows:
{df.duplicated().sum()}

Summary Statistics:
{df.describe(include="all").to_string()}
"""
    return report


@tool
def generate_visualizations(filepath: str) -> str:
    """Generate multiple visualizations and save them in the plots folder."""
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return f"Error reading file: {e}"

    os.makedirs("plots", exist_ok=True)

    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include="object").columns

    # 1. Histograms
    for col in numeric_cols:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[col], kde=True)
        plt.title(f"Histogram - {col}")
        plt.savefig(f"plots/histogram_{col}.png")
        plt.close()

    # 2. Box Plots
    for col in numeric_cols:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[col])
        plt.title(f"Box Plot - {col}")
        plt.savefig(f"plots/boxplot_{col}.png")
        plt.close()

    # 3. Bar Plots
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            plt.figure(figsize=(8, 4))
            df[col].value_counts().plot(kind="bar")
            plt.title(f"Bar Plot - {col}")
            plt.savefig(f"plots/bar_{col}.png")
            plt.close()

    # 4. Correlation Heatmap
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig("plots/correlation_heatmap.png")
        plt.close()

    return "Successfully generated visualizations and saved them in the plots folder."


@tool
def correlation_analysis(filepath: str) -> str:
    """Perform correlation analysis on a CSV file and generate a heatmap."""
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return f"Error reading file: {e}"

    os.makedirs("plots", exist_ok=True)

    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 2:
        return "Not enough numeric columns for correlation analysis."

    corr = numeric_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("plots/correlation_heatmap.png")
    plt.close()

    return f"Correlation Heatmap saved successfully.\n\n{corr.to_string()}"


@tool
def save_report(content: str, filename: str = "dataset_report") -> str:
    """Save report into reports folder."""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"reports/{filename}_{timestamp}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Report saved successfully: {filepath}"