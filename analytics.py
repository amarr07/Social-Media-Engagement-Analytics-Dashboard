"""
Analytics functions for social media engagement calculation and ranking
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple


def calculate_engagement(df: pd.DataFrame, likes_col: str, comments_col: str, 
                        shares_col: str) -> pd.DataFrame:
    """
    Calculate engagement score for each post
    Formula: Engagement = 1×Likes + 2×Comments + 3×Shares
    
    Args:
        df: DataFrame with post data
        likes_col: Column name for likes
        comments_col: Column name for comments
        shares_col: Column name for shares
        
    Returns:
        DataFrame with added 'engagement' column
    """
    df = df.copy()
    
    # Ensure numeric values
    df[likes_col] = pd.to_numeric(df[likes_col], errors='coerce').fillna(0)
    df[comments_col] = pd.to_numeric(df[comments_col], errors='coerce').fillna(0)
    df[shares_col] = pd.to_numeric(df[shares_col], errors='coerce').fillna(0)
    
    # Calculate engagement
    df['engagement'] = (
        1 * df[likes_col] + 
        2 * df[comments_col] + 
        3 * df[shares_col]
    )
    
    return df


def aggregate_by_day(df: pd.DataFrame, page_col: str, date_col: str) -> pd.DataFrame:
    """
    Aggregate engagement by page/profile and date
    
    Args:
        df: DataFrame with post data and engagement
        page_col: Column name for page/profile/channel
        date_col: Column name for date
        
    Returns:
        DataFrame aggregated by page and date
    """
    df = df.copy()
    
    # Ensure date is datetime
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    # Extract just the date (remove time component)
    df['date_only'] = df[date_col].dt.date
    
    # Aggregate by page and date
    daily_agg = df.groupby([page_col, 'date_only']).agg({
        'engagement': 'sum',
        date_col: 'count'  # Count posts per day
    }).reset_index()
    
    daily_agg.columns = [page_col, 'date', 'total_engagement', 'post_count']
    
    return daily_agg


def identify_daily_winners(daily_df: pd.DataFrame, page_col: str) -> pd.DataFrame:
    """
    Identify the page with highest engagement for each day
    Adds 'day_won' column (1 for winner, 0 for others)
    
    Args:
        daily_df: DataFrame aggregated by page and date
        page_col: Column name for page/profile/channel
        
    Returns:
        DataFrame with 'day_won' column added
    """
    df = daily_df.copy()
    
    # For each date, find the page with max engagement
    idx_max = df.groupby('date')['total_engagement'].idxmax()
    
    # Initialize day_won column with 0
    df['day_won'] = 0
    
    # Set day_won to 1 for winners
    df.loc[idx_max, 'day_won'] = 1
    
    return df


def aggregate_overall(df: pd.DataFrame, page_col: str, daily_winners_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create overall aggregation by page/profile with total posts, engagement, and days won
    
    Args:
        df: Original DataFrame with all posts
        page_col: Column name for page/profile/channel
        daily_winners_df: DataFrame with daily winners information
        
    Returns:
        Aggregated DataFrame by page
    """
    # Aggregate total posts and engagement
    overall = df.groupby(page_col).agg({
        'engagement': ['sum', 'count']  # Sum engagement and count posts
    }).reset_index()
    
    # Flatten column names
    overall.columns = [page_col, 'total_engagement', 'total_posts']
    
    # Calculate days won
    days_won = daily_winners_df.groupby(page_col)['day_won'].sum().reset_index()
    days_won.columns = [page_col, 'days_won']
    
    # Merge
    overall = overall.merge(days_won, on=page_col, how='left')
    overall['days_won'] = overall['days_won'].fillna(0).astype(int)
    
    return overall


def calculate_percentage_change(current_value: float, previous_value: float) -> float:
    """
    Calculate percentage change between two values
    Formula: ((Current - Previous) / Previous) × 100
    
    Args:
        current_value: Current period value
        previous_value: Previous period value
        
    Returns:
        Percentage change
    """
    if pd.isna(previous_value) or previous_value == 0:
        return 0.0
    
    return ((current_value - previous_value) / previous_value) * 100


def add_comparison_data(current_df: pd.DataFrame, previous_df: pd.DataFrame, 
                       page_col: str) -> pd.DataFrame:
    """
    Add comparison metrics (% change in posts and engagement)
    
    Args:
        current_df: Current period DataFrame with aggregated data
        previous_df: Previous period DataFrame with posts and engagement
        page_col: Column name for page/profile/channel
        
    Returns:
        DataFrame with percentage change columns added
    """
    df = current_df.copy()
    
    # Ensure previous_df has required columns
    if 'total_posts' not in previous_df.columns or 'total_engagement' not in previous_df.columns:
        # If previous_df doesn't have aggregated data, return current with 0% change
        df['posts_change_pct'] = 0.0
        df['engagement_change_pct'] = 0.0
        return df
    
    # Merge with previous data
    comparison = df.merge(
        previous_df[[page_col, 'total_posts', 'total_engagement']], 
        on=page_col, 
        how='left', 
        suffixes=('_current', '_previous')
    )
    
    # Rename current columns if needed
    if 'total_posts_current' in comparison.columns:
        comparison.rename(columns={
            'total_posts_current': 'total_posts',
            'total_engagement_current': 'total_engagement'
        }, inplace=True)
    
    # Calculate percentage changes
    comparison['posts_change_pct'] = comparison.apply(
        lambda row: calculate_percentage_change(
            row['total_posts'], 
            row.get('total_posts_previous', 0)
        ), 
        axis=1
    )
    
    comparison['engagement_change_pct'] = comparison.apply(
        lambda row: calculate_percentage_change(
            row['total_engagement'], 
            row.get('total_engagement_previous', 0)
        ), 
        axis=1
    )
    
    # Drop previous columns
    comparison = comparison.drop(columns=[
        col for col in comparison.columns 
        if col.endswith('_previous')
    ])
    
    return comparison


