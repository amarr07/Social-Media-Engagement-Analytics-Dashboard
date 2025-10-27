# Social Media Performance Dashboard

A comprehensive single-page Streamlit application for analyzing social media engagement across multiple pages/profiles/channels.

## Features

✨ **Engagement Calculation**: Automatically calculates engagement using the formula: `Engagement = 1×Likes + 2×Comments + 3×Shares`

📊 **Day-wise Analysis**: Aggregates data by day and identifies daily winners

🏆 **Leaderboard Rankings**: Ranks pages by total engagement with comprehensive metrics

📈 **Comparison Analytics**: Calculates percentage changes vs. last fortnight performance

👥 **Follower Integration**: Displays follower counts alongside performance metrics

📋 **Interactive Dashboard**: Single-page interface with sidebar uploads and tooltips

💾 **Export Options**: Download results as Excel or CSV

## Installation

1. Ensure Python 3.8+ is installed on your system

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
/project-root
├── app.py              # Main Streamlit interface
├── analytics.py        # Engagement, ranking, and reporting functions
├── utils.py            # Helper functions (file detection, mapping)
├── requirements.txt    # Python dependencies
├── /static            # Static files and visuals
├── /data              # Uploaded or demo files
├── exampleupload1.xlsx # Example performance data
├── exampleupload2.xlsx # Example previous period data
└── exampleupload3.xlsx # Example follower data
```

## Usage

### 1. Launch the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at http://localhost:8501

### 2. Upload Files (via Sidebar)

The sidebar contains three upload sections. Upload Excel files (.xlsx or .xls):

**File 1: Daily Post Performance** (Current Period)
- Required columns: Page/Profile/Channel Name, Post ID, Date, Likes, Comments, Shares
- Each row represents one post

**File 2: Last Fortnight Performance** (For Comparison)
- Required columns: Page/Profile/Channel Name, Engagement, Post Count, Day Won, Rank
- Aggregated data from last fortnight period

**File 3: Follower Counts**
- Required columns: Page/Profile/Channel Name, Follower Count
- Current follower counts for each page

### 3. Map Columns

Click "Map Columns & Generate Dashboard" button in the sidebar.

The app will guide you through mapping your data columns to the required fields:
- Auto-detection attempts to identify columns automatically
- Manual selection available via dropdown menus for each field
- Preview your data before proceeding

### 4. View Dashboard

The interactive single-page dashboard displays:
- **Summary Metrics**: Total pages, posts, and engagement
- **Leaderboard Table**: Ranked list with all metrics and tooltips
- **Top Performers**: Top 5 pages by engagement
- **Most Days Won**: Pages with most daily victories
- **Export Options**: Download results as Excel or CSV

## Data Requirements

### Performance Data (File 1)
| Column | Description | Example |
|--------|-------------|---------|
| Page Name | Name of page/profile/channel | "Tech News Daily" |
| Post ID | Unique post identifier | "POST_001" |
| Date | Post publication date | "2024-01-15" |
| Likes | Number of likes | 150 |
| Comments | Number of comments | 25 |
| Shares | Number of shares | 10 |

### Last Fortnight Data (File 2)
| Column | Description | Example |
|--------|-------------|---------|
| Page Name | Name of page/profile/channel | "Tech News Daily" |
| Engagement | Total engagement from last fortnight | 5000 |
| Post Count | Number of posts in last fortnight | 45 |
| Day Won | Days won in last fortnight | 3 |
| Rank | Rank in last fortnight | 2 |

### Follower Data (File 3)
| Column | Description | Example |
|--------|-------------|---------|
| Page Name | Name of page/profile/channel | "Tech News Daily" |
| Followers | Current follower count | 15000 |

## Engagement Formula

```
Engagement = (1 × Likes) + (2 × Comments) + (3 × Shares)
```

This weighted formula prioritizes:
- **Shares** (weight: 3) - Highest value, indicates strong engagement
- **Comments** (weight: 2) - Medium value, indicates conversation
- **Likes** (weight: 1) - Base value, indicates acknowledgment

## Output Metrics

The dashboard calculates and displays:

1. **Follower**: Current follower count (with tooltip)
2. **Page/Profile/Channel**: Name of the page (with tooltip)
3. **Post**: Number of posts in current period (with tooltip)
4. **Engagement**: Sum of engagement scores for all posts (with tooltip)
5. **Rank**: Current ranking based on total engagement (1 = highest) (with tooltip)
6. **Day Won**: Number of days this page had the highest engagement (with tooltip)
7. **% Change in Post**: Percentage change in posts vs. last fortnight (with tooltip)
8. **% Change in Engagement**: Percentage change in engagement vs. last fortnight (with tooltip)
9. **Last Fortnight Day Won**: Days won in the last fortnight period (with tooltip)
10. **Last Fortnight Rank**: Ranking in the last fortnight period (with tooltip)

## Day-wise Winner Logic

For each day:
1. All posts are aggregated by page and date
2. Engagement is summed for each page on that date
3. The page with highest engagement wins that day
4. Winner gets +1 to their "Days Won" count

## Tips for Best Results

- Ensure date columns are properly formatted (YYYY-MM-DD or Excel date format)
- Use consistent page/profile names across all three files
- Numeric columns (likes, comments, shares) should contain only numbers
- Remove any header rows beyond the first row
- Check for and remove any merged cells in Excel files

## Troubleshooting

**Issue**: "Error loading file"
- **Solution**: Ensure file is .xlsx or .xls format, not corrupted

**Issue**: Columns not auto-detected
- **Solution**: Manually select the correct columns from dropdowns

**Issue**: Missing data in results
- **Solution**: Verify page names match exactly across all three files

**Issue**: Percentage changes show as 0%
- **Solution**: Ensure previous period data contains valid numeric values

## Example Files

The repository includes three example files:
- `exampleupload1.xlsx`: Sample performance data
- `exampleupload2.xlsx`: Sample previous period data
- `exampleupload3.xlsx`: Sample follower data

Use these to test the application and understand the required format.

## Support

For issues or questions:
1. Check that all required packages are installed
2. Verify Python version is 3.8 or higher
3. Ensure all three files are uploaded before mapping columns
4. Review the instruction.md file for detailed specifications

## License

This project is for internal use and analysis purposes.
