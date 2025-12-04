# 📁 Bulk Upload Feature Guide

## Overview

The Bulk Upload feature allows you to calculate should costs for multiple household goods moves simultaneously by uploading an Excel file. This is perfect for:

- Processing large batches of move requests
- Historical data analysis
- What-if scenario planning
- Quarterly reporting

## Quick Start

### 1. Access the Bulk Upload Page

Navigate to: `http://localhost:5000/bulk`

Or click the "📁 Bulk Upload" link in the navigation menu.

### 2. Download the Template

Click the "⬇️ Download Excel Template" button to get a pre-formatted Excel file with:
- Required column headers
- Example data rows
- Detailed instructions
- Valid option values

### 3. Fill in Your Data

Open the template and add your move details:

#### Required Columns

| Column | Description | Example |
|--------|-------------|----------|
| `origin` | Starting location (City, State or ZIP) | `Bentonville, AR` or `72712` |
| `destination` | Ending location (City, State or ZIP) | `Austin, TX` or `78701` |
| `weight` | Total weight in pounds (must be > 0) | `5000` |

#### Optional Columns

| Column | Description | Valid Values | Default |
|--------|-------------|--------------|----------|
| `distance_miles` | Manual distance override | Any positive number | Auto-calculated |
| `packing_service` | Packing service level | `self_pack`, `partial_pack`, `full_pack` | `self_pack` |
| `storage_option` | Storage duration | `no_storage`, `storage_30days`, `storage_60days` | `no_storage` |
| `include_insurance` | Insurance coverage | `TRUE`, `FALSE`, `Yes`, `No` | `TRUE` |

### 4. Upload Your File

Drag and drop your Excel file onto the upload area, or click to browse and select your file.

**File Requirements:**
- Format: `.xlsx` or `.xls`
- Max size: 16MB
- Must include all required columns

### 5. Review Validation Results

The system will automatically validate your file and show:
- ✅ **Success:** File is ready to process
- ⚠️ **Warnings:** Non-critical issues (e.g., missing optional columns)
- ❌ **Errors:** Issues that must be fixed before processing

### 6. Process Calculations

If validation passes, click "🚀 Process Calculations" to begin batch processing.

You'll see:
- Real-time progress indicator
- Processing status updates
- Estimated completion time

### 7. Review Results

After processing, you'll see:

#### Summary Statistics
- Total rows processed
- Successful calculations
- Failed calculations
- Success rate percentage

#### Results Table
For each row:
- Row number from your Excel file
- Status (Success/Failed)
- Origin and destination
- Distance and weight
- **Total should cost**
- "View" button for detailed breakdown

#### Detailed Breakdown
Click "View" on any row to see:
- Route information
- Regional classifications
- Complete cost breakdown
- All applied adjustments and multipliers

### 8. Download Results

Click "⬇️ Download Detailed Excel Report" to get a comprehensive Excel file containing:

**Success Rows:**
- All input data
- Calculated distance (if auto-calculated)
- Total should cost
- Detailed cost breakdown
  - Material cost
  - Transportation cost
  - Packing cost
  - Storage cost
  - Fuel charge
  - Insurance cost
  - Tariffs & taxes
- Regional information
- Service selections

**Failed Rows:**
- Row number
- Error message
- Original input data (for correction)

## Common Use Cases

### Scenario 1: Monthly Move Planning

```excel
origin              | destination      | weight | packing_service | storage_option
Bentonville, AR     | Seattle, WA      | 5000   | full_pack       | no_storage
Austin, TX          | Miami, FL        | 8000   | partial_pack    | storage_30days
New York, NY        | Los Angeles, CA  | 3500   | self_pack       | no_storage
```

### Scenario 2: What-If Analysis

Test different packing/storage combinations for the same route:

```excel
origin          | destination | weight | packing_service | storage_option
Dallas, TX      | Chicago, IL | 6000   | self_pack       | no_storage
Dallas, TX      | Chicago, IL | 6000   | partial_pack    | no_storage
Dallas, TX      | Chicago, IL | 6000   | full_pack       | no_storage
Dallas, TX      | Chicago, IL | 6000   | full_pack       | storage_30days
Dallas, TX      | Chicago, IL | 6000   | full_pack       | storage_60days
```

