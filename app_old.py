"""
Social Media Engagement Analytics Dashboard
Main Streamlit application
"""
import streamlit as st
import pandas as pd
from io import BytesIO
import utils
import analytics


# Page configuration
st.set_page_config(
    page_title="Social Media Engagement Analytics",
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
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'step' not in st.session_state:
        st.session_state.step = 1
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
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = None


def upload_files_step():
    """Step 1: Upload all three files"""
    st.markdown('<p class="main-header">📊 Social Media Engagement Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your performance data files to get started</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📁 File 1: Performance Data")
        st.info("Upload current period performance data with page names, post details, dates, likes, comments, and shares.")
        performance_file = st.file_uploader(
            "Performance File",
            type=['xlsx', 'xls'],
            key='performance_upload',
            help="Excel file with post-level performance data"
        )
        
        if performance_file:
            df = utils.load_excel_file(performance_file)
            if df is not None:
                st.session_state.performance_df = df
                st.success(f"✅ Loaded {len(df)} rows")
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10))
    
    with col2:
        st.markdown("### 📁 File 2: Previous Period Data")
        st.info("Upload previous period data with page names, total posts, and total engagement for comparison.")
        previous_file = st.file_uploader(
            "Previous Period File",
            type=['xlsx', 'xls'],
            key='previous_upload',
            help="Excel file with aggregated previous period data"
        )
        
        if previous_file:
            df = utils.load_excel_file(previous_file)
            if df is not None:
                st.session_state.previous_df = df
                st.success(f"✅ Loaded {len(df)} rows")
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10))
    
    with col3:
        st.markdown("### 📁 File 3: Follower Data")
        st.info("Upload follower data with page names and current follower counts.")
        follower_file = st.file_uploader(
            "Follower File",
            type=['xlsx', 'xls'],
            key='follower_upload',
            help="Excel file with follower information"
        )
        
        if follower_file:
            df = utils.load_excel_file(follower_file)
            if df is not None:
                st.session_state.follower_df = df
                st.success(f"✅ Loaded {len(df)} rows")
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10))
    
    st.markdown("---")
    
    # Check if all files are uploaded
    if (st.session_state.performance_df is not None and 
        st.session_state.previous_df is not None and 
        st.session_state.follower_df is not None):
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✨ Next: Map Columns", type="primary", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
    else:
        st.warning("⚠️ Please upload all three files to continue.")


def map_columns_step():
    """Step 2: Map columns for all three files"""
    st.markdown('<p class="main-header">🔗 Column Mapping</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Map your data columns to the required fields</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Performance file mapping
    st.markdown("### 📊 Performance Data Mapping")
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
        "Performance Data",
        performance_fields
    )
    
    st.markdown("---")
    
    # Previous period mapping
    st.markdown("### 📅 Previous Period Data Mapping")
    previous_fields = {
        'page_name': 'Page/Profile/Channel Name',
        'posts': 'Total Posts',
        'engagement': 'Total Engagement'
    }
    
    previous_mapping = utils.create_column_mapping_ui(
        st.session_state.previous_df,
        "Previous Period",
        previous_fields
    )
    
    st.markdown("---")
    
    # Follower data mapping
    st.markdown("### 👥 Follower Data Mapping")
    follower_fields = {
        'page_name': 'Page/Profile/Channel Name',
        'followers': 'Followers Count'
    }
    
    follower_mapping = utils.create_column_mapping_ui(
        st.session_state.follower_df,
        "Follower Data",
        follower_fields
    )
    
    st.markdown("---")
    
    # Validate and proceed
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    with col3:
        # Validate all mappings
        perf_valid, perf_empty = utils.validate_mapping(performance_mapping)
        prev_valid, prev_empty = utils.validate_mapping(previous_mapping)
        foll_valid, foll_empty = utils.validate_mapping(follower_mapping)
        
        if perf_valid and prev_valid and foll_valid:
            if st.button("🚀 Generate Dashboard", type="primary", use_container_width=True):
                # Store mappings
                st.session_state.performance_mapping = performance_mapping
                st.session_state.previous_mapping = previous_mapping
                st.session_state.follower_mapping = follower_mapping
                
                # Generate leaderboard
                with st.spinner("Calculating engagement metrics..."):
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
                            previous_posts_col=previous_mapping['posts'],
                            previous_engagement_col=previous_mapping['engagement']
                        )
                        
                        st.session_state.leaderboard = leaderboard
                        st.session_state.step = 3
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating dashboard: {str(e)}")
                        st.exception(e)
        else:
            st.button("🚀 Generate Dashboard", disabled=True, use_container_width=True)
            error_msgs = []
            if not perf_valid:
                error_msgs.append(f"Performance: {', '.join(perf_empty)}")
            if not prev_valid:
                error_msgs.append(f"Previous: {', '.join(prev_empty)}")
            if not foll_valid:
                error_msgs.append(f"Follower: {', '.join(foll_empty)}")
            st.error(f"⚠️ Please map all required fields: {'; '.join(error_msgs)}")


