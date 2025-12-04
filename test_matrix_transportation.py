#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for matrix-based transportation costs."""

import sys
import io
from calculator.cost_engine import HouseholdGoodsCostCalculator
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_matrix_based_transportation():
    """Test the new weight-distance matrix transportation costs."""
    print("\n" + "="*60)
    print("Testing Weight-Distance Matrix Transportation Costs")
    print("(CapRelo Style)")
    print("="*60 + "\n")
    
    calculator = HouseholdGoodsCostCalculator()
    
    # Test cases: Different weight and distance combinations
    test_cases = [
        {
            "name": "Small local move",
            "origin": "Austin, TX",
            "destination": "San Antonio, TX",
            "distance": 80,
            "weight": 800,
            "packing": "self_pack"
        },
        {
            "name": "Medium regional move",
            "origin": "Dallas, TX",
            "destination": "Houston, TX",
            "distance": 240,
            "weight": 4500,
            "packing": "partial_pack"
        },
        {
            "name": "Large long-distance move",
            "origin": "New York, NY",
            "destination": "Los Angeles, CA",
            "distance": 2800,
            "weight": 12000,
            "packing": "full_pack"
        },
        {
            "name": "Cross-country heavy move",
            "origin": "Seattle, WA",
            "destination": "Miami, FL",
            "distance": 3100,
            "weight": 18000,
            "packing": "full_pack"
        }
    ]
    
    for test in test_cases:
        print(f"\n[{test['name'].upper()}]")
        print("-" * 60)
        
        result = calculator.calculate_should_cost(
            origin=test['origin'],
            destination=test['destination'],
            distance_miles=test['distance'],
            weight_pounds=test['weight'],
            packing_service=test['packing'],
            storage_option='no_storage',
            include_insurance=True
        )
        
        breakdown = result['breakdown']
        
        print(f"Route: {test['origin']} → {test['destination']}")
        print(f"Distance: {test['distance']} miles")
        print(f"Weight: {test['weight']:,} lbs")
        print(f"\nTransportation (Matrix-based):")
        print(f"  Weight Bracket: {breakdown['transportation_weight_bracket']}")
        print(f"  Distance Bracket: {breakdown['transportation_distance_bracket']}")
        print(f"  Transportation Cost: ${breakdown['transportation_cost']:,.2f}")
        print(f"\nMaterial Costs:")
        print(f"  Base Material Cost: ${breakdown['material_base_cost']:,.2f}")
        print(f"  Weight Adjustment: {breakdown['material_weight_adjustment']}x")
        print(f"  Adjusted Material: ${breakdown['material_adjusted_cost']:,.2f}")
        print(f"\nAdditional Services:")
        print(f"  Packing ({breakdown['packing_service']}): ${breakdown['packing_cost']:,.2f}")
        print(f"  Storage ({breakdown['storage_option']}): ${breakdown['storage_cost']:,.2f}")
        print(f"  Fuel Surcharge: ${breakdown['fuel_charge']:,.2f}")
        print(f"  Insurance: ${breakdown['insurance_cost']:,.2f}")
        
        if breakdown.get('total_tariffs_and_taxes', 0) > 0:
            print(f"\nTariffs & Taxes:")
            print(f"  Type: {breakdown['tariff_description']}")
            print(f"  Interstate Tariff: ${breakdown['interstate_tariff']:,.2f}")
            print(f"  State Tax: ${breakdown['state_tax']:,.2f}")
            print(f"  Total Tariffs/Taxes: ${breakdown['total_tariffs_and_taxes']:,.2f}")
        
        print(f"\nTOTAL SHOULD COST: ${result['total_should_cost']:,.2f}")
    
    print("\n" + "="*60)
    print("Matrix-based transportation costs working!")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_matrix_based_transportation()
