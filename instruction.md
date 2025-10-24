Project Instructions: Social Media Engagement Analytics Agent
Folder Structure
text
/project-root
    |-- app.py             # Main Streamlit interface
    |-- analytics.py       # Engagement, ranking, and reporting functions
    |-- utils.py           # Helper functions (file type detection, mapping)
    |-- requirements.txt   # Python package list for reference (optional)
    |-- /static            # For any static files, visuals, or preview images
    |-- /data              # Save uploaded or demo files (optional)
Required Setup
Python 3.8+ (recommended version; must be installed on your system)

Streamlit and pandas libraries—ensure these are available via pip install streamlit pandas for code to run.

No additional system installation steps—just ensure your Python is ready with pandas and streamlit.​

Step-by-Step Detailed Instructions
1. Launching the Streamlit Dashboard

Run app.py with streamlit run app.py

2. Uploading the Performance Data

The dashboard will prompt you to upload three files:

Performance File #1 – must be an Excel file (.xlsx or .xls) containing columns: page/profile/channel name, post id/name, post date, like, comment, share.

Each row = one post, columns as described.

Last Time Comparison File #2 – another Excel which has page/profile/channel name with corresponding aggregate post and engagement values for earlier period.

Follower Data File #3 – Excel file listing page/profile/channel name and latest follower count.​

3. Data Mapping & Validation

After upload, the app lists columns for mapping: user selects which column maps to "Page Name", "Post Name/ID", "Like", "Comment", "Share", "Date" for performance.

For each upload, if columns are mismatched or ambiguous, the app preview will let you select which corresponds to which.​

4. Engagement Calculation

Engagement for every post is computed as:

Engagement
=
1
×
Like
+
2
×
Comment
+
3
×
Share
Engagement=1×Like+2×Comment+3×Share

This formula is applied to each row (i.e., each post).​

5. Daywise Winner Logic

The app aggregates by page/profile/channel and date, summing engagement for each combination.​

The page/profile/channel with the highest engagement that day gets "day won" = 1; all others are 0 for that date.

6. Aggregation and Ranking

The final leaderboard dashboard displays per page/profile/channel:

Follower count (from 3rd file)

Number of Posts (sum for period from file 1)

Total Engagement (sum over all posts in day range)

Rank (by descending Engagement)

Day Won (sum for period)

% Change in Posts (vs file 2's period)

% Change in Engagement (vs file 2)

% changes are calculated as:

Current
−
Previous
Previous
×
100
Previous
Current−Previous
 ×100

for both Posts and Engagement.

7. Interactive Dashboard Display

All metrics above shown in an interactive table in Streamlit.

Page/profile/channel name column should always be visible and sorted by Rank.

Data should be visually styled with Streamlit's built-in or minimal custom options for clarity and an upscale look.​​

Allow download/export of result for manual checks.

Recommendations for Copilot/Agent
Always prompt user for data column mapping before calculation, if ambiguity exists.

Add validations for file format and required columns after upload.

For all calculations (engagement, aggregation, change), use pandas—avoid manual looping and keep formulas explicit and visible in code.

Store uploaded dataframes in session state for easy stepwise interaction.

For anything unclear (column mapping, missing columns), show the preview and request user selection.

Keep interface simple: a three-step sidebar or three-page flow:

Upload all files and map columns

Preview per-post engagement, by day

Leaderboard dashboard and export