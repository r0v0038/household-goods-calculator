# Weight-Distance Matrix Transportation Costs (CapRelo Style)

## Overview

Updated the household goods calculator to use a **weight-distance matrix** for transportation costs instead of simple per-mile calculations. This mirrors industry-standard pricing models used by companies like CapRelo.

## What Changed

### Before (Per-Mile Model)
```
Transportation Cost = Distance (miles) × $2.50/mile
```
- Linear pricing that doesn't reflect real-world economies of scale
- Doesn't account for weight-based pricing tiers
- Less accurate for industry benchmarking

### After (Matrix Model)
```
Transportation Cost = Matrix[Weight Bracket][Distance Bracket]
```
- Industry-standard weight-distance matrix
- 7 weight brackets: 0-1K, 1K-3K, 3K-5K, 5K-7K, 7K-10K, 10K-15K, 15K+ lbs
- 7 distance brackets: 0-100, 101-250, 251-500, 501-1K, 1K-1.5K, 1.5K-2.5K, 2.5K+ miles
- 49 rate combinations for accurate pricing

## Rate Matrix

| Weight \ Distance | 0-100 mi | 101-250 mi | 251-500 mi | 501-1K mi | 1K-1.5K mi | 1.5K-2.5K mi | 2.5K+ mi |
|------------------|----------|------------|------------|-----------|------------|--------------|----------|
| **0-1K lbs**     | $450     | $650       | $1,200     | $2,400    | $3,200     | $4,800       | $6,500   |
| **1K-3K lbs**    | $950     | $1,350     | $2,400     | $4,200    | $5,800     | $8,200       | $11,000  |
| **3K-5K lbs**    | $1,450   | $2,100     | $3,600     | $6,000    | $8,500     | $11,500      | $15,500  |
| **5K-7K lbs**    | $1,950   | $2,850     | $4,800     | $7,800    | $11,000    | $14,800      | $20,000  |
| **7K-10K lbs**   | $2,850   | $4,200     | $6,800     | $10,800   | $15,200    | $20,500      | $27,500  |
| **10K-15K lbs**  | $4,200   | $6,200     | $9,800     | $15,500   | $21,800    | $29,500      | $39,500  |
| **15K+ lbs**     | $5,800   | $8,500     | $13,500    | $21,500   | $30,000    | $40,500      | $54,000  |

## Example Calculations

### Small Local Move
- **Route:** Austin, TX → San Antonio, TX
- **Distance:** 80 miles (0-100 bracket)
- **Weight:** 800 lbs (0-1,000 bracket)
- **Transportation Cost:** $450 (from matrix)

### Large Cross-Country Move
- **Route:** New York, NY → Los Angeles, CA
- **Distance:** 2,800 miles (2,501+ bracket)
- **Weight:** 12,000 lbs (10,001-15,000 bracket)
- **Transportation Cost:** $39,500 (from matrix)

### Heavy Long-Distance Move
- **Route:** Seattle, WA → Miami, FL
- **Distance:** 3,100 miles (2,501+ bracket)
- **Weight:** 18,000 lbs (15,001+ bracket)
- **Transportation Cost:** $54,000 (from matrix)

## Benefits

✅ **Industry Standard:** Matches how real moving companies price services
✅ **Economies of Scale:** Longer distances get better per-mile rates
✅ **Weight-Based Tiers:** Heavier shipments reflect actual cost structures
✅ **Benchmarking Ready:** Can compare directly to CapRelo and other industry pricing
✅ **Transparency:** Clear bracket labels show which rate applies

## Cost Breakdown Structure

The calculator now returns:

```json
{
  "breakdown": {
    "transportation_cost": 39500.00,
    "transportation_weight_bracket": "10,001-15,000 lbs",
    "transportation_distance_bracket": "2,501+ miles",
    "transportation_matrix_note": "Rate from weight-distance matrix (CapRelo style)",
    "material_base_cost": 9000.00,
    "material_weight_adjustment": 0.8,
    "material_adjusted_cost": 7200.00,
    // ... other costs
  }
}
```

## Files Modified

1. **`data/household_goods_matrix.json`**
   - Added `transportation_matrix` with weight/distance brackets and rates
   - Removed obsolete `base_rate_per_mile` and `distance_tiers`
   - Kept `weight_tiers` for material cost adjustments

2. **`calculator/cost_engine.py`**
   - Added `_get_transportation_cost_from_matrix()` method
   - Updated `calculate_should_cost()` to use matrix lookups
   - Modified breakdown to include bracket labels
   - Removed distance adjustment for transportation (now baked into matrix)

## Testing

Run the test script to see the matrix in action:

```bash
cd household-goods-calculator
python test_matrix_transportation.py
```

This will show 4 different scenarios demonstrating how the matrix pricing works across various weight and distance combinations.

## Note

Material costs (packing supplies, materials, etc.) still use the `base_rate_per_pound` with weight tier adjustments. Only the **transportation cost** now uses the matrix-based approach.

---

*Updated to match CapRelo industry standards* 🚚📦
