# Quick Start Guide

## 🚀 Running the Application

1. **Open Terminal** in the project directory

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to: http://localhost:8501

## 📝 Step-by-Step Workflow

### Step 1: Upload Files
1. Click on "Performance File" and upload `exampleupload1.xlsx` (or your data)
2. Click on "Previous Period File" and upload `exampleupload2.xlsx` (or your data)
3. Click on "Follower File" and upload `exampleupload3.xlsx` (or your data)
4. Click "Next: Map Columns"

### Step 2: Map Columns
The app will try to auto-detect your columns. Verify or adjust the mappings:

**Performance Data:**
- Page/Profile/Channel Name → Select the column with page names
- Post ID/Name → Select the column with post identifiers
- Post Date → Select the column with dates
- Likes → Select the column with like counts
- Comments → Select the column with comment counts
- Shares → Select the column with share counts

**Previous Period Data:**
- Page/Profile/Channel Name → Select the column with page names
- Total Posts → Select the column with post counts
- Total Engagement → Select the column with engagement scores

**Follower Data:**
- Page/Profile/Channel Name → Select the column with page names
- Followers Count → Select the column with follower numbers

Click "Generate Dashboard"

### Step 3: View Results
- Review the summary metrics
- Explore the leaderboard table
- Check top performers
- Download results (Excel or CSV)

## 🎯 Key Features to Explore

1. **Summary Metrics** - Get overview of total pages, posts, and engagement
2. **Interactive Table** - Sort and filter the leaderboard
3. **Top Performers** - See top 5 pages by engagement
4. **Days Won** - Find pages with most daily victories
5. **Export** - Download your analysis results

## 💡 Tips

- Column names don't need to match exactly - the app maps them for you
- Auto-detection works best with common column names
- Preview your data before mapping to verify it loaded correctly
- Use "Start Over" button to analyze different datasets

## 🔍 What Gets Calculated

For each post:
```
Engagement = (1 × Likes) + (2 × Comments) + (3 × Shares)
```

Daily aggregation:
- Posts are grouped by page and date
- Engagement is summed per day
- Highest engagement page wins that day

Final rankings:
- Pages ranked by total engagement
- Comparison metrics calculated vs. previous period
- All data combined into comprehensive leaderboard

## 📊 Example Data

Use the included example files to test:
- `exampleupload1.xlsx` - Performance data
- `exampleupload2.xlsx` - Previous period data  
- `exampleupload3.xlsx` - Follower data

## ❓ Need Help?

Check `README.md` for detailed documentation or `instruction.md` for technical specifications.

---

**Ready to analyze your social media engagement? Run the app now!** 🎉
