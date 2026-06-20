# Visualization Module
# Functions for creating plots and charts

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Tuple

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def plot_cancellation_distribution(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plot cancellation distribution.
    
    Args:
        df: Input DataFrame
        save_path: Optional path to save figure
    """
    if 'is_canceled' not in df.columns:
        print("Error: 'is_canceled' column not found")
        return
    
    fig, ax = plt.subplots(figsize=(8, 5))
    cancellation_counts = df['is_canceled'].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    
    cancellation_counts.plot(kind='bar', ax=ax, color=colors)
    ax.set_title('Booking Cancellations', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Bookings', fontsize=12)
    ax.set_xlabel('Status', fontsize=12)
    ax.set_xticklabels(['Completed', 'Canceled'], rotation=0)
    
    # Add value labels on bars
    for i, v in enumerate(cancellation_counts):
        ax.text(i, v + 50, str(v), ha='center', fontweight='bold')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_monthly_trends(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plot monthly booking trends.
    
    Args:
        df: Input DataFrame with arrival_date_month column
        save_path: Optional path to save figure
    """
    if 'arrival_date_month' not in df.columns:
        print("Error: 'arrival_date_month' column not found")
        return
    
    monthly_data = df.groupby('arrival_date_month').size()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_data.plot(kind='line', ax=ax, marker='o', linewidth=2, color='#3498db')
    ax.set_title('Monthly Booking Trends', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Bookings', fontsize=12)
    ax.set_xlabel('Month', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_adr_distribution(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plot Average Daily Rate distribution.
    
    Args:
        df: Input DataFrame with adr column
        save_path: Optional path to save figure
    """
    if 'adr' not in df.columns:
        print("Error: 'adr' column not found")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    df['adr'].hist(bins=50, ax=ax, color='#9b59b6', edgecolor='black')
    ax.set_title('Average Daily Rate Distribution', fontsize=14, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_xlabel('ADR ($)', fontsize=12)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_customer_type_distribution(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plot customer type distribution.
    
    Args:
        df: Input DataFrame with customer_type column
        save_path: Optional path to save figure
    """
    if 'customer_type' not in df.columns:
        print("Error: 'customer_type' column not found")
        return
    
    fig, ax = plt.subplots(figsize=(8, 6))
    customer_counts = df['customer_type'].value_counts()
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    customer_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors[:len(customer_counts)])
    ax.set_title('Customer Type Distribution', fontsize=14, fontweight='bold')
    ax.set_ylabel('')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_lead_time_analysis(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plot lead time distribution.
    
    Args:
        df: Input DataFrame with lead_time column
        save_path: Optional path to save figure
    """
    if 'lead_time' not in df.columns:
        print("Error: 'lead_time' column not found")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    df['lead_time'].hist(bins=50, ax=ax, color='#1abc9c', edgecolor='black')
    ax.set_title('Lead Time Distribution', fontsize=14, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_xlabel('Lead Time (days)', fontsize=12)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_dashboard(df: pd.DataFrame, save_dir: str = None) -> None:
    """
    Create a dashboard with multiple visualizations.
    
    Args:
        df: Input DataFrame
        save_dir: Optional directory to save figures
    """
    print("Creating summary dashboard...")
    
    if 'is_canceled' in df.columns:
        plot_cancellation_distribution(df, f"{save_dir}/01_cancellations.png" if save_dir else None)
    
    if 'arrival_date_month' in df.columns:
        plot_monthly_trends(df, f"{save_dir}/02_monthly_trends.png" if save_dir else None)
    
    if 'adr' in df.columns:
        plot_adr_distribution(df, f"{save_dir}/03_adr_distribution.png" if save_dir else None)
    
    if 'customer_type' in df.columns:
        plot_customer_type_distribution(df, f"{save_dir}/04_customer_types.png" if save_dir else None)
    
    if 'lead_time' in df.columns:
        plot_lead_time_analysis(df, f"{save_dir}/05_lead_time.png" if save_dir else None)
    
    print("✓ Dashboard creation complete!")