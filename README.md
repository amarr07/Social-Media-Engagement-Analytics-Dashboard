# Social Media Engagement Analytics Dashboard

A comprehensive Streamlit application for analyzing social media engagement across multiple pages/profiles/channels.

## Features

✨ **Engagement Calculation**: Automatically calculates engagement using the formula: `Engagement = 1×Likes + 2×Comments + 3×Shares`

📊 **Day-wise Analysis**: Aggregates data by day and identifies daily winners

🏆 **Leaderboard Rankings**: Ranks pages by total engagement with comprehensive metrics

📈 **Comparison Analytics**: Calculates percentage changes in posts and engagement vs. previous period

👥 **Follower Integration**: Displays follower counts alongside performance metrics

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

The dashboard will open in your default web browser.

### 2. Upload Files

Upload three Excel files (.xlsx or .xls):

**File 1: Performance Data** (Current Period)
- Required columns: Page/Profile Name, Post ID, Date, Likes, Comments, Shares
- Each row represents one post

**File 2: Previous Period Data** (For Comparison)
- Required columns: Page/Profile Name, Total Posts, Total Engagement
- Aggregated data from previous period

**File 3: Follower Data**
- Required columns: Page/Profile Name, Followers Count
- Current follower counts for each page

### 3. Map Columns

The app will guide you through mapping your data columns to the required fields:
- Auto-detection attempts to identify columns automatically
- Manual selection available via dropdown menus
- Preview your data before proceeding

### 4. View Dashboard

The interactive dashboard displays:
- **Summary Metrics**: Total pages, posts, and engagement
- **Leaderboard Table**: Ranked list with all metrics
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

### Previous Period Data (File 2)
| Column | Description | Example |
|--------|-------------|---------|
| Page Name | Name of page/profile/channel | "Tech News Daily" |
| Total Posts | Number of posts in previous period | 45 |
| Total Engagement | Total engagement in previous period | 5000 |

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

1. **Rank**: Position based on total engagement (1 = highest)
2. **Page/Profile/Channel**: Name of the page
3. **Followers**: Current follower count
4. **Total Posts**: Number of posts in current period
5. **Total Engagement**: Sum of engagement scores for all posts
6. **Days Won**: Number of days this page had highest engagement
7. **% Change Posts**: Percentage change in posts vs. previous period
8. **% Change Engagement**: Percentage change in engagement vs. previous period

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
