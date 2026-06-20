# Data Processing Module
# Functions for data cleaning and transformation

import pandas as pd
import numpy as np
from typing import Tuple, List

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load booking data from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with booking data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None

def check_data_quality(df: pd.DataFrame) -> dict:
    """
    Check data quality metrics.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with quality metrics
    """
    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    return quality_report

def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: Input DataFrame
        strategy: 'drop' to remove rows, 'fill_numeric' to fill numeric with mean, 'fill_category' for mode
        
    Returns:
        DataFrame with handled missing values
    """
    df_clean = df.copy()
    
    if strategy == 'drop':
        df_clean = df_clean.dropna()
    elif strategy == 'fill_numeric':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == 'fill_category':
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown')
    
    return df_clean

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from dataset.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with duplicates removed
    """
    initial_rows = len(df)
    df_clean = df.drop_duplicates()
    removed = initial_rows - len(df_clean)
    print(f"Removed {removed} duplicate rows.")
    return df_clean

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names and data types.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with standardized columns
    """
    # Convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

def create_date_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Create additional features from date column.
    
    Args:
        df: Input DataFrame
        date_column: Name of the date column
        
    Returns:
        DataFrame with new date features
    """
    df[date_column] = pd.to_datetime(df[date_column])
    df[f'{date_column}_year'] = df[date_column].dt.year
    df[f'{date_column}_month'] = df[date_column].dt.month
    df[f'{date_column}_quarter'] = df[date_column].dt.quarter
    df[f'{date_column}_dayofweek'] = df[date_column].dt.dayofweek
    df[f'{date_column}_week'] = df[date_column].dt.isocalendar().week
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete data cleaning pipeline.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    print("Starting data cleaning pipeline...")
    
    # Standardize columns
    df = standardize_columns(df)
    print("✓ Columns standardized")
    
    # Remove duplicates
    df = remove_duplicates(df)
    print("✓ Duplicates removed")
    
    # Handle missing values
    df = handle_missing_values(df, strategy='drop')
    print("✓ Missing values handled")
    
    print(f"Final dataset shape: {df.shape}")
    return df

def export_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Export processed data to CSV.
    
    Args:
        df: DataFrame to export
        output_path: Path for output file
    """
    df.to_csv(output_path, index=False)
    print(f"Data exported to {output_path}")