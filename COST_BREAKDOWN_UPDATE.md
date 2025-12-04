# Cost Breakdown Enhancement - Household Goods Calculator

## Overview

The calculator now provides a **detailed cost breakdown** that separates household goods move costs into four distinct categories:

1. 📦 **Material Costs** - Weight-based costs for the household goods
2. 🚚 **Transportation Costs** - Distance-based shipping costs
3. 🛠️ **Service Costs** - Packing and storage services
4. 💰 **Other Costs** - Regional adjustments, fuel surcharge, and insurance

## What Changed?

### Backend (`calculator/cost_engine.py`)

The cost calculation engine now separates material and transportation costs and calculates each component individually:

**New breakdown fields:**

#### Material Costs
- `material_base_cost` - Base cost based on weight (lbs × rate per lb)
- `material_weight_adjustment` - Tier adjustment for weight (e.g., 0.85 = 15% discount)
- `material_adjusted_cost` - Final material cost after adjustments

#### Transportation Costs
- `transportation_base_cost` - Base cost based on distance (miles × rate per mile)
- `transportation_distance_adjustment` - Tier adjustment for distance
- `transportation_adjusted_cost` - Final transportation cost after adjustments

#### Service Costs
- `packing_service` - Type of packing service selected
- `packing_multiplier` - Multiplier applied for packing (e.g., 1.35 for full pack)
- `packing_cost` - Dollar amount for packing service
- `storage_option` - Type of storage selected
- `storage_multiplier` - Multiplier applied for storage
- `storage_cost` - Dollar amount for storage service

#### Other Costs
- `regional_cost_adjustment` - Dollar adjustment for origin/destination regions
- `fuel_charge` - Fuel surcharge amount
- `insurance_cost` - Insurance coverage cost

### Frontend (`templates/index.html`)

The UI now displays costs in **organized sections** with color-coded categories:

- **Material Costs** (Orange border) - Shows household goods weight costs
- **Transportation Costs** (Dark Blue border) - Shows distance/shipping costs
- **Service Costs** (Orange/Yellow border) - Shows packing and storage costs
- **Other Costs** (Green border) - Shows regional, fuel, and insurance costs

Each section shows:
- Individual line items with calculations
- Adjustment percentages and multipliers
- Section subtotals
- Clear, accessible formatting (WCAG 2.2 Level AA compliant)

## Example Output

```
Move: Dallas, TX -> Houston, TX
Distance: 240 miles
Weight: 6,000 lbs

MATERIAL COSTS (Household Goods)
  Base Material Cost:        $  4,500.00
  Weight Tier Adjustment:           85%
  Total Material Cost:       $  3,825.00

TRANSPORTATION COSTS
  Base Transportation:       $    600.00
  Distance Tier Adjustment:         90%
  Total Transportation Cost: $    540.00

SERVICE COSTS
  Packing (full_pack):       $  1,365.53
  Storage (storage_30days):  $  1,053.40
  Total Service Cost:        $  2,418.93

OTHER COSTS
  Regional (SE -> SW):       $    474.03
  Fuel Surcharge:            $    815.34
  Insurance:                 $     30.00
  Total Other Costs:         $  1,319.37

TOTAL SHOULD COST:           $  7,639.80
```

## Benefits

✅ **Transparency** - Customers can see exactly where their money goes
✅ **Itemization** - Clear separation of material, transportation, and service costs
✅ **Better Decision Making** - Easier to compare service options and understand trade-offs
✅ **Compliance Ready** - Detailed breakdown supports auditing and cost justification
✅ **Accessibility** - Color-coded, clearly labeled sections with proper ARIA attributes

## Testing

All 13 unit tests pass successfully:

```bash
python -m pytest tests/test_cost_engine.py -v
# 13 passed in 0.29s ✅
```

To see the new breakdown in action:

```bash
python test_breakdown.py
```

## Code Quality

- ✅ All files remain under 600 lines (as per Zen Puppy principles)
- ✅ DRY - No duplication, calculated values reused
- ✅ SOLID - Single responsibility for each cost component
- ✅ Clear separation of concerns
- ✅ Comprehensive test coverage maintained

## Migration Notes

**Breaking Changes:** None! The API remains backward compatible.

Old breakdown fields still exist:
- `base_cost`
- `adjusted_base`
- `service_adjusted_cost`
- `regional_cost`
- `subtotal`

New fields are additions that provide more granular detail.

---

**Built with ❤️ by Batman the Code Puppy** 🐶
