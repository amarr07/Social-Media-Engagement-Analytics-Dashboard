"""
Social Media Performance Dashboard
Single-page Streamlit application with sidebar uploads
"""
import streamlit as st
import pandas as pd
from io import BytesIO
import utils
import analytics


# Page configuration
st.set_page_config(
    page_title="Social Media Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .rank-1 { background-color: #ffd700; color: #000; }
    .rank-2 { background-color: #c0c0c0; color: #000; }
    .rank-3 { background-color: #cd7f32; color: #fff; }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'performance_df' not in st.session_state:
        st.session_state.performance_df = None
    if 'previous_df' not in st.session_state:
        st.session_state.previous_df = None
    if 'follower_df' not in st.session_state:
        st.session_state.follower_df = None
    if 'performance_mapping' not in st.session_state:
        st.session_state.performance_mapping = None
    if 'previous_mapping' not in st.session_state:
        st.session_state.previous_mapping = None
    if 'follower_mapping' not in st.session_state:
        st.session_state.follower_mapping = None
    if 'show_mapping' not in st.session_state:
        st.session_state.show_mapping = False
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = None


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">📊 Social Media Performance Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze engagement metrics across all your pages/profiles/channels</p>', unsafe_allow_html=True)
    
    # Sidebar for file uploads
    with st.sidebar:
        st.markdown("## 📁 Upload Data Files")
        st.markdown("Upload three Excel files to analyze your social media performance.")
        st.markdown("---")
        
        # File 1: Daily Post Performance
        st.markdown("### 📊 File 1: Daily Post Performance")
        st.caption("Required columns: page/profile/channel name, post name/id, date, like, comment, share")
        performance_file = st.file_uploader(
            "Upload Performance Data",
            type=['xlsx', 'xls'],
            key='performance_upload',
            help="Excel file with daily post-level performance data"
        )
        
        if performance_file:
            df = utils.load_excel_file(performance_file)
            if df is not None:
                st.session_state.performance_df = df
                st.success(f"✅ Loaded {len(df)} rows")
        
        st.markdown("---")
        
        # File 2: Last Fortnight Performance
        st.markdown("### 📅 File 2: Last Fortnight Performance")
        st.caption("Required columns: page/profile/channel name, engagement, post count, day won, rank")
        previous_file = st.file_uploader(
            "Upload Last Fortnight Data",
            type=['xlsx', 'xls'],
            key='previous_upload',
            help="Excel file with last fortnight aggregated performance"
        )
        
        if previous_file:
            df = utils.load_excel_file(previous_file)
            if df is not None:
                st.session_state.previous_df = df
                st.success(f"✅ Loaded {len(df)} rows")
        
        st.markdown("---")
        
        # File 3: Follower Counts
        st.markdown("### 👥 File 3: Follower Counts")
        st.caption("Required columns: page/profile/channel name, follower")
        follower_file = st.file_uploader(
            "Upload Follower Data",
            type=['xlsx', 'xls'],
            key='follower_upload',
            help="Excel file with current follower counts"
        )
        
        if follower_file:
            df = utils.load_excel_file(follower_file)
            if df is not None:
                st.session_state.follower_df = df
                st.success(f"✅ Loaded {len(df)} rows")
        
        st.markdown("---")
        
        # Check if all files uploaded
        all_uploaded = (
            st.session_state.performance_df is not None and
            st.session_state.previous_df is not None and
            st.session_state.follower_df is not None
        )
        
        if all_uploaded:
            if st.button("🔗 Map Columns & Generate Dashboard", type="primary", use_container_width=True):
                st.session_state.show_mapping = True
                st.rerun()
        else:
            st.info("⚠️ Upload all three files to continue")
        
        st.markdown("---")
        st.markdown("### 📐 Engagement Formula")
        st.latex(r"E = 1 \times L + 2 \times C + 3 \times S")
        st.caption("L=Likes, C=Comments, S=Shares")
    
    # Main content area
    if not all_uploaded:
        # Show welcome/instructions when files not uploaded
        st.info("👈 Please upload all three Excel files using the sidebar to get started.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 📊 File 1: Daily Posts")
            st.markdown("""
            Upload your daily post performance data with:
            - Page/Profile/Channel name
            - Post ID or name
            - Post date
            - Likes count
            - Comments count
            - Shares count
            """)
        
        with col2:
            st.markdown("### 📅 File 2: Last Fortnight")
            st.markdown("""
            Upload last fortnight's aggregated data with:
            - Page/Profile/Channel name
            - Total engagement score
            - Post count
            - Days won
            - Rank
            """)
        
        with col3:
            st.markdown("### 👥 File 3: Followers")
            st.markdown("""
            Upload current follower data with:
            - Page/Profile/Channel name
            - Follower count
            """)
        
        st.markdown("---")
        st.markdown("### 📋 What You'll Get")
        st.markdown("""
        After uploading all files, you'll see a comprehensive dashboard with:
        - **Engagement rankings** for all pages/profiles/channels
        - **Performance comparisons** vs. last fortnight
        - **Daily winner tracking** showing which pages won each day
        - **Interactive table** with sorting and filtering
        - **Export options** to download results
        """)
    
    elif st.session_state.show_mapping:
        # Show column mapping interface
        show_column_mapping()
    
    elif st.session_state.leaderboard is not None:
        # Show the dashboard
        show_dashboard()


def show_column_mapping():
    """Display column mapping interface"""
    st.markdown("## 🔗 Column Mapping")
    st.info("Map your data columns to the required fields. Auto-detection is provided as a starting point.")
    
    # Performance file mapping
    with st.expander("📊 File 1: Daily Post Performance - Column Mapping", expanded=True):
        st.dataframe(st.session_state.performance_df.head(3), use_container_width=True)
        
        performance_fields = {
            'page_name': 'Page/Profile/Channel Name',
            'post_id': 'Post ID/Name',
            'date': 'Post Date',
            'likes': 'Likes',
            'comments': 'Comments',
            'shares': 'Shares'
        }
        
        performance_mapping = utils.create_column_mapping_ui(
            st.session_state.performance_df,
            "Performance",
            performance_fields
        )
    
    # Previous period mapping
    with st.expander("📅 File 2: Last Fortnight Performance - Column Mapping", expanded=True):
        st.dataframe(st.session_state.previous_df.head(3), use_container_width=True)
        
        previous_fields = {
            'page_name': 'Page/Profile/Channel Name',
            'engagement': 'Total Engagement',
            'post_count': 'Post Count',
            'day_won': 'Day Won',
            'rank': 'Rank'
        }
        
        previous_mapping = utils.create_column_mapping_ui(
            st.session_state.previous_df,
            "LastFortnight",
            previous_fields
        )
    
    # Follower data mapping
    with st.expander("👥 File 3: Follower Counts - Column Mapping", expanded=True):
        st.dataframe(st.session_state.follower_df.head(3), use_container_width=True)
        
        follower_fields = {
            'page_name': 'Page/Profile/Channel Name',
            'followers': 'Followers Count'
        }
        
        follower_mapping = utils.create_column_mapping_ui(
            st.session_state.follower_df,
            "Follower",
            follower_fields
        )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Upload", use_container_width=True):
            st.session_state.show_mapping = False
            st.rerun()
    
    with col3:
        # Validate mappings
        perf_valid, perf_empty = utils.validate_mapping(performance_mapping)
        prev_valid, prev_empty = utils.validate_mapping(previous_mapping)
        foll_valid, foll_empty = utils.validate_mapping(follower_mapping)
        
        if perf_valid and prev_valid and foll_valid:
            if st.button("🚀 Generate Dashboard", type="primary", use_container_width=True):
                with st.spinner("Calculating engagement metrics and rankings..."):
                    try:
                        leaderboard = analytics.create_leaderboard(
                            performance_df=st.session_state.performance_df,
                            previous_df=st.session_state.previous_df,
                            follower_df=st.session_state.follower_df,
                            page_col=performance_mapping['page_name'],
                            date_col=performance_mapping['date'],
                            likes_col=performance_mapping['likes'],
                            comments_col=performance_mapping['comments'],
                            shares_col=performance_mapping['shares'],
                            follower_col=follower_mapping['followers'],
                            previous_posts_col=previous_mapping['post_count'],
                            previous_engagement_col=previous_mapping['engagement'],
                            previous_day_won_col=previous_mapping['day_won'],
                            previous_rank_col=previous_mapping['rank']
                        )
                        
                        st.session_state.leaderboard = leaderboard
                        st.session_state.show_mapping = False
                        st.success("✅ Dashboard generated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error generating dashboard: {str(e)}")
                        with st.expander("See detailed error"):
                            st.exception(e)
        else:
            st.button("🚀 Generate Dashboard", disabled=True, use_container_width=True)
            errors = []
            if not perf_valid:
                errors.append(f"Performance: {', '.join(perf_empty)}")
            if not prev_valid:
                errors.append(f"Last Fortnight: {', '.join(prev_empty)}")
            if not foll_valid:
                errors.append(f"Follower: {', '.join(foll_empty)}")
            st.error(f"⚠️ Please map all required fields:\n" + "\n".join(f"- {e}" for e in errors))


def show_dashboard():
    """Display the main dashboard with results"""
    st.markdown("## 🏆 Performance Dashboard")
    
    leaderboard = st.session_state.leaderboard.copy()
    
    # Format engagement values to millions with M suffix
    def format_engagement(value):
        """Format engagement value as millions with 2 decimals"""
        return f"{value / 1_000_000:.2f}M"
    
    def format_percentage(value):
        """Format percentage as whole number with % sign"""
        if pd.isna(value):
            return "0%"
        return f"{int(round(value))}%"
    
    # Create display version with formatted values
    display_leaderboard = leaderboard.copy()
    display_leaderboard['Engagement'] = leaderboard['Engagement'].apply(
        lambda x: format_engagement(x) if pd.notna(x) else "0.00M"
    )
    display_leaderboard['% Change in Post'] = leaderboard['% Change in Post'].apply(format_percentage)
    display_leaderboard['% Change in Engagement'] = leaderboard['% Change in Engagement'].apply(format_percentage)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Pages",
            len(leaderboard),
            help="Total number of pages/profiles/channels analyzed"
        )
    
    with col2:
        total_posts = leaderboard['Post'].sum()
        st.metric(
            "Total Posts",
            f"{total_posts:,}",
            help="Sum of all posts across all pages in current period"
        )
    
    with col3:
        total_engagement = leaderboard['Engagement'].sum()
        st.metric(
            "Total Engagement",
            f"{total_engagement / 1_000_000:.2f}M",
            help="Sum of all engagement scores (1×Likes + 2×Comments + 3×Shares) in millions"
        )
    
    with col4:
        avg_engagement = leaderboard['Engagement'].mean()
        st.metric(
            "Avg Engagement",
            f"{avg_engagement / 1_000_000:.2f}M",
            help="Average engagement score per page in millions"
        )
    
    st.markdown("---")
    
    # Main leaderboard table with tooltips
    st.markdown("### 📋 Performance Leaderboard")
    
    # Column configuration with help text
    column_config = {
        "Follower": st.column_config.NumberColumn(
            "Follower",
            help="Current follower count for the page/profile/channel",
            format="%d"
        ),
        "Page/Profile/Channel": st.column_config.TextColumn(
            "Page/Profile/Channel",
            help="Name of the social media page, profile, or channel"
        ),
        "Post": st.column_config.NumberColumn(
            "Post",
            help="Total number of posts in the current period",
            format="%d"
        ),
        "Engagement": st.column_config.TextColumn(
            "Engagement",
            help="Total engagement score calculated as: 1×Likes + 2×Comments + 3×Shares (in millions)"
        ),
        "Rank": st.column_config.NumberColumn(
            "Rank",
            help="Current ranking based on total engagement (1 = highest)",
            format="%d"
        ),
        "Day Won": st.column_config.NumberColumn(
            "Day Won",
            help="Number of days this page had the highest engagement",
            format="%d"
        ),
        "% Change in Post": st.column_config.TextColumn(
            "% Change in Post",
            help="Percentage change in post count compared to last fortnight"
        ),
        "% Change in Engagement": st.column_config.TextColumn(
            "% Change in Engagement",
            help="Percentage change in engagement compared to last fortnight"
        ),
        "Last Fortnight Day Won": st.column_config.NumberColumn(
            "Last Fortnight Day Won",
            help="Number of days won in the last fortnight period",
            format="%d"
        ),
        "Last Fortnight Rank": st.column_config.NumberColumn(
            "Last Fortnight Rank",
            help="Ranking in the last fortnight period",
            format="%d"
        )
    }
    
    st.dataframe(
        display_leaderboard,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    st.markdown("---")
    
    # Additional insights (use original leaderboard for sorting by numeric engagement)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🥇 Top 5 by Engagement")
        top_5_orig = leaderboard.head(5)[['Rank', 'Page/Profile/Channel', 'Engagement', 'Day Won']].copy()
        # Format engagement for display
        top_5_display = top_5_orig.copy()
        top_5_display['Engagement'] = top_5_orig['Engagement'].apply(
            lambda x: format_engagement(x) if pd.notna(x) else "0.00M"
        )
        st.dataframe(top_5_display, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Most Days Won")
        most_days_orig = leaderboard.nlargest(5, 'Day Won')[['Rank', 'Page/Profile/Channel', 'Day Won', 'Engagement']].copy()
        # Format engagement for display
        most_days_display = most_days_orig.copy()
        most_days_display['Engagement'] = most_days_orig['Engagement'].apply(
            lambda x: format_engagement(x) if pd.notna(x) else "0.00M"
        )
        st.dataframe(most_days_display, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Export options
    st.markdown("### 💾 Export Results")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        # Excel export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            leaderboard.to_excel(writer, index=False, sheet_name='Dashboard')
        
        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name="performance_dashboard.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        # CSV export
        csv = leaderboard.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="performance_dashboard.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col4:
        if st.button("🔄 Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