def add_follower_data(df: pd.DataFrame, follower_df: pd.DataFrame, 
                     page_col: str, follower_col: str) -> pd.DataFrame:
    """
    Add follower count to the aggregated data
    
    Args:
        df: Aggregated DataFrame
        follower_df: DataFrame with follower information
        page_col: Column name for page/profile/channel
        follower_col: Column name for followers
        
    Returns:
        DataFrame with followers column added
    """
    result = df.merge(
        follower_df[[page_col, follower_col]], 
        on=page_col, 
        how='left'
    )
    
    # Rename follower column to standard name
    result.rename(columns={follower_col: 'followers'}, inplace=True)
    
    # Fill missing follower counts with 0
    result['followers'] = result['followers'].fillna(0).astype(int)
    
    return result


def rank_pages(df: pd.DataFrame, rank_by: str = 'total_engagement') -> pd.DataFrame:
    """
    Rank pages by specified metric (default: total_engagement)
    
    Args:
        df: DataFrame with page data
        rank_by: Column name to rank by
        
    Returns:
        DataFrame with 'rank' column added, sorted by rank
    """
    df = df.copy()
    
    # Create rank (1 is highest)
    df['rank'] = df[rank_by].rank(ascending=False, method='min').astype(int)
    
    # Sort by rank
    df = df.sort_values('rank')
    
    return df


def create_leaderboard(performance_df: pd.DataFrame, previous_df: pd.DataFrame,
                      follower_df: pd.DataFrame, page_col: str, 
                      date_col: str, likes_col: str, comments_col: str,
                      shares_col: str, follower_col: str,
                      previous_posts_col: str = 'total_posts',
                      previous_engagement_col: str = 'total_engagement') -> pd.DataFrame:
    """
    Create complete leaderboard with all metrics
    
    Args:
        performance_df: Current period performance data
        previous_df: Previous period comparison data
        follower_df: Follower count data
        page_col: Column name for page/profile/channel
        date_col: Column name for date
        likes_col: Column name for likes
        comments_col: Column name for comments
        shares_col: Column name for shares
        follower_col: Column name for followers
        previous_posts_col: Column name for posts in previous data
        previous_engagement_col: Column name for engagement in previous data
        
    Returns:
        Complete leaderboard DataFrame
    """
    # Step 1: Calculate engagement for each post
    df_with_engagement = calculate_engagement(
        performance_df, 
        likes_col, 
        comments_col, 
        shares_col
    )
    
    # Step 2: Aggregate by day
    daily_agg = aggregate_by_day(df_with_engagement, page_col, date_col)
    
    # Step 3: Identify daily winners
    daily_with_winners = identify_daily_winners(daily_agg, page_col)
    
    # Step 4: Create overall aggregation
    overall = aggregate_overall(df_with_engagement, page_col, daily_with_winners)
    
    # Step 5: Prepare previous data with standard column names
    previous_prepared = previous_df.copy()
    if previous_posts_col in previous_prepared.columns:
        previous_prepared.rename(columns={previous_posts_col: 'total_posts'}, inplace=True)
    if previous_engagement_col in previous_prepared.columns:
        previous_prepared.rename(columns={previous_engagement_col: 'total_engagement'}, inplace=True)
    
    # Step 6: Add comparison data
    with_comparison = add_comparison_data(overall, previous_prepared, page_col)
    
    # Step 7: Add follower data
    with_followers = add_follower_data(with_comparison, follower_df, page_col, follower_col)
    
    # Step 8: Rank pages
    leaderboard = rank_pages(with_followers, 'total_engagement')
    
    # Step 9: Reorder columns for better display
    column_order = [
        'rank',
        page_col,
        'followers',
        'total_posts',
        'total_engagement',
        'days_won',
        'posts_change_pct',
        'engagement_change_pct'
    ]
    
    # Only include columns that exist
    final_columns = [col for col in column_order if col in leaderboard.columns]
    leaderboard = leaderboard[final_columns]
    
    # Rename columns for display
    leaderboard.columns = [
        'Rank',
        'Page/Profile/Channel',
        'Followers',
        'Total Posts',
        'Total Engagement',
        'Days Won',
        '% Change Posts',
        '% Change Engagement'
    ]
    
    return leaderboard
