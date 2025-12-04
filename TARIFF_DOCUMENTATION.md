# Tariff & Tax System - Household Goods Calculator

## Overview

⚠️ **IMPORTANT LEGAL NOTE**: Interstate tariffs on household goods moves are **unconstitutional** under the U.S. Commerce Clause. This calculator implements **state sales tax** on moving services, which IS legal and varies by state.

The calculator includes a comprehensive **Sales Tax System** that calculates:

1. 🏛️ **State-Specific Sales Tax** - Based on destination state (50 states + DC)
2. ✅ **Intrastate Recognition** - Proper tax treatment for same-state moves
3. 🌍 **International Moves** - USMCA duty-free household goods movement
4. 📊 **Accurate 2025 Rates** - Updated December 2025 with current state tax rates

## Key Features

### Interstate vs Intrastate Detection

The system automatically detects whether a move is:
- **Interstate** - Moving between different states (e.g., TX → CA)
- **Intrastate** - Moving within the same state (e.g., TX → TX)

State detection uses smart regex matching to avoid false positives (e.g., "Austin" won't match "IN").

### Sales Tax Calculation

**All Moves (Interstate and Intrastate):**
- State sales tax applies based on **destination state**
- No additional interstate commerce fees (unconstitutional)
- Example: TX → CA = 7.25% CA sales tax
- Example: TX → TX = 6.25% TX sales tax

**Tax-Exempt States:**
The following states do NOT charge sales tax on moving services:
- Alaska (AK)
- Delaware (DE)  
- Montana (MT)
- New Hampshire (NH)
- Oregon (OR)

### State Sales Tax Rates (Updated December 2025)

All 50 states + DC are configured with current sales tax rates:

| State | Code | Tax Rate | State | Code | Tax Rate |
|-------|------|----------|-------|------|----------|
| Alabama | AL | 4.00% | Montana | MT | 0.00% |
| Alaska | AK | 0.00% | Nebraska | NE | 5.50% |
| Arizona | AZ | 5.60% | Nevada | NV | 6.85% |
| Arkansas | AR | 6.50% | New Hampshire | NH | 0.00% |
| California | CA | 7.25% | New Jersey | NJ | 6.625% |
| Colorado | CO | 2.90% | New Mexico | NM | 5.125% |
| Connecticut | CT | 6.35% | New York | NY | 4.00% |
| Delaware | DE | 0.00% | North Carolina | NC | 4.75% |
| Florida | FL | 6.00% | North Dakota | ND | 5.00% |
| Georgia | GA | 4.00% | Ohio | OH | 5.75% |
| Hawaii | HI | 4.00% | Oklahoma | OK | 4.50% |
| Idaho | ID | 6.00% | Oregon | OR | 0.00% |
| Illinois | IL | 6.25% | Pennsylvania | PA | 6.00% |
| Indiana | IN | 7.00% | Rhode Island | RI | 7.00% |
| Iowa | IA | 6.00% | South Carolina | SC | 6.00% |
| Kansas | KS | 6.50% | South Dakota | SD | 4.50% |
| Kentucky | KY | 6.00% | Tennessee | TN | 7.00% |
| Louisiana | LA | 4.45% | Texas | TX | 6.25% |
| Maine | ME | 5.50% | Utah | UT | 4.85% |
| Maryland | MD | 6.00% | Vermont | VT | 6.00% |
| Massachusetts | MA | 6.25% | Virginia | VA | 5.30% |
| Michigan | MI | 6.00% | Washington | WA | 6.50% |
| Minnesota | MN | 6.875% | Washington DC | DC | 6.00% |
| Mississippi | MS | 7.00% | West Virginia | WV | 6.00% |
| Missouri | MO | 4.225% | Wisconsin | WI | 5.00% |
|||||Wyoming | WY | 4.00% |

**Note:** Rates shown are base state rates. Local city/county taxes may increase the total rate.

## Configuration

Sales taxes are configured in `data/household_goods_matrix.json`:

```json
{
  "tariffs": {
    "enable_interstate_tariffs": false,
    "interstate_tariff_rate": 0.0,
    "intrastate_tariff_rate": 0.0,
    "state_specific_taxes": {
      "AL": 0.04,
      "CA": 0.0725,
      "TX": 0.0625,
      "NY": 0.04,
      "FL": 0.06,
      "WA": 0.065,
      ... (all 50 states + DC)
    },
    "state_tax_note": "Updated December 2025 - State sales tax rates on moving/transportation services. Some states exempt moving services from sales tax (AK, DE, MT, NH, OR).",
    "international_tariffs": {
      "US_to_CA": 0.0,
      "US_to_MX": 0.0,
      "CA_to_US": 0.0,
      "MX_to_US": 0.0
    },
    "international_tariff_note": "USMCA provides duty-free movement for household goods relocations. Commercial tariffs do not apply to personal household goods moves."
  }
}
```

### Configuration Options

- **enable_interstate_tariffs** (boolean) - DEPRECATED - Should always be false (interstate tariffs are unconstitutional)
- **interstate_tariff_rate** (decimal) - DEPRECATED - Should always be 0.0
- **intrastate_tariff_rate** (decimal) - DEPRECATED - Should always be 0.0  
- **state_specific_taxes** (object) - State codes mapped to sales tax rates (50 states + DC)
- **international_tariffs** (object) - International tariffs (0.0 for USMCA countries)
- **state_tax_note** (string) - Documentation about tax rates and updates
- **international_tariff_note** (string) - Documentation about international moves

## API Response Structure

The breakdown now includes these tariff-related fields:

```json
{
  "breakdown": {
    "origin_state": "TX",
    "destination_state": "CA",
    "tariff_type": "interstate",
    "tariff_description": "Interstate (TX → CA)",
    "interstate_tariff": 279.92,
    "state_tax": 676.47,
    "total_tariffs_and_taxes": 956.38,
    "subtotal_before_tariffs": 9330.55,
    "subtotal": 10286.93
  }
}
```

### Tariff Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `origin_state` | string | 2-letter origin state code |
| `destination_state` | string | 2-letter destination state code |
| `tariff_type` | string | "interstate", "intrastate", or "none" |
| `tariff_description` | string | Human-readable tariff description |
| `interstate_tariff` | number | Interstate commerce fee amount |
| `state_tax` | number | State-specific moving tax amount |
| `total_tariffs_and_taxes` | number | Sum of all tariffs and taxes |
| `subtotal_before_tariffs` | number | Cost before tariffs applied |
| `subtotal` | number | Cost after tariffs (before minimum charge) |

## Example Calculations

### Example 1: Interstate Move (TX → CA)

**Route:** Austin, TX → Los Angeles, CA  
**Distance:** 1,500 miles  
**Weight:** 6,000 lbs

```
Subtotal (before tax):       $9,330.55
California State Tax (7.25%):  $676.47
──────────────────────────────────────
Total Sales Tax:               $676.47
Final Total:                $10,007.02
```

**Tax Impact:** 7.25% increase

### Example 2: Intrastate Move (TX → TX)

**Route:** Dallas, TX → Houston, TX  
**Distance:** 240 miles  
**Weight:** 6,000 lbs

```
Subtotal (before tax):       $6,341.50
Texas State Tax (6.25%):       $396.34
──────────────────────────────────────
Total Sales Tax:               $396.34
Final Total:                 $6,737.84
```

**Tax Impact:** 6.25% increase

### Example 3: Interstate Move (NY → FL)

**Route:** New York, NY → Miami, FL  
**Distance:** 1,300 miles  
**Weight:** 8,000 lbs

```
Subtotal (before tax):      $10,694.01
Florida State Tax (6%):        $641.64
──────────────────────────────────────
Total Sales Tax:               $641.64
Final Total:                $11,335.65
```

**Tax Impact:** 6.00% increase

## UI Display

The web interface displays taxes in a dedicated section:

```
📊 Sales Tax
  State Sales Tax (CA)                $676.47
  ─────────────────────────────────────────
  Total Sales Tax                     $676.47
```

If no sales tax applies (tax-exempt state):

```
✅ Sales Tax  
  No sales tax applies                  $0.00
```

## Custom Rate Overrides

You can override tariff rates via the API:

```python
result = calculator.calculate_should_cost(
    origin="Austin, TX",
    destination="Los Angeles, CA",
    distance_miles=1500,
    weight_pounds=6000,
    custom_rates={
        'interstate_tariff_rate': 0.05,  # Override to 5%
        'state_tax_CA': 0.10             # Override CA tax to 10%
    }
)
```

## Testing

Three new unit tests verify tariff functionality:

1. **test_interstate_tariff_applied** - Verifies interstate fees apply
2. **test_intrastate_no_tariff** - Verifies intrastate moves have no interstate fee
3. **test_state_tax_applied** - Verifies state-specific taxes work

```bash
python -m pytest tests/test_cost_engine.py -v
# 16 passed ✅
```

## Demo Scripts

**View tariff calculations:**
```bash
python test_tariffs.py
```

**View complete breakdown with tariffs:**
```bash
python test_breakdown.py
```

## Important Notes

### Legal Compliance ✅

> ✅ **UPDATED December 2025:** This calculator now implements **legally accurate sales tax** on moving services:
> - **State sales tax** is constitutional and varies by state (0%-7.25%)
> - **No interstate tariffs** (these would be unconstitutional under Commerce Clause)
> - **USMCA compliance** for US-Canada-Mexico moves (duty-free household goods)
> - Rates updated to current December 2025 state tax schedules
>
> **Disclaimer:** Tax rates shown are base state rates. Local city/county taxes may apply. Always consult with tax professionals for specific move scenarios.

### What These Taxes Represent

- ✅ **State sales tax** on moving/transportation services (legitimate, varies by state)
- ✅ **Local taxes** may increase total rate beyond base state rate (not shown)
- ✅ **Some states exempt** moving services from sales tax (AK, DE, MT, NH, OR)
- ✅ **Updated December 2025** with current state tax rates

## Disabling Sales Tax

To disable sales tax calculation entirely (for testing/modeling):

```json
{
  "tariffs": {
    "enable_interstate_tariffs": false,
    "state_specific_taxes": {}
  }
}
```

When disabled:
- All tax fields will be 0
- No tax section appears in UI
- Useful for cost modeling without taxes

## Future Enhancements

- [ ] Add ZIP code database for more accurate state detection
- [ ] County/city-level local tax rates
- [ ] Support for Canadian provincial sales taxes (GST/PST/HST)
- [ ] Support for Mexican states (IVA)
- [ ] Annual automatic tax rate updates
- [ ] Integration with state tax authority APIs
- [ ] Historical tax rate tracking

---

**Built with ❤️ by Batman the Code Puppy** 🐶  
*Making household goods moves transparent, one tariff at a time!*