def dashboard_step():
    """Step 3: Display interactive dashboard"""
    st.markdown('<p class="main-header">🏆 Engagement Leaderboard Dashboard</p>', unsafe_allow_html=True)
    
    if st.session_state.leaderboard is None:
        st.error("No leaderboard data available. Please go back and generate the dashboard.")
        return
    
    leaderboard = st.session_state.leaderboard
    
    # Summary metrics
    st.markdown("### 📈 Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Pages/Profiles",
            len(leaderboard),
            help="Total number of pages analyzed"
        )
    
    with col2:
        total_posts = leaderboard['Total Posts'].sum()
        st.metric(
            "Total Posts",
            f"{total_posts:,}",
            help="Sum of all posts across all pages"
        )
    
    with col3:
        total_engagement = leaderboard['Total Engagement'].sum()
        st.metric(
            "Total Engagement",
            f"{total_engagement:,.0f}",
            help="Sum of all engagement scores"
        )
    
    with col4:
        avg_engagement = leaderboard['Total Engagement'].mean()
        st.metric(
            "Avg Engagement per Page",
            f"{avg_engagement:,.0f}",
            help="Average engagement score per page"
        )
    
    st.markdown("---")
    
    # Leaderboard table
    st.markdown("### 🏅 Leaderboard Rankings")
    
    # Format the dataframe for display
    display_df = leaderboard.copy()
    
    # Format percentage columns
    display_df['% Change Posts'] = display_df['% Change Posts'].apply(lambda x: f"{x:+.1f}%")
    display_df['% Change Engagement'] = display_df['% Change Engagement'].apply(lambda x: f"{x:+.1f}%")
    
    # Format numeric columns
    display_df['Followers'] = display_df['Followers'].apply(lambda x: f"{x:,}")
    display_df['Total Posts'] = display_df['Total Posts'].apply(lambda x: f"{x:,}")
    display_df['Total Engagement'] = display_df['Total Engagement'].apply(lambda x: f"{x:,.0f}")
    
    # Display with highlighting
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=600
    )
    
    st.markdown("---")
    
    # Top performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🥇 Top 5 by Engagement")
        top_5 = leaderboard.head(5)[['Rank', 'Page/Profile/Channel', 'Total Engagement', 'Days Won']]
        st.dataframe(top_5, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Most Days Won")
        most_days = leaderboard.nlargest(5, 'Days Won')[['Rank', 'Page/Profile/Channel', 'Days Won', 'Total Engagement']]
        st.dataframe(most_days, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Download options
    st.markdown("### 💾 Export Data")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Export to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            leaderboard.to_excel(writer, index=False, sheet_name='Leaderboard')
        
        st.download_button(
            label="📥 Download as Excel",
            data=output.getvalue(),
            file_name="engagement_leaderboard.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        # Export to CSV
        csv = leaderboard.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="engagement_leaderboard.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 Start Over", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def main():
    """Main application flow"""
    initialize_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        st.markdown("---")
        
        # Step indicators
        steps = ["📁 Upload Files", "🔗 Map Columns", "📊 Dashboard"]
        for i, step_name in enumerate(steps, 1):
            if st.session_state.step == i:
                st.markdown(f"**➡️ {step_name}**")
            elif st.session_state.step > i:
                st.markdown(f"✅ {step_name}")
            else:
                st.markdown(f"⭕ {step_name}")
        
        st.markdown("---")
        
        # Instructions
        st.markdown("## ℹ️ Instructions")
        st.markdown("""
        **Step 1: Upload Files**
        - Performance data with post details
        - Previous period comparison data
        - Follower count data
        
        **Step 2: Map Columns**
        - Map your columns to required fields
        - Auto-detection helps speed this up
        
        **Step 3: View Dashboard**
        - Interactive leaderboard
        - Download results
        """)
        
        st.markdown("---")
        st.markdown("### 📐 Engagement Formula")
        st.latex(r"E = 1 \times L + 2 \times C + 3 \times S")
        st.caption("L=Likes, C=Comments, S=Shares")
    
    # Main content based on current step
    if st.session_state.step == 1:
        upload_files_step()
    elif st.session_state.step == 2:
        map_columns_step()
    elif st.session_state.step == 3:
        dashboard_step()


if __name__ == "__main__":
    main()
