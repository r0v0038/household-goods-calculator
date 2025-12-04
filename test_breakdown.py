#!/usr/bin/env python3
"""Test script to demonstrate the new cost breakdown structure."""

from calculator import HouseholdGoodsCostCalculator
import json


def main():
    print("\n" + "="*70)
    print(" HOUSEHOLD GOODS COST CALCULATOR - NEW BREAKDOWN DEMO")
    print("="*70 + "\n")
    
    calculator = HouseholdGoodsCostCalculator()
    
    result = calculator.calculate_should_cost(
        origin="Dallas, TX",
        destination="Houston, TX",
        distance_miles=240,
        weight_pounds=6000,
        packing_service="full_pack",
        storage_option="storage_30days",
        include_insurance=True
    )
    
    print(f"Move: {result['origin']} -> {result['destination']}")
    print(f"Distance: {result['distance_miles']} miles")
    print(f"Weight: {result['weight_pounds']:,} lbs\n")
    
    breakdown = result['breakdown']
    
    print("="*70)
    print(" MATERIAL COSTS (Household Goods)")
    print("="*70)
    print(f"  Base Material Cost:        ${breakdown['material_base_cost']:>10,.2f}")
    print(f"  Weight Tier Adjustment:    {breakdown['material_weight_adjustment']:>10.0%}")
    print(f"  Total Material Cost:       ${breakdown['material_adjusted_cost']:>10,.2f}")
    
    print("\n" + "="*70)
    print(" TRANSPORTATION COSTS")
    print("="*70)
    print(f"  Base Transportation:       ${breakdown['transportation_base_cost']:>10,.2f}")
    print(f"  Distance Tier Adjustment:  {breakdown['transportation_distance_adjustment']:>10.0%}")
    print(f"  Total Transportation Cost: ${breakdown['transportation_adjusted_cost']:>10,.2f}")
    
    print("\n" + "="*70)
    print(" SERVICE COSTS")
    print("="*70)
    print(f"  Packing ({breakdown['packing_service']}):  ${breakdown['packing_cost']:>10,.2f}")
    print(f"  Storage ({breakdown['storage_option']}): ${breakdown['storage_cost']:>10,.2f}")
    total_service = breakdown['packing_cost'] + breakdown['storage_cost']
    print(f"  Total Service Cost:        ${total_service:>10,.2f}")
    
    print("\n" + "="*70)
    print(" OTHER COSTS")
    print("="*70)
    print(f"  Regional ({breakdown['origin_region']} -> {breakdown['destination_region']}): ${breakdown['regional_cost_adjustment']:>10,.2f}")
    print(f"  Fuel Surcharge:            ${breakdown['fuel_charge']:>10,.2f}")
    print(f"  Insurance:                 ${breakdown['insurance_cost']:>10,.2f}")
    total_other = breakdown['regional_cost_adjustment'] + breakdown['fuel_charge'] + breakdown['insurance_cost']
    print(f"  Total Other Costs:         ${total_other:>10,.2f}")
    
    print("\n" + "="*70)
    print(" TARIFFS & TAXES")
    print("="*70)
    if breakdown['total_tariffs_and_taxes'] > 0:
        print(f"  Tariff Type:               {breakdown['tariff_description']}")
        if breakdown['interstate_tariff'] > 0:
            print(f"  Interstate Commerce Fee:   ${breakdown['interstate_tariff']:>10,.2f}")
        if breakdown['state_tax'] > 0:
            print(f"  State Tax ({breakdown['destination_state']}):          ${breakdown['state_tax']:>10,.2f}")
        print(f"  Total Tariffs & Taxes:     ${breakdown['total_tariffs_and_taxes']:>10,.2f}")
    else:
        print(f"  No tariffs or taxes apply  ${0.00:>10,.2f}")
    
    print("\n" + "="*70)
    print(" TOTAL COST SUMMARY")
    print("="*70)
    print(f"  Material Costs:            ${breakdown['material_adjusted_cost']:>10,.2f}")
    print(f"  Transportation Costs:      ${breakdown['transportation_adjusted_cost']:>10,.2f}")
    print(f"  Service Costs:             ${total_service:>10,.2f}")
    print(f"  Other Costs:               ${total_other:>10,.2f}")
    print(f"  Tariffs & Taxes:           ${breakdown['total_tariffs_and_taxes']:>10,.2f}")
    print(f"  {'-'*70}")
    print(f"  TOTAL SHOULD COST:         ${result['total_should_cost']:>10,.2f}")
    print("="*70 + "\n")
    
    # Print JSON for inspection
    print("\nComplete breakdown as JSON:")
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
