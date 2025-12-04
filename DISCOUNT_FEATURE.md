# Discount Feature

## Overview
A discount feature has been added to the Household Goods Calculator that allows users to apply a percentage discount to the total cost, excluding fuel surcharge and tariffs.

## How It Works

### Calculation Flow
1. **Base Cost Calculation**: Material + Transportation + Services (Packing/Storage) + Regional Adjustment + Insurance
2. **Discount Applied**: Percentage discount is subtracted from the base cost
3. **Fuel Surcharge**: Calculated on the ORIGINAL base cost (pre-discount)
4. **Tariffs & Taxes**: Calculated on the discounted subtotal (after discount is applied)

### Formula
```
Subtotal Before Discount = Regional Cost + Insurance
Discount Amount = Subtotal Before Discount × Discount Rate
Subtotal After Discount = Subtotal Before Discount - Discount Amount
Fuel Charge = Subtotal Before Discount × Fuel Surcharge Rate (calculated on pre-discount amount)
Tariffs = (Subtotal After Discount + Fuel Charge) × Tariff Rate
Total Cost = Subtotal After Discount + Fuel Charge + Tariffs
```

## Features

### Frontend
- **Discount Input**: Added to Advanced Settings in both Single Calculator and Bulk Upload pages
- **Range**: 0% to 50% in 0.5% increments
- **Default**: 0% (no discount)
- **Display**: Shows discount amount and subtotal after discount in breakdown

### Discount Section in Breakdown
When a discount is applied, a new section appears in the detailed cost breakdown:
- **Discount Rate**: Shows the percentage applied
- **Discount Amount**: Shows the dollar amount saved
- **Subtotal After Discount**: Shows the cost after discount is applied
- **Green Highlighting**: Makes the discount visually prominent

## Files Modified

### Frontend
- `templates/index.html` - Added discount input field
- `templates/bulk.html` - Added discount input field  
- `static/calculator.js` - Added discount data collection and breakdown display
- `static/bulk.js` - Added discount to custom rates sent to backend

### Backend
- `calculator/cost_engine.py` - Added discount calculation logic
  - New variable: `discount_rate` from custom_rates
  - New variable: `discount_amount` calculated as base cost × discount rate
  - New variable: `subtotal_after_discount` after discount is applied
  - Updated: `subtotal` calculation to include discounted amount
  - Updated: breakdown return dictionary with discount fields

## Usage

### Single Calculator
1. Open "Advanced Rate Settings"
2. Find the "Discount (%)" field
3. Enter the desired discount percentage (e.g., 10 for 10% off)
4. Click "Calculate Should Cost"
5. See the discount breakdown in the detailed results

### Bulk Upload
1. Open "Advanced Rate Settings"
2. Find the "Discount (%)" field
3. Enter the desired discount percentage
4. Upload and process your Excel file
5. Discount will be applied to all calculations in the batch

## Discount Behavior

### What's Included in Discount
✅ Material Costs
✅ Transportation Costs
✅ Packing Service Charges
✅ Storage Option Charges
✅ Regional Adjustments
✅ Insurance

### What's Excluded from Discount
❌ Fuel Surcharge (calculated on pre-discount amount, then added after)
❌ Tariffs & Taxes (calculated as % of final subtotal, so reduced when base is discounted)

## Examples

### Example 1: 10% Discount
- Base Cost: $1,000
- Discount (10%): -$100
- Subtotal After Discount: $900
- Fuel Surcharge (calculated on $1,000): +$100
- Tariffs (calculated on $900 + $100): +$80
- **Total: $1,080** (compared to $1,180 without discount)
- **Savings: $100**

### Example 2: 0% Discount (Default)
- All costs are calculated normally
- Discount amount is $0
- Total matches original calculation

## Reset to Defaults
Click "Reset to Defaults" button to:
- Set discount back to 0%
- Reset all other advanced settings to their default values

## API

When sending calculation requests to the backend, include discount in custom_rates:
```json
{
  "origin": "Bentonville, AR",
  "destination": "Austin, TX",
  "distance_miles": 500,
  "weight": 5000,
  "custom_rates": {
    "discount": 0.10
  }
}
```

## Testing

Run the test file to verify discount functionality:
```bash
python test_discount.py
```

The test:
- Calculates costs with and without discount
- Verifies fuel charges are identical (pre-discount)
- Verifies tariffs change appropriately
- Shows total savings from discount