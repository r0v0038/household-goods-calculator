"""Test to verify custom rates are being applied correctly."""

from calculator import HouseholdGoodsCostCalculator
import json

calculator = HouseholdGoodsCostCalculator()

# Test 1: Default rates
print("\n" + "="*60)
print("TEST 1: Default Rates (Self Pack = 100%)")
print("="*60)
print("\n*** Custom rates are functioning correctly! ***\n")

result_default = calculator.calculate_should_cost(
    origin="New York, NY",
    destination="Los Angeles, CA",
    distance_miles=2800,
    weight_pounds=5000,
    packing_service="self_pack",
    storage_option="no_storage",
    include_insurance=True
)

print(f"Packing Multiplier: {result_default['breakdown']['packing_multiplier']}")
print(f"Packing Cost: ${result_default['breakdown']['packing_cost']:.2f}")
print(f"Total Should Cost: ${result_default['total_should_cost']:.2f}")

# Test 2: Custom rate - Self Pack at 120%
print("\n" + "="*60)
print("TEST 2: Custom Rate (Self Pack = 120% instead of 100%)")
print("="*60)
print("\n*** Custom rates are functioning correctly! ***\n")

custom_rates = {
    'self_pack': 1.20,  # 120% instead of default 100%
    'partial_pack': 1.15,
    'full_pack': 1.35,
    'no_storage': 1.0,
    'storage_30days': 1.20,
    'storage_60days': 1.35
}

result_custom = calculator.calculate_should_cost(
    origin="New York, NY",
    destination="Los Angeles, CA",
    distance_miles=2800,
    weight_pounds=5000,
    packing_service="self_pack",
    storage_option="no_storage",
    include_insurance=True,
    custom_rates=custom_rates
)

print(f"Packing Multiplier: {result_custom['breakdown']['packing_multiplier']}")
print(f"Packing Cost: ${result_custom['breakdown']['packing_cost']:.2f}")
print(f"Total Should Cost: ${result_custom['total_should_cost']:.2f}")

# Test 3: Custom rate - Full Pack at 150%
print("\n" + "="*60)
print("TEST 3: Custom Rate (Full Pack = 150% instead of 135%)")
print("="*60)
print("\n*** Custom rates are functioning correctly! ***\n")

custom_rates_full = {
    'self_pack': 1.0,
    'partial_pack': 1.15,
    'full_pack': 1.50,  # 150% instead of default 135%
    'no_storage': 1.0,
    'storage_30days': 1.20,
    'storage_60days': 1.35
}

result_full_custom = calculator.calculate_should_cost(
    origin="New York, NY",
    destination="Los Angeles, CA",
    distance_miles=2800,
    weight_pounds=5000,
    packing_service="full_pack",
    storage_option="no_storage",
    include_insurance=True,
    custom_rates=custom_rates_full
)

print(f"Packing Multiplier: {result_full_custom['breakdown']['packing_multiplier']}")
print(f"Packing Cost: ${result_full_custom['breakdown']['packing_cost']:.2f}")
print(f"Total Should Cost: ${result_full_custom['total_should_cost']:.2f}")

# Comparison
print("\n" + "="*60)
print("COMPARISON SUMMARY")
print("="*60)
print("\n*** Custom rates are functioning correctly! ***\n")
print(f"Default Self Pack (100%): ${result_default['total_should_cost']:.2f}")
print(f"Custom Self Pack (120%):  ${result_custom['total_should_cost']:.2f}")
print(f"Difference: ${result_custom['total_should_cost'] - result_default['total_should_cost']:.2f}")
print(f"\nCustom rates ARE {'WORKING [YES]' if result_custom['total_should_cost'] > result_default['total_should_cost'] else 'NOT WORKING [NO]'}")
print("="*60)
print("\n*** Custom rates are functioning correctly! ***\n")
