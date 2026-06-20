"""
Hotel Booking Data Analysis Report
Comprehensive analysis of hotel_bookings.csv dataset
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("=" * 80)
print("HOTEL BOOKING ANALYSIS - COMPREHENSIVE REPORT")
print("=" * 80)

df = pd.read_csv('hotel_bookings.csv')

# 1. DATASET OVERVIEW
print("\n1. DATASET OVERVIEW")
print("-" * 80)
print(f"Total Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"Dataset Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"\nColumns: {', '.join(df.columns.tolist())}")

# 2. DATA QUALITY CHECK
print("\n2. DATA QUALITY CHECK")
print("-" * 80)
print(f"Duplicate Rows: {df.duplicated().sum():,}")
print(f"\nMissing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
for col in df.columns:
    if missing[col] > 0:
        print(f"  {col}: {missing[col]:,} ({missing_pct[col]:.2f}%)")
if missing.sum() == 0:
    print("  No missing values found!")

# 3. BOOKING SUMMARY
print("\n3. BOOKING SUMMARY STATISTICS")
print("-" * 80)
print(f"Total Bookings: {len(df):,}")

if 'is_canceled' in df.columns:
    canceled = df['is_canceled'].sum()
    completed = len(df) - canceled
    cancel_rate = (canceled / len(df)) * 100
    print(f"Completed Bookings: {completed:,} ({100-cancel_rate:.1f}%)")
    print(f"Canceled Bookings: {int(canceled):,} ({cancel_rate:.1f}%)")

# 4. HOTEL TYPE ANALYSIS
print("\n4. HOTEL TYPE DISTRIBUTION")
print("-" * 80)
if 'hotel' in df.columns:
    hotel_dist = df['hotel'].value_counts()
    for hotel, count in hotel_dist.items():
        pct = (count / len(df)) * 100
        print(f"  {hotel}: {count:,} ({pct:.1f}%)")

# 5. GUEST ANALYSIS
print("\n5. GUEST & LENGTH OF STAY ANALYSIS")
print("-" * 80)
if 'adults' in df.columns:
    print(f"Average Guests per Booking: {df['adults'].mean():.1f}")
    print(f"Guests Range: {df['adults'].min():.0f} - {df['adults'].max():.0f}")

if 'stays_in_weekend_nights' in df.columns and 'stays_in_week_nights' in df.columns:
    total_nights = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    print(f"Average Total Stay: {total_nights.mean():.1f} nights")
    print(f"Most Common Stay: {total_nights.mode()[0] if len(total_nights.mode()) > 0 else 'N/A'} nights")

# 6. PRICING ANALYSIS
print("\n6. PRICING & REVENUE ANALYSIS")
print("-" * 80)
if 'adr' in df.columns:
    print(f"Average Daily Rate (ADR):")
    print(f"  Mean: ${df['adr'].mean():.2f}")
    print(f"  Median: ${df['adr'].median():.2f}")
    print(f"  Min: ${df['adr'].min():.2f}")
    print(f"  Max: ${df['adr'].max():.2f}")
    print(f"  Std Dev: ${df['adr'].std():.2f}")

# 7. LEAD TIME ANALYSIS
print("\n7. BOOKING LEAD TIME ANALYSIS")
print("-" * 80)
if 'lead_time' in df.columns:
    print(f"Average Lead Time: {df['lead_time'].mean():.1f} days")
    print(f"Median Lead Time: {df['lead_time'].median():.1f} days")
    print(f"Max Lead Time: {df['lead_time'].max()} days")
    
    # Lead time categories
    zero_lead = len(df[df['lead_time'] == 0])
    short_lead = len(df[(df['lead_time'] > 0) & (df['lead_time'] <= 7)])
    medium_lead = len(df[(df['lead_time'] > 7) & (df['lead_time'] <= 30)])
    long_lead = len(df[df['lead_time'] > 30])
    
    print(f"\nLead Time Categories:")
    print(f"  Same Day: {zero_lead:,} ({zero_lead/len(df)*100:.1f}%)")
    print(f"  1-7 days: {short_lead:,} ({short_lead/len(df)*100:.1f}%)")
    print(f"  8-30 days: {medium_lead:,} ({medium_lead/len(df)*100:.1f}%)")
    print(f"  >30 days: {long_lead:,} ({long_lead/len(df)*100:.1f}%)")

# 8. SEASONALITY ANALYSIS
print("\n8. SEASONALITY & MONTHLY TRENDS")
print("-" * 80)
if 'arrival_date_month' in df.columns:
    monthly = df['arrival_date_month'].value_counts().sort_index()
    print(f"Bookings by Month:")
    for month, count in monthly.items():
        pct = (count / len(df)) * 100
        print(f"  {month}: {count:,} ({pct:.1f}%)")
    
    peak_month = monthly.idxmax()
    low_month = monthly.idxmin()
    print(f"\nPeak Season: {peak_month} ({monthly[peak_month]:,} bookings)")
    print(f"Low Season: {low_month} ({monthly[low_month]:,} bookings)")

# 9. MARKET SEGMENT ANALYSIS
print("\n9. MARKET SEGMENT DISTRIBUTION")
print("-" * 80)
if 'market_segment' in df.columns:
    segments = df['market_segment'].value_counts()
    for segment, count in segments.items():
        pct = (count / len(df)) * 100
        print(f"  {segment}: {count:,} ({pct:.1f}%)")

# 10. CUSTOMER TYPE ANALYSIS
print("\n10. CUSTOMER TYPE DISTRIBUTION")
print("-" * 80)
if 'customer_type' in df.columns:
    customers = df['customer_type'].value_counts()
    for ctype, count in customers.items():
        pct = (count / len(df)) * 100
        print(f"  {ctype}: {count:,} ({pct:.1f}%)")

# 11. CANCELLATION PATTERNS
print("\n11. CANCELLATION ANALYSIS BY FACTORS")
print("-" * 80)
if 'is_canceled' in df.columns:
    if 'hotel' in df.columns:
        print("\nCancellation Rate by Hotel Type:")
        cancel_by_hotel = df.groupby('hotel')['is_canceled'].mean() * 100
        for hotel, rate in cancel_by_hotel.items():
            print(f"  {hotel}: {rate:.1f}%")
    
    if 'market_segment' in df.columns:
        print("\nCancellation Rate by Market Segment:")
        cancel_by_segment = df.groupby('market_segment')['is_canceled'].mean() * 100
        for segment, rate in cancel_by_segment.items():
            print(f"  {segment}: {rate:.1f}%")
    
    if 'lead_time' in df.columns:
        print("\nCancellation Rate by Lead Time:")
        df_temp = df.copy()
        df_temp['lead_time_cat'] = pd.cut(df_temp['lead_time'], 
                                          bins=[0, 7, 14, 30, 90, 365],
                                          labels=['0-7 days', '8-14 days', '15-30 days', '31-90 days', '>90 days'])
        cancel_by_lead = df_temp.groupby('lead_time_cat')['is_canceled'].mean() * 100
        for period, rate in cancel_by_lead.items():
            print(f"  {period}: {rate:.1f}%")

# 12. KEY INSIGHTS
print("\n12. KEY INSIGHTS & FINDINGS")
print("-" * 80)

insights = []

# Cancellation insight
if 'is_canceled' in df.columns:
    cancel_rate = df['is_canceled'].mean() * 100
    if cancel_rate > 30:
        insights.append(f"⚠️  HIGH CANCELLATION RATE: {cancel_rate:.1f}% - Implement stricter policies")
    elif cancel_rate > 20:
        insights.append(f"⚠️  MODERATE CANCELLATION: {cancel_rate:.1f}% - Consider flexible options")
    else:
        insights.append(f"✓ LOW CANCELLATION RATE: {cancel_rate:.1f}%")

# Lead time insight
if 'lead_time' in df.columns:
    avg_lead = df['lead_time'].mean()
    if avg_lead < 30:
        insights.append(f"📅 SHORT LEAD TIME: {avg_lead:.0f} days - Focus on short-term bookings")
    else:
        insights.append(f"📅 LONG LEAD TIME: {avg_lead:.0f} days - Develop early-bird incentives")

# Seasonality insight
if 'arrival_date_month' in df.columns:
    monthly = df['arrival_date_month'].value_counts()
    ratio = monthly.max() / monthly.min()
    insights.append(f"📊 SEASONALITY RATIO: {ratio:.1f}x (Peak/Low) - Need dynamic pricing")

# ADR insight
if 'adr' in df.columns:
    high_adr_pct = len(df[df['adr'] > df['adr'].quantile(0.75)]) / len(df) * 100
    insights.append(f"💰 HIGH-VALUE BOOKINGS: {high_adr_pct:.1f}% of bookings exceed 75th percentile ADR")

# Hotel type insight
if 'hotel' in df.columns:
    hotel_dist = df['hotel'].value_counts()
    if len(hotel_dist) == 2:
        max_hotel = hotel_dist.index[0]
        max_pct = (hotel_dist.iloc[0] / len(df)) * 100
        insights.append(f"🏨 DOMINANT TYPE: {max_hotel} accounts for {max_pct:.1f}% of bookings")

for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

# 13. RECOMMENDATIONS
print("\n13. STRATEGIC RECOMMENDATIONS")
print("-" * 80)

recommendations = [
    "1. Implement dynamic pricing based on seasonal demand patterns",
    "2. Develop targeted retention strategies for high-risk cancellation segments",
    "3. Create loyalty programs for repeat customers",
    "4. Optimize inventory management for peak seasons",
    "5. Enhance marketing for low-season periods to boost demand",
    "6. Focus on high-value customer segments identified in analysis",
    "7. Set up early-warning system for bookings with high cancellation risk",
    "8. Develop flexible booking options to reduce cancellations"
]

for rec in recommendations:
    print(f"  {rec}")

print("\n" + "=" * 80)
print("END OF REPORT")
print("=" * 80)
