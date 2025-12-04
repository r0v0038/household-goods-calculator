# Tariff/Tax System Update - December 2025

## Summary of Changes

The household goods calculator has been updated with **legally accurate and current state sales tax rates** as of December 2025.

## What Was Fixed

### 1. **Removed Unconstitutional Interstate Tariffs** ❌➡️✅

**BEFORE:**
- System charged a 3% "interstate commerce fee" on cross-state moves
- This is **unconstitutional** under the U.S. Commerce Clause
- Configuration had `enable_interstate_tariffs: true`

**AFTER:**
- Removed all interstate commerce fees (set to 0%)
- Disabled interstate tariff system permanently
- Added clarifying notes in documentation about unconstitutionality

### 2. **Updated State Sales Tax Rates** 📊

**BEFORE:**
- Only 6 states configured (CA, NY, TX, FL, IL, WA)
- Rates may have been outdated

**AFTER:**
- **All 50 states + Washington DC** now configured
- Updated to December 2025 current rates
- Tax-exempt states properly noted (AK, DE, MT, NH, OR)
- Added documentation notes about local taxes

### 3. **Fixed International Tariff Rates** 🌍

**BEFORE:**
- US-Canada: 15% tariff
- US-Mexico: 12% tariff

**AFTER:**
- All set to 0% (USMCA provides duty-free household goods movement)
- Added note: "Commercial tariffs do not apply to personal household goods moves"
- Customs fees and broker fees may still apply (not calculated here)

### 4. **Fixed Tax Calculation Logic** 🔧

**ISSUE:**
- The code wrapped ALL tax calculations in an `if enable_interstate_tariffs` check
- When interstate tariffs were disabled, legitimate state sales taxes also stopped applying

**FIX:**
- Refactored `cost_engine.py` to always apply state sales taxes
- State sales taxes now apply regardless of interstate tariff setting
- Added backward-compatible field names for API consumers

## Current State Sales Tax Rates (December 2025)

### Highest Tax States
- **Tennessee (TN)**: 7.00%
- **Mississippi (MS)**: 7.00%
- **California (CA)**: 7.25%
- **Indiana (IN)**: 7.00%
- **Rhode Island (RI)**: 7.00%

### Lowest Tax States (Non-Zero)
- **Colorado (CO)**: 2.90%
- **New York (NY)**: 4.00%
- **Alabama (AL)**: 4.00%
- **Georgia (GA)**: 4.00%
- **Hawaii (HI)**: 4.00%

### Tax-Exempt States (0%)
- Alaska (AK)
- Delaware (DE)
- Montana (MT)
- New Hampshire (NH)
- Oregon (OR)

## Files Updated

1. **`data/household_goods_matrix.json`**
   - Disabled interstate tariffs
   - Added all 50 states + DC with current tax rates
   - Set international tariffs to 0%
   - Added explanatory notes

2. **`calculator/cost_engine.py`**
   - Removed interstate tariff calculation logic
   - Fixed state tax application to always run
   - Added new field names (`state_sales_tax`, `total_sales_tax`)
   - Kept legacy fields for backward compatibility

3. **`TARIFF_DOCUMENTATION.md`**
   - Updated all examples and descriptions
   - Removed references to unconstitutional interstate fees
   - Added comprehensive state tax rate table
   - Clarified legal compliance

4. **`test_tariffs.py`**
   - Renamed to reflect sales tax (not tariffs)
   - Updated all output labels and descriptions
   - Removed emoji characters (Windows encoding issues)
   - Added December 2025 update notes

## Testing Results

✅ All calculations working correctly:

### Example: TX → CA (Interstate)
- **Subtotal**: $24,656.94
- **CA Sales Tax (7.25%)**: $1,787.63
- **Final Total**: $26,474.57

### Example: TX → TX (Intrastate)
- **Subtotal**: $10,849.55
- **TX Sales Tax (6.25%)**: $678.10
- **Final Total**: $11,557.64

### Example: NY → FL (Interstate)
- **Subtotal**: $34,513.25
- **FL Sales Tax (6.0%)**: $2,070.79
- **Final Total**: $36,624.04

## Legal Compliance ✅

### What's Legal
- ✅ State sales tax on moving services (varies 0%-7.25%)
- ✅ Based on destination state
- ✅ USMCA duty-free household goods (US/Canada/Mexico)

### What's NOT Legal (and removed)
- ❌ Interstate commerce fees/tariffs (Commerce Clause violation)
- ❌ Commercial tariffs on personal household goods

## API Changes (Backward Compatible)

### New Fields (Recommended)
- `state_sales_tax`: State-specific sales tax amount
- `total_sales_tax`: Total sales tax (currently same as state_sales_tax)
- `move_type`: "interstate" or "intrastate"
- `move_description`: Human-readable move type

### Legacy Fields (Still Available)
- `tariff_type`: Same as `move_type`
- `tariff_description`: Same as `move_description`
- `interstate_tariff`: Always 0.0 now
- `state_tax`: Same as `state_sales_tax`
- `total_tariffs_and_taxes`: Same as `total_sales_tax`

## How to Test

Run the demonstration script:
```bash
cd household-goods-calculator
python test_tariffs.py
```

Run the full test suite:
```bash
python -m pytest tests/ -v
```

## Notes for Users

1. **Rates are BASE state rates** - Local city/county taxes may increase the total but are not included in this calculator

2. **Tax-exempt states** - If moving to AK, DE, MT, NH, or OR, no sales tax will be applied

3. **Annual updates recommended** - State tax rates change periodically; update the `household_goods_matrix.json` file annually

4. **International moves** - For moves to/from Canada or Mexico, customs fees and broker fees may apply separately (not calculated here)

## Configuration Location

All tax rates are configured in:
```
household-goods-calculator/data/household_goods_matrix.json
```

Look for the `tariffs.state_specific_taxes` section.

---

**Updated by:** Batman (code-puppy) 🐶  
**Date:** December 1, 2025  
**Status:** ✅ Legally compliant and current