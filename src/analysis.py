# Analysis Module
# Functions for analyzing hotel booking data

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List

def booking_summary(df: pd.DataFrame) -> dict:
    """
    Generate basic booking statistics.
    
    Args:
        df: Input DataFrame with booking data
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_bookings': len(df),
        'date_range': f"{df['arrival_date'].min()} to {df['arrival_date'].max()}" if 'arrival_date' in df.columns else 'N/A',
        'average_lead_time': df['lead_time'].mean() if 'lead_time' in df.columns else 'N/A',
        'total_guests': df['adults'].sum() + df['children'].sum() if 'adults' in df.columns else 'N/A',
    }
    return summary

def cancellation_analysis(df: pd.DataFrame) -> dict:
    """
    Analyze booking cancellations.
    
    Args:
        df: Input DataFrame with booking data
        
    Returns:
        Dictionary with cancellation metrics
    """
    if 'is_canceled' in df.columns:
        total = len(df)
        canceled = df['is_canceled'].sum()
        cancellation_rate = (canceled / total * 100) if total > 0 else 0
        
        analysis = {
            'total_bookings': total,
            'canceled_bookings': int(canceled),
            'completed_bookings': int(total - canceled),
            'cancellation_rate': f"{cancellation_rate:.2f}%"
        }
        return analysis
    else:
        return {'error': 'is_canceled column not found'}

def revenue_analysis(df: pd.DataFrame) -> dict:
    """
    Analyze revenue metrics.
    
    Args:
        df: Input DataFrame with booking data
        
    Returns:
        Dictionary with revenue insights
    """
    if 'adr' in df.columns and 'stays_in_weekend_nights' in df.columns:
        df_completed = df[df['is_canceled'] == 0] if 'is_canceled' in df.columns else df
        
        total_nights = df_completed['stays_in_weekend_nights'].sum() + df_completed['stays_in_week_nights'].sum() if 'stays_in_week_nights' in df.columns else df_completed['stays_in_weekend_nights'].sum()
        total_revenue = (df_completed['adr'] * total_nights).sum()
        
        analysis = {
            'total_revenue': f"${total_revenue:,.2f}" if total_revenue > 0 else 'N/A',
            'average_daily_rate': f"${df_completed['adr'].mean():,.2f}" if len(df_completed) > 0 else 'N/A',
            'total_nights_stayed': int(total_nights),
        }
        return analysis
    else:
        return {'error': 'Required columns (adr, stays_in_weekend_nights) not found'}

def customer_segmentation(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Segment customers based on specified column.
    
    Args:
        df: Input DataFrame
        column: Column name to segment by
        
    Returns:
        Series with value counts
    """
    if column in df.columns:
        return df[column].value_counts()
    else:
        return pd.Series({'error': f'{column} not found'})

def monthly_booking_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze booking trends by month.
    
    Args:
        df: Input DataFrame with arrival_date columns
        
    Returns:
        DataFrame with monthly trends
    """
    if 'arrival_date_month' in df.columns:
        trends = df.groupby('arrival_date_month').agg({
            'booking_id': 'count',
            'adr': 'mean' if 'adr' in df.columns else None,
            'is_canceled': 'mean' if 'is_canceled' in df.columns else None
        }).rename(columns={'booking_id': 'total_bookings', 'adr': 'avg_daily_rate', 'is_canceled': 'cancellation_rate'})
        return trends
    else:
        return pd.DataFrame({'error': 'arrival_date_month column not found'})

def analyze_bookings(df: pd.DataFrame) -> dict:
    """
    Complete analysis pipeline.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with all analyses
    """
    results = {
        'summary': booking_summary(df),
        'cancellations': cancellation_analysis(df),
        'revenue': revenue_analysis(df),
        'customer_segments': customer_segmentation(df, 'market_segment').to_dict() if 'market_segment' in df.columns else {},
    }
    return results

def get_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate actionable insights from data.
    
    Args:
        df: Input DataFrame
        
    Returns:
        List of insights
    """
    insights = []
    
    # Cancellation insight
    if 'is_canceled' in df.columns:
        cancel_rate = df['is_canceled'].mean() * 100
        insights.append(f"Cancellation rate is {cancel_rate:.1f}% - {'High' if cancel_rate > 30 else 'Moderate' if cancel_rate > 10 else 'Low'}")
    
    # Lead time insight
    if 'lead_time' in df.columns:
        avg_lead = df['lead_time'].mean()
        insights.append(f"Average lead time is {avg_lead:.0f} days")
    
    # Seasonal insight
    if 'arrival_date_month' in df.columns:
        peak_month = df['arrival_date_month'].mode()[0]
        insights.append(f"Peak booking month is {peak_month}")
    
    return insights