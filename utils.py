"""
Utility functions for social media engagement analytics
"""
import pandas as pd
import streamlit as st
from typing import Optional, List, Dict


def detect_file_type(uploaded_file) -> str:
    """
    Detect file type from uploaded file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: File extension ('xlsx' or 'xls')
    """
    filename = uploaded_file.name
    if filename.endswith('.xlsx'):
        return 'xlsx'
    elif filename.endswith('.xls'):
        return 'xls'
    else:
        return 'unknown'


def load_excel_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load Excel file into pandas DataFrame
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        DataFrame or None if error occurs
    """
    try:
        file_type = detect_file_type(uploaded_file)
        
        if file_type == 'xlsx':
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif file_type == 'xls':
            df = pd.read_excel(uploaded_file, engine='xlrd')
        else:
            st.error(f"Unsupported file type. Please upload .xlsx or .xls files.")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


def get_column_preview(df: pd.DataFrame, num_rows: int = 5) -> pd.DataFrame:
    """
    Get a preview of the DataFrame
    
    Args:
        df: pandas DataFrame
        num_rows: Number of rows to preview
        
    Returns:
        Preview DataFrame
    """
    return df.head(num_rows)


def validate_required_columns(df: pd.DataFrame, required_cols: List[str]) -> tuple[bool, List[str]]:
    """
    Validate that DataFrame contains required columns
    
    Args:
        df: pandas DataFrame
        required_cols: List of required column names
        
    Returns:
        Tuple of (is_valid, missing_columns)
    """
    df_columns = df.columns.tolist()
    missing = [col for col in required_cols if col not in df_columns]
    
    return len(missing) == 0, missing


def create_column_mapping_ui(df: pd.DataFrame, file_label: str, required_fields: Dict[str, str]) -> Dict[str, str]:
    """
    Create UI for mapping DataFrame columns to required fields
    
    Args:
        df: pandas DataFrame
        file_label: Label for the file being mapped
        required_fields: Dict of field_key: field_description
        
    Returns:
        Dict mapping field_key to selected column name
    """
    st.subheader(f"Map Columns for {file_label}")
    
    available_columns = [''] + df.columns.tolist()
    mapping = {}
    
    for field_key, field_desc in required_fields.items():
        # Try to auto-detect column based on common patterns
        auto_detected = auto_detect_column(df.columns.tolist(), field_key)
        default_index = available_columns.index(auto_detected) if auto_detected in available_columns else 0
        
        selected = st.selectbox(
            f"Select column for **{field_desc}**",
            available_columns,
            index=default_index,
            key=f"{file_label}_{field_key}"
        )
        mapping[field_key] = selected
    
    return mapping


def auto_detect_column(columns: List[str], field_key: str) -> Optional[str]:
    """
    Auto-detect likely column name based on field key
    
    Args:
        columns: List of column names
        field_key: Field identifier
        
    Returns:
        Best matching column name or None
    """
    # Convert columns to lowercase for matching
    columns_lower = {col.lower(): col for col in columns}
    
    # Patterns for each field type
    patterns = {
        'page_name': ['page', 'profile', 'channel', 'account', 'name'],
        'post_id': ['post', 'id', 'post_id', 'post_name', 'content'],
        'date': ['date', 'post_date', 'published', 'time', 'posted'],
        'likes': ['like', 'likes', 'love', 'reactions'],
        'comments': ['comment', 'comments', 'replies'],
        'shares': ['share', 'shares', 'repost', 'reposts'],
        'posts': ['post', 'posts', 'total_posts'],
        'post_count': ['post_count', 'post', 'posts', 'count'],
        'engagement': ['engagement', 'total_engagement', 'eng'],
        'day_won': ['day_won', 'days_won', 'won', 'days'],
        'rank': ['rank', 'ranking', 'position'],
        'followers': ['follower', 'followers', 'fans', 'subscribers']
    }
    
    if field_key not in patterns:
        return None
    
    # Try to find best match
    for pattern in patterns[field_key]:
        for col_lower, col_original in columns_lower.items():
            if pattern in col_lower:
                return col_original
    
    return None


def validate_mapping(mapping: Dict[str, str], allow_empty: List[str] = []) -> tuple[bool, List[str]]:
    """
    Validate that all required fields are mapped
    
    Args:
        mapping: Dict of field mappings
        allow_empty: List of field keys that can be empty
        
    Returns:
        Tuple of (is_valid, empty_fields)
    """
    empty_fields = []
    
    for field_key, column_name in mapping.items():
        if not column_name and field_key not in allow_empty:
            empty_fields.append(field_key)
    
    return len(empty_fields) == 0, empty_fields


def safe_numeric_conversion(series: pd.Series) -> pd.Series:
    """
    Safely convert series to numeric, replacing errors with 0
    
    Args:
        series: pandas Series
        
    Returns:
        Numeric series
    """
    return pd.to_numeric(series, errors='coerce').fillna(0)


def safe_date_conversion(series: pd.Series) -> pd.Series:
    """
    Safely convert series to datetime
    
    Args:
        series: pandas Series
        
    Returns:
        Datetime series
    """
    return pd.to_datetime(series, errors='coerce')
