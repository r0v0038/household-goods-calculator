#!/usr/bin/env python3
"""Example usage of the household goods cost calculator."""

from calculator import HouseholdGoodsCostCalculator
from calculator.distance_service import DistanceService
import json


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*70 + "\n")


def main():
    """Run example calculations."""
    print("\n🏡 Household Goods Should Cost Calculator - Examples\n")
    
    # Initialize calculator
    calculator = HouseholdGoodsCostCalculator()
    distance_service = DistanceService()
    
    # Example 1: Basic move within same state
    print_separator()
    print("Example 1: Short Distance Move (Within Arkansas)")
    print_separator()
    
    result1 = calculator.calculate_should_cost(
        origin="Bentonville, AR",
        destination="Little Rock, AR",
        distance_miles=200,
        weight_pounds=3500,
        packing_service="self_pack",
        storage_option="no_storage",
        include_insurance=True
    )
    
    print(f"Origin: {result1['origin']}")
    print(f"Destination: {result1['destination']}")
    print(f"Distance: {result1['distance_miles']} miles")
    print(f"Weight: {result1['weight_pounds']:,} lbs")
    print(f"\n💰 Total Should Cost: ${result1['total_should_cost']:,.2f}")
    
    # Example 2: Cross-country move with full service
    print_separator()
    print("Example 2: Long Distance Move (Cross-Country)")
    print_separator()
    
    result2 = calculator.calculate_should_cost(
        origin="New York, NY",
        destination="Los Angeles, CA",
        distance_miles=2800,
        weight_pounds=9000,
        packing_service="full_pack",
        storage_option="storage_30days",
        include_insurance=True
    )
    
    print(f"Origin: {result2['origin']}")
    print(f"Destination: {result2['destination']}")
    print(f"Distance: {result2['distance_miles']:,} miles")
    print(f"Weight: {result2['weight_pounds']:,} lbs")
    print(f"Services: Full Packing + 30 Days Storage")
    print(f"\n💰 Total Should Cost: ${result2['total_should_cost']:,.2f}")
    
    # Example 3: Auto-calculate distance
    print_separator()
    print("Example 3: Auto-Calculated Distance")
    print_separator()
    
    origin = "Seattle, WA"
    destination = "Portland, OR"
    
    distance = distance_service.calculate_distance(origin, destination)
    
    if distance:
        print(f"Calculating distance from {origin} to {destination}...")
        print(f"Distance: {distance} miles (auto-calculated)")
        
        result3 = calculator.calculate_should_cost(
            origin=origin,
            destination=destination,
            distance_miles=distance,
            weight_pounds=5500,
            packing_service="partial_pack",
            storage_option="no_storage",
            include_insurance=True
        )
        
        print(f"Weight: {result3['weight_pounds']:,} lbs")
        print(f"Services: Partial Packing")
        print(f"\n💰 Total Should Cost: ${result3['total_should_cost']:,.2f}")
    else:
        print("⚠️  Could not auto-calculate distance")
    
    # Example 4: Detailed breakdown
    print_separator()
    print("Example 4: Detailed Cost Breakdown")
    print_separator()
    
    result4 = calculator.calculate_should_cost(
        origin="Dallas, TX",
        destination="Houston, TX",
        distance_miles=240,
        weight_pounds=6000,
        packing_service="full_pack",
        storage_option="storage_60days",
        include_insurance=True
    )
    
    print(f"Move: {result4['origin']} → {result4['destination']}")
    print(f"Distance: {result4['distance_miles']} miles")
    print(f"Weight: {result4['weight_pounds']:,} lbs\n")
    
    breakdown = result4['breakdown']
    print("📦 MATERIAL COSTS (Household Goods):")
    print(f"  Base Material Cost: ${breakdown['material_base_cost']:,.2f}")
    print(f"  Weight Tier Adjustment: {breakdown['material_weight_adjustment']:.0%}")
    print(f"  Total Material Cost: ${breakdown['material_adjusted_cost']:,.2f}")
    
    print("\n🚚 TRANSPORTATION COSTS:")
    print(f"  Base Transportation: ${breakdown['transportation_base_cost']:,.2f}")
    print(f"  Distance Tier Adjustment: {breakdown['transportation_distance_adjustment']:.0%}")
    print(f"  Total Transportation Cost: ${breakdown['transportation_adjusted_cost']:,.2f}")
    
    print("\n🛠️  SERVICE COSTS:")
    print(f"  Packing ({breakdown['packing_service']}): ${breakdown['packing_cost']:,.2f}")
    print(f"  Storage ({breakdown['storage_option']}): ${breakdown['storage_cost']:,.2f}")
    print(f"  Total Service Cost: ${breakdown['packing_cost'] + breakdown['storage_cost']:,.2f}")
    
    print("\n💰 OTHER COSTS:")
    print(f"  Regional Adjustment ({breakdown['origin_region']} → {breakdown['destination_region']}): ${breakdown['regional_cost_adjustment']:,.2f}")
    print(f"  Fuel Surcharge: ${breakdown['fuel_charge']:,.2f}")
    print(f"  Insurance: ${breakdown['insurance_cost']:,.2f}")
    print(f"  Total Other Costs: ${breakdown['regional_cost_adjustment'] + breakdown['fuel_charge'] + breakdown['insurance_cost']:,.2f}")
    
    print(f"\n  Subtotal: ${breakdown['subtotal']:,.2f}")
    
    if breakdown['applied_minimum_charge']:
        print(f"  ⚠️  Minimum Charge Applied: $500.00")
    
    print(f"\n💰 Total Should Cost: ${result4['total_should_cost']:,.2f}")
    
    # Example 5: Comparing service levels
    print_separator()
    print("Example 5: Service Level Comparison")
    print_separator()
    
    base_params = {
        'origin': 'Chicago, IL',
        'destination': 'Detroit, MI',
        'distance_miles': 280,
        'weight_pounds': 4500,
        'storage_option': 'no_storage',
        'include_insurance': True
    }
    
    services = ['self_pack', 'partial_pack', 'full_pack']
    service_names = ['Self Pack', 'Partial Pack', 'Full Pack']
    
    print(f"Comparing packing services for {base_params['weight_pounds']:,} lbs move")
    print(f"from {base_params['origin']} to {base_params['destination']}\n")
    
    for service, name in zip(services, service_names):
        result = calculator.calculate_should_cost(
            **{**base_params, 'packing_service': service}
        )
        print(f"  {name:15} → ${result['total_should_cost']:>10,.2f}")
    
    print_separator()
    print("\n✅ Examples complete!\n")


if __name__ == '__main__':
    main()