### Scenario 3: Historical Cost Analysis

Analyze past moves with actual weights and distances:

```excel
origin          | destination    | weight | distance_miles | packing_service
Portland, OR    | Boston, MA     | 4500   | 3050          | partial_pack
Phoenix, AZ     | Denver, CO     | 7200   | 860           | full_pack
Atlanta, GA     | Tampa, FL      | 3200   | 450           | self_pack
```

## Error Handling

### Common Validation Errors

1. **Missing required columns**
   - **Error:** "Missing required columns: weight"
   - **Fix:** Ensure your Excel file has columns named exactly: `origin`, `destination`, `weight`

2. **Empty cells in required columns**
   - **Error:** "Column 'origin' has 2 empty cell(s)"
   - **Fix:** Fill in all required data for every row

3. **Invalid weight values**
   - **Error:** "Found 1 row(s) with invalid weight (must be > 0)"
   - **Fix:** Ensure all weights are positive numbers

### Common Processing Errors

1. **Location not found**
   - **Error:** "Could not calculate distance. Please provide distance manually."
   - **Fix:** Add a `distance_miles` column with manual distance values

2. **Invalid service options**
   - **Error:** "Invalid packing service"
   - **Fix:** Use exact values: `self_pack`, `partial_pack`, or `full_pack`

## Performance Tips

🚀 **Batch Size:** For optimal performance, process up to 100 rows at a time

🔄 **Auto-calculation:** If you have distances, include them to speed up processing (no geocoding needed)

💾 **File Size:** Keep files under 5MB for fastest upload/processing

⏱️ **Processing Time:** Expect ~1-2 seconds per row with auto-distance calculation, ~0.5 seconds with manual distances

## Technical Specifications

### API Endpoints

#### Validate File
```
POST /bulk/validate
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "validation": {
    "valid": true,
    "errors": [],
    "warnings": [],
    "row_count": 25
  }
}
```

#### Process File
```
POST /bulk/process
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "results": [...],
  "errors": [],
  "summary": {
    "total_rows": 25,
    "successful": 24,
    "failed": 1,
    "success_rate": "96.0%"
  }
}
```

#### Download Template
```
GET /bulk/template

Response: Excel file download
```

#### Download Results
```
GET /bulk/download/excel?results={JSON}

Response: Excel file download
```

## Best Practices

✅ **Test with template:** Always start with the downloaded template

✅ **Validate data:** Use Excel data validation to prevent invalid entries

✅ **Consistent formatting:** Keep location formats consistent (all cities or all ZIP codes)

✅ **Backup originals:** Keep a copy of your original data before uploading

✅ **Review errors:** Check failed rows and correct issues before re-uploading

✅ **Use optional columns:** Include `distance_miles` when known to improve accuracy

❌ **Avoid:** Mixed formats, special characters, merged cells, formulas in data cells

## Troubleshooting

### Upload Issues

**Problem:** "Invalid file format"
- **Solution:** Save file as `.xlsx` (Excel 2007+) format

**Problem:** "File too large"
- **Solution:** Split into multiple files or remove unnecessary rows/columns

### Processing Issues

**Problem:** "Many rows failing with distance errors"
- **Solution:** Add `distance_miles` column with pre-calculated distances

**Problem:** "Results don't match single calculator"
- **Solution:** Ensure exact same inputs (check for extra spaces, case differences)

### Download Issues

**Problem:** "No results to download"
- **Solution:** Process a file successfully first before downloading

**Problem:** "Download doesn't start"
- **Solution:** Check browser pop-up blocker settings

## Accessibility Features

♿ **WCAG 2.2 Level AA Compliant:**
- Full keyboard navigation support
- Screen reader friendly
- ARIA labels and live regions
- High contrast mode support
- Focus indicators
- Error announcements

### Keyboard Shortcuts

- `Tab` - Navigate through elements
- `Enter` / `Space` - Activate buttons/upload area
- `Esc` - Close modal dialogs

## Support

For questions, issues, or feature requests related to bulk upload:

1. Check this guide first
2. Review error messages carefully
3. Contact the development team with:
   - Screenshot of error
   - Sample Excel file (anonymized)
   - Steps to reproduce

---

**Built with 🐶 by Batman (code-puppy)**
