#!/usr/bin/env python3
"""Demonstration of state sales tax calculations for moving services."""

from calculator import HouseholdGoodsCostCalculator
import json


def print_separator(char="=", length=70):
    print(char * length)


def main():
    print("\n" + "="*70)
    print(" STATE SALES TAX DEMONSTRATION - Moving Services (Dec 2025)")
    print("="*70 + "\n")
    
    calculator = HouseholdGoodsCostCalculator()
    
    # Example 1: Interstate move (TX -> CA) - California sales tax applies
    print_separator()
    print(" Example 1: INTERSTATE MOVE (Texas to California)")
    print(" California sales tax: 7.25%")
    print_separator()
    
    result1 = calculator.calculate_should_cost(
        origin="Austin, TX",
        destination="Los Angeles, CA",
        distance_miles=1500,
        weight_pounds=6000,
        packing_service="full_pack",
        storage_option="no_storage",
        include_insurance=True
    )
    
    b1 = result1['breakdown']
    print(f"\nRoute: {result1['origin']} -> {result1['destination']}")
    print(f"Distance: {result1['distance_miles']:,} miles")
    print(f"Weight: {result1['weight_pounds']:,} lbs\n")
    
    print("SALES TAX DETAILS:")
    print(f"  Origin State:              {b1['origin_state']}")
    print(f"  Destination State:         {b1['destination_state']}")
    print(f"  Move Type:                 {b1['tariff_type'].upper()}")
    print(f"  State Sales Tax (CA):      ${b1['state_tax']:>10,.2f} (7.25% of subtotal)")
    print(f"  Total Sales Tax:           ${b1['total_tariffs_and_taxes']:>10,.2f}")
    print(f"\n  Subtotal (before tax):     ${b1['subtotal_before_tariffs']:>10,.2f}")
    print(f"  Final Total:               ${result1['total_should_cost']:>10,.2f}")
    
    # Example 2: Intrastate move (TX -> TX) - Texas sales tax applies
    print("\n" + "="*70)
    print(" Example 2: INTRASTATE MOVE (Within Texas)")
    print(" Texas sales tax: 6.25%")
    print_separator()
    
    result2 = calculator.calculate_should_cost(
        origin="Dallas, TX",
        destination="Houston, TX",
        distance_miles=240,
        weight_pounds=6000,
        packing_service="full_pack",
        storage_option="no_storage",
        include_insurance=True
    )
    
    b2 = result2['breakdown']
    print(f"\nRoute: {result2['origin']} -> {result2['destination']}")
    print(f"Distance: {result2['distance_miles']:,} miles")
    print(f"Weight: {result2['weight_pounds']:,} lbs\n")
    
    print("SALES TAX DETAILS:")
    print(f"  Origin State:              {b2['origin_state']}")
    print(f"  Destination State:         {b2['destination_state']}")
    print(f"  Move Type:                 {b2['tariff_type'].upper()}")
    print(f"  State Sales Tax (TX):      ${b2['state_tax']:>10,.2f} (6.25% of subtotal)")
    print(f"  Total Sales Tax:           ${b2['total_tariffs_and_taxes']:>10,.2f}")
    print(f"\n  Subtotal (before tax):     ${b2['subtotal_before_tariffs']:>10,.2f}")
    print(f"  Final Total:               ${result2['total_should_cost']:>10,.2f}")
    
    # Example 3: Interstate move (NY -> FL) - Florida sales tax applies
    print("\n" + "="*70)
    print(" Example 3: INTERSTATE MOVE (New York to Florida)")
    print(" Florida sales tax: 6.0%")
    print_separator()
    
    result3 = calculator.calculate_should_cost(
        origin="New York, NY",
        destination="Miami, FL",
        distance_miles=1300,
        weight_pounds=8000,
        packing_service="partial_pack",
        storage_option="storage_30days",
        include_insurance=True
    )
    
    b3 = result3['breakdown']
    print(f"\nRoute: {result3['origin']} -> {result3['destination']}")
    print(f"Distance: {result3['distance_miles']:,} miles")
    print(f"Weight: {result3['weight_pounds']:,} lbs\n")
    
    print("SALES TAX DETAILS:")
    print(f"  Origin State:              {b3['origin_state']}")
    print(f"  Destination State:         {b3['destination_state']}")
    print(f"  Move Type:                 {b3['tariff_type'].upper()}")
    print(f"  State Sales Tax (FL):      ${b3['state_tax']:>10,.2f} (6.0% of subtotal)")
    print(f"  Total Sales Tax:           ${b3['total_tariffs_and_taxes']:>10,.2f}")
    print(f"\n  Subtotal (before tax):     ${b3['subtotal_before_tariffs']:>10,.2f}")
    print(f"  Final Total:               ${result3['total_should_cost']:>10,.2f}")
    
    # Comparison Summary
    print("\n" + "="*70)
    print(" SALES TAX COMPARISON SUMMARY")
    print_separator()
    print(f"\n{'Move Type':<30} {'Base Cost':>12} {'Sales Tax':>12} {'Total':>12}")
    print_separator("-")
    print(f"{'Interstate (TX->CA)':<30} ${b1['subtotal_before_tariffs']:>11,.2f} ${b1['total_tariffs_and_taxes']:>11,.2f} ${result1['total_should_cost']:>11,.2f}")
    print(f"{'Intrastate (TX->TX)':<30} ${b2['subtotal_before_tariffs']:>11,.2f} ${b2['total_tariffs_and_taxes']:>11,.2f} ${result2['total_should_cost']:>11,.2f}")
    print(f"{'Interstate (NY->FL)':<30} ${b3['subtotal_before_tariffs']:>11,.2f} ${b3['total_tariffs_and_taxes']:>11,.2f} ${result3['total_should_cost']:>11,.2f}")
    print_separator("-")
    
    # Calculate sales tax percentages
    tax_pct_1 = (b1['total_tariffs_and_taxes'] / b1['subtotal_before_tariffs']) * 100
    tax_pct_2 = (b2['total_tariffs_and_taxes'] / b2['subtotal_before_tariffs']) * 100
    tax_pct_3 = (b3['total_tariffs_and_taxes'] / b3['subtotal_before_tariffs']) * 100
    
    print(f"\nSales Tax as % of base cost:")
    print(f"  Interstate (TX->CA):       {tax_pct_1:>6.2f}% (CA sales tax 7.25%)")
    print(f"  Intrastate (TX->TX):       {tax_pct_2:>6.2f}% (TX sales tax 6.25%)")
    print(f"  Interstate (NY->FL):       {tax_pct_3:>6.2f}% (FL sales tax 6.0%)")
    
    print("\n" + "="*70)
    print(" NOTES: (Updated December 2025)")
    print("="*70)
    print("""
  LEGAL & ACCURATE:
  - State sales tax applies based on DESTINATION state
  - Sales tax rates updated to December 2025 standards
  - No interstate commerce fees (unconstitutional under Commerce Clause)
  - Tax-exempt states: AK, DE, MT, NH, OR (no sales tax on moving services)
  
  SAMPLE STATE RATES (50 states + DC configured):
      * California (CA): 7.25%    * New York (NY): 4.00%
      * Texas (TX): 6.25%         * Washington (WA): 6.50%
      * Florida (FL): 6.00%       * Illinois (IL): 6.25%
      * Tennessee (TN): 7.00%     * Mississippi (MS): 7.00%
      * Minnesota (MN): 6.875%    * Nevada (NV): 6.85%
  
  CONFIGURATION NOTES:
  - Rates shown are BASE state rates (local taxes may increase total)
  - All 50 states + DC are configured with current rates
  - Rates are configurable in household_goods_matrix.json
  - Calculation applies to subtotal (after all service costs)
    """)
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
