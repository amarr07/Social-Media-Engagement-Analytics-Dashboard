# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue: `streamlit: command not found`
**Solution:**
```bash
pip install streamlit
# or
python -m pip install streamlit
```

#### Issue: `ModuleNotFoundError: No module named 'openpyxl'`
**Solution:**
```bash
pip install openpyxl xlrd
```

#### Issue: Package installation fails
**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Install packages one by one
pip install streamlit
pip install pandas
pip install openpyxl
pip install xlrd
```

### File Upload Issues

#### Issue: "Error loading file"
**Possible Causes:**
- File is corrupted
- File is not .xlsx or .xls format
- File has password protection

**Solution:**
1. Open file in Excel and save as new .xlsx file
2. Remove any password protection
3. Ensure no merged cells or complex formatting

#### Issue: "Unsupported file type"
**Solution:**
- Only .xlsx and .xls files are supported
- Convert .csv files to .xlsx using Excel

### Column Mapping Issues

#### Issue: Columns not auto-detected
**Solution:**
- Use manual dropdown selection
- Check column names in your file
- Ensure first row contains headers

#### Issue: "Please map all required fields"
**Solution:**
- Ensure all dropdowns have a selection (not blank)
- Each required field must be mapped to a column

#### Issue: Wrong column auto-detected
**Solution:**
- Simply select the correct column from dropdown
- Auto-detection is a suggestion, not mandatory

### Data Processing Issues

#### Issue: Engagement scores are 0 or incorrect
**Possible Causes:**
- Likes, comments, or shares columns contain non-numeric data
- Columns mapped incorrectly

**Solution:**
1. Check your data has numbers in likes/comments/shares columns
2. Remove any text or special characters from numeric columns
3. Verify column mapping is correct

#### Issue: Dates not parsing correctly
**Possible Causes:**
- Date column contains text or unusual format
- Mixed date formats in same column

**Solution:**
1. Ensure dates are in standard format (YYYY-MM-DD or Excel date format)
2. Remove any text from date column
3. Use Excel to format dates consistently

#### Issue: "Days Won" all showing 0
**Possible Causes:**
- Date column not mapped correctly
- Dates are all the same

**Solution:**
1. Verify date column mapping
2. Check that you have posts on multiple different dates
3. Ensure date format is correct

### Comparison Issues

#### Issue: % Change shows 0% for all pages
**Possible Causes:**
- Previous period data doesn't match current data
- Page names don't match exactly
- Previous data has 0 values

**Solution:**
1. Ensure page names are identical across files (case-sensitive)
2. Check previous period data has valid numeric values
3. Verify page names don't have extra spaces

#### Issue: Some pages missing from results
**Possible Causes:**
- Page name spelling differs between files
- Extra spaces in page names

**Solution:**
1. Copy page names from File 1 to Files 2 and 3
2. Use TRIM() function in Excel to remove extra spaces
3. Check for typos in page names

### Display Issues

#### Issue: Dashboard not showing after clicking "Generate Dashboard"
**Possible Causes:**
- Error in data processing
- Missing required data

**Solution:**
1. Check browser console for errors (F12)
2. Look for error messages in the app
3. Try "Start Over" and re-upload files

#### Issue: Percentages showing very large numbers
**Possible Causes:**
- Previous period data is very small or 0
- Data mismatch

**Solution:**
- This is mathematically correct if previous values were very small
- Review your previous period data for accuracy

### Performance Issues

#### Issue: App is slow or freezing
**Possible Causes:**
- Very large datasets
- System resource constraints

**Solution:**
1. Try with smaller date range
2. Close other applications
3. Install watchdog module:
   ```bash
   pip install watchdog
   ```

#### Issue: Upload taking too long
**Possible Causes:**
- Very large Excel files
- Complex Excel formatting

**Solution:**
1. Remove unnecessary columns before upload
2. Save Excel file without formatting (Save As → Excel Workbook)
3. Split large datasets into smaller date ranges

### Export Issues

#### Issue: Download button not working
**Solution:**
1. Try different browser (Chrome recommended)
2. Check browser download settings
3. Ensure pop-ups are allowed for localhost

#### Issue: Downloaded file is empty
**Solution:**
1. Go back and regenerate dashboard
2. Ensure leaderboard is displaying data
3. Try CSV export instead of Excel

## Browser Compatibility

**Recommended Browsers:**
- ✅ Google Chrome (best performance)
- ✅ Mozilla Firefox
- ✅ Microsoft Edge
- ⚠️ Safari (may have issues with downloads)

## Data Validation Checklist

Before uploading, ensure:

**Performance Data (File 1):**
- [ ] Has headers in first row
- [ ] Page names column exists
- [ ] Date column has valid dates
- [ ] Likes column has numbers
- [ ] Comments column has numbers
- [ ] Shares column has numbers
- [ ] No merged cells
- [ ] No password protection

**Previous Period Data (File 2):**
- [ ] Has headers in first row
- [ ] Page names match File 1 exactly
- [ ] Posts column has numbers
- [ ] Engagement column has numbers
- [ ] No merged cells

**Follower Data (File 3):**
- [ ] Has headers in first row
- [ ] Page names match File 1 exactly
- [ ] Followers column has numbers
- [ ] No merged cells

## Getting Help

1. **Check Error Messages**: Read the red error boxes carefully
2. **Review Example Files**: Compare your files to exampleupload*.xlsx
3. **Preview Your Data**: Use the preview function to verify uploads
4. **Start Fresh**: Use "Start Over" button to reset
5. **Check Console**: Press F12 in browser to see detailed errors

## Data Preparation Tips

### In Excel Before Upload:

1. **Clean Column Names:**
   - Remove special characters
   - Use simple names like "Likes", "Comments", "Shares"

2. **Format Numbers:**
   - Select numeric columns
   - Format → Number
   - Remove decimal places if not needed

3. **Format Dates:**
   - Select date column
   - Format → Short Date

4. **Remove Extras:**
   - Delete empty rows at top
   - Delete unused columns
   - Remove merged cells
   - Clear all formatting (optional)

5. **Verify Page Names:**
   - Copy column from File 1
   - Paste into Files 2 and 3
   - Ensures exact matches

## Still Having Issues?

1. Create minimal test data (5-10 rows)
2. Use example files to verify app works
3. Compare your data structure to examples
4. Ensure Python 3.8+ is installed
5. Update all packages: `pip install --upgrade streamlit pandas openpyxl`

## Debug Mode

To see detailed error information, run with:
```bash
streamlit run app.py --logger.level=debug
```

## Contact Information

For technical support:
- Review README.md for detailed documentation
- Check instruction.md for specifications
- Examine example files for proper format

---

**Most common fix: Ensure page names match EXACTLY across all three files!**
