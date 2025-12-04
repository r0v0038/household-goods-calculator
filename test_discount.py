#!/usr/bin/env python
"""Test discount functionality."""

from calculator import HouseholdGoodsCostCalculator

calculator = HouseholdGoodsCostCalculator()

# Test without discount
result_no_discount = calculator.calculate_should_cost(
    origin='Bentonville, AR',
    destination='Austin, TX',
    distance_miles=500,
    weight_pounds=5000,
    packing_service='self_pack',
    storage_option='no_storage',
    include_insurance=True,
    custom_rates={'discount': 0.0}
)

print("=" * 60)
print("TEST: Without Discount")
print("=" * 60)
print(f"Total Cost (no discount): ${result_no_discount['total_should_cost']:.2f}")
print(f"Subtotal before tariffs: ${result_no_discount['breakdown']['subtotal_before_tariffs']:.2f}")
print(f"Discount amount: ${result_no_discount['breakdown']['discount_amount']:.2f}")
print(f"Discount rate: {result_no_discount['breakdown']['discount_rate'] * 100:.1f}%")

# Test with 10% discount
result_with_discount = calculator.calculate_should_cost(
    origin='Bentonville, AR',
    destination='Austin, TX',
    distance_miles=500,
    weight_pounds=5000,
    packing_service='self_pack',
    storage_option='no_storage',
    include_insurance=True,
    custom_rates={'discount': 0.10}  # 10% discount
)

print("\n" + "=" * 60)
print("TEST: With 10% Discount")
print("=" * 60)
print(f"Total Cost (with discount): ${result_with_discount['total_should_cost']:.2f}")
print(f"Subtotal before tariffs: ${result_with_discount['breakdown']['subtotal_before_tariffs']:.2f}")
print(f"Discount amount: ${result_with_discount['breakdown']['discount_amount']:.2f}")
print(f"Discount rate: {result_with_discount['breakdown']['discount_rate'] * 100:.1f}%")
print(f"Subtotal after discount: ${result_with_discount['breakdown']['subtotal_after_discount']:.2f}")

# Verify discount is NOT applied to fuel surcharge (pre-discount) but tariffs use discounted subtotal
no_disc_fuel = result_no_discount['breakdown']['fuel_charge']
with_disc_fuel = result_with_discount['breakdown']['fuel_charge']
no_disc_tariff = result_no_discount['breakdown']['total_tariffs_and_taxes']
with_disc_tariff = result_with_discount['breakdown']['total_tariffs_and_taxes']

print("\n" + "=" * 60)
print("VERIFICATION: Discount applied correctly")
print("=" * 60)
print(f"Fuel charge (no discount): ${no_disc_fuel:.2f}")
print(f"Fuel charge (with discount): ${with_disc_fuel:.2f}")
print(f"Fuel charges match: {no_disc_fuel == with_disc_fuel} (should be True - fuel is pre-discount)")
print()
print(f"Tariffs (no discount): ${no_disc_tariff:.2f}")
print(f"Tariffs (with discount): ${with_disc_tariff:.2f}")
print(f"Tariffs are lower: {with_disc_tariff < no_disc_tariff} (should be True - tariffs calculated on discounted subtotal)")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
cost_savings = result_no_discount['total_should_cost'] - result_with_discount['total_should_cost']
print(f"Cost without discount: ${result_no_discount['total_should_cost']:.2f}")
print(f"Cost with 10% discount: ${result_with_discount['total_should_cost']:.2f}")
print(f"Total savings: ${cost_savings:.2f}")
print()
if cost_savings > 0:
    print("SUCCESS: Discount is working correctly!")
else:
    print("ERROR: Discount not applied!")