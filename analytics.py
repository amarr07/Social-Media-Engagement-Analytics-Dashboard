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
                       page_col: str, previous_posts_col: str = 'post_count',
                       previous_engagement_col: str = 'engagement',
                       previous_day_won_col: str = 'day_won',
                       previous_rank_col: str = 'rank') -> pd.DataFrame:
    """
    Add comparison metrics (% change in posts and engagement) and last fortnight data
    
    Args:
        current_df: Current period DataFrame with aggregated data
        previous_df: Last fortnight DataFrame with engagement, post count, day won, rank
        page_col: Column name for page/profile/channel
        previous_posts_col: Column name for posts in previous data (default: 'post_count')
        previous_engagement_col: Column name for engagement in previous data (default: 'engagement')
        previous_day_won_col: Column name for day won in previous data (default: 'day_won')
        previous_rank_col: Column name for rank in previous data (default: 'rank')
        
    Returns:
        DataFrame with percentage change columns and last fortnight metrics added
    """
    df = current_df.copy()
    
    # Check if required columns exist in previous_df
    required_cols = [previous_posts_col, previous_engagement_col]
    missing_cols = [col for col in required_cols if col not in previous_df.columns]
    
    if missing_cols:
        # If previous_df doesn't have required data, return current with default values
        df['posts_change_pct'] = 0.0
        df['engagement_change_pct'] = 0.0
        df['last_fortnight_day_won'] = 0
        df['last_fortnight_rank'] = 0
        return df
    
    # Prepare columns to merge from previous data
    merge_cols = [page_col, previous_posts_col, previous_engagement_col]
    if previous_day_won_col in previous_df.columns:
        merge_cols.append(previous_day_won_col)
    if previous_rank_col in previous_df.columns:
        merge_cols.append(previous_rank_col)
    
    # Merge with previous data
    comparison = df.merge(
        previous_df[merge_cols], 
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
    
    # Calculate percentage changes using the mapped column names
    prev_posts_col_name = f'{previous_posts_col}_previous' if f'{previous_posts_col}_previous' in comparison.columns else previous_posts_col
    prev_eng_col_name = f'{previous_engagement_col}_previous' if f'{previous_engagement_col}_previous' in comparison.columns else previous_engagement_col
    
    comparison['posts_change_pct'] = comparison.apply(
        lambda row: calculate_percentage_change(
            row['total_posts'], 
            row.get(prev_posts_col_name, 0)
        ), 
        axis=1
    )
    
    comparison['engagement_change_pct'] = comparison.apply(
        lambda row: calculate_percentage_change(
            row['total_engagement'], 
            row.get(prev_eng_col_name, 0)
        ), 
        axis=1
    )
    
    # Add last fortnight day won and rank
    if previous_day_won_col in previous_df.columns:
        day_won_col = f'{previous_day_won_col}_previous' if f'{previous_day_won_col}_previous' in comparison.columns else previous_day_won_col
        comparison['last_fortnight_day_won'] = comparison.get(day_won_col, 0).fillna(0).astype(int)
    else:
        comparison['last_fortnight_day_won'] = 0
    
    if previous_rank_col in previous_df.columns:
        rank_col = f'{previous_rank_col}_previous' if f'{previous_rank_col}_previous' in comparison.columns else previous_rank_col
        comparison['last_fortnight_rank'] = comparison.get(rank_col, 0).fillna(0).astype(int)
    else:
        comparison['last_fortnight_rank'] = 0
    
    # Drop previous columns (keep last fortnight metrics)
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
                      previous_posts_col: str = 'post_count',
                      previous_engagement_col: str = 'engagement',
                      previous_day_won_col: str = 'day_won',
                      previous_rank_col: str = 'rank') -> pd.DataFrame:
    """
    Create complete leaderboard with all metrics
    
    Args:
        performance_df: Current period performance data
        previous_df: Last fortnight comparison data
        follower_df: Follower count data
        page_col: Column name for page/profile/channel
        date_col: Column name for date
        likes_col: Column name for likes
        comments_col: Column name for comments
        shares_col: Column name for shares
        follower_col: Column name for followers
        previous_posts_col: Column name for posts in previous data (default: 'post_count')
        previous_engagement_col: Column name for engagement in previous data (default: 'engagement')
        previous_day_won_col: Column name for day won in previous data (default: 'day_won')
        previous_rank_col: Column name for rank in previous data (default: 'rank')
        
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
    
    # Step 5: Add comparison data with last fortnight metrics
    with_comparison = add_comparison_data(
        overall, 
        previous_df, 
        page_col,
        previous_posts_col,
        previous_engagement_col,
        previous_day_won_col,
        previous_rank_col
    )
    
    # Step 6: Add follower data
    with_followers = add_follower_data(with_comparison, follower_df, page_col, follower_col)
    
    # Step 7: Rank pages
    leaderboard = rank_pages(with_followers, 'total_engagement')
    
    # Step 8: Reorder columns for display (per instruction.md spec)
    # Order: follower, page name, post, engagement, rank, day won, % change post, % change engagement, last fortnight day won, last fortnight rank
    column_order = [
        'followers',
        page_col,
        'total_posts',
        'total_engagement',
        'rank',
        'days_won',
        'posts_change_pct',
        'engagement_change_pct',
        'last_fortnight_day_won',
        'last_fortnight_rank'
    ]
    
    # Only include columns that exist
    final_columns = [col for col in column_order if col in leaderboard.columns]
    leaderboard = leaderboard[final_columns]
    
    # Rename columns for display
    display_names = {
        'followers': 'Follower',
        page_col: 'Page/Profile/Channel',
        'total_posts': 'Post',
        'total_engagement': 'Engagement',
        'rank': 'Rank',
        'days_won': 'Day Won',
        'posts_change_pct': '% Change in Post',
        'engagement_change_pct': '% Change in Engagement',
        'last_fortnight_day_won': 'Last Fortnight Day Won',
        'last_fortnight_rank': 'Last Fortnight Rank'
    }
    
    leaderboard.rename(columns=display_names, inplace=True)
    
    return leaderboard
