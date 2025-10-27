
# Project Instructions: Social Media Performance Dashboard

## Objective  
Build a Streamlit interface in Python to analyze social media post performance by uploading Excel files. Output a dashboard summarizing engagement and performance metrics for all pages/profiles/channels.

## Folder Structure  
```
project_root/
│
├── app.py                # Main Streamlit app
├── utils.py              # Helper functions for processing data
├── requirements.txt      # List only core packages for reference
├── README.md             # Basic overview + dashboard usage
├── assets/               # Static images/CSS (if any UI tweaks/designer additions)
└── uploads/              # Optional temp location for user files
```

## Step-by-Step Workflow

### 1. Launch Streamlit Interface
- Start with a single file, `app.py`, where all logic is laid out clearly.
- Main dashboard should have three upload buttons, each accepting an Excel (xlsx) file using `st.file_uploader`.
    - Upload 1: Daily Post Performance (columns: page/profile/channel name, post name/id, date, like, comment, share)
    - Upload 2: Last Fortnight Performance (columns: page/profile/channel name, engagement, post count, day won, rank)
    - Upload 3: Follower Counts (columns: page/profile/channel name, follower)

### 2. Data Processing / Mapping
1. Load the uploaded Excel using `pandas.read_excel`, engine `openpyxl`.
2. Show a preview with `st.dataframe` so the user can manually map which columns mean like, comment, share, post name/id if column names are ambiguous.
3. Compute engagement for each post:
    - Formula: $$ engagement = 1 \times like + 2 \times comment + 3 \times share $$
    - For ambiguous columns, display mapping dialog and let user pick which is which.
4. Group posts by page/profile/channel and date.
    - For each date, sum engagement for each entity; the one with the highest value is "day won" (mark as 1 for that record, 0 otherwise).
5. For final aggregation:
    - Unique pages/profiles/channels as index.
    - Sum of posts, total engagement, sum of “day won”.

### 3. Add Metrics from Other Uploads
1. After 2nd upload, for each page/channel/profile, compute:
    - % Change in post: $$ \frac{current\_post - last\_fortnight\_post}{last\_fortnight\_post} \times 100 $$
    - % Change in engagement: $$ \frac{current\_engagement - last\_fortnight\_engagement}{last\_fortnight\_engagement} \times 100 $$
    - Add last fortnight’s day won and rank (direct mapping from file).
2. After 3rd upload, merge follower counts with the final report.

### 4. Dashboard Outputs  
- Make the results in an interactive `st.dataframe`/`st.table` with sorting/ranking enabled.
- Display columns:
    - follower
    - page/profile/channel name
    - post (sum by entity)
    - engagement (sum by entity)
    - rank (by engagement descending)
    - day won (sum by entity)
    - % change in post
    - % change in engagement
    - last fortnight day won
    - last fortnight rank
- Use modern Streamlit visuals like badges/ranking icons for a “classy” look. Optionally, use conditional formatting or colored bars for ranking.

### 5. Additional UI Details
- Use Streamlit sidebar for file uploads.
- Add help tooltips for each column header explaining how the metric is calculated.
- Always show error messages clearly (file format, missing columns, incorrect mappings).

### 6. Guidance for Copilot Suggestions  
- Always assume ambiguous column mapping; prompt user visually.
- Avoid unnecessary Flask/Django setups.
- All logic must be Python + Streamlit only.
- Never add external service calls or major side effects.
- Suggestions must cover clean error handling, progress feedback, and null protection.
- UI should remain single-page unless explicitly asked for tabs/views.

