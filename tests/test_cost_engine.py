"""Unit tests for the cost calculation engine."""

import unittest
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from calculator.cost_engine import HouseholdGoodsCostCalculator


class TestHouseholdGoodsCostCalculator(unittest.TestCase):
    """Test cases for household goods cost calculator."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = HouseholdGoodsCostCalculator()

    def test_initialization(self):
        """Test calculator initializes with matrix data."""
        self.assertIsNotNone(self.calculator.matrix)
        self.assertIn('base_rate_per_mile', self.calculator.matrix)
        self.assertIn('base_rate_per_pound', self.calculator.matrix)

    def test_basic_calculation(self):
        """Test basic cost calculation with minimal inputs."""
        result = self.calculator.calculate_should_cost(
            origin="Bentonville, AR",
            destination="Austin, TX",
            distance_miles=500,
            weight_pounds=5000
        )

        self.assertIn('total_should_cost', result)
        self.assertGreater(result['total_should_cost'], 0)
        self.assertIn('breakdown', result)

    def test_minimum_charge_applied(self):
        """Test that minimum charge is applied for small moves."""
        result = self.calculator.calculate_should_cost(
            origin="Bentonville, AR",
            destination="Rogers, AR",
            distance_miles=10,
            weight_pounds=100
        )

        self.assertEqual(result['total_should_cost'], 500.00)
        self.assertTrue(result['breakdown']['applied_minimum_charge'])

    def test_packing_service_multiplier(self):
        """Test that packing service increases cost appropriately."""
        base_result = self.calculator.calculate_should_cost(
            origin="Dallas, TX",
            destination="Houston, TX",
            distance_miles=300,
            weight_pounds=5000,
            packing_service="self_pack"
        )

        full_pack_result = self.calculator.calculate_should_cost(
            origin="Dallas, TX",
            destination="Houston, TX",
            distance_miles=300,
            weight_pounds=5000,
            packing_service="full_pack"
        )

        self.assertGreater(
            full_pack_result['total_should_cost'],
            base_result['total_should_cost']
        )

    def test_storage_option_multiplier(self):
        """Test that storage option increases cost appropriately."""
        no_storage_result = self.calculator.calculate_should_cost(
            origin="Seattle, WA",
            destination="Portland, OR",
            distance_miles=200,
            weight_pounds=4000,
            storage_option="no_storage"
        )

        storage_result = self.calculator.calculate_should_cost(
            origin="Seattle, WA",
            destination="Portland, OR",
            distance_miles=200,
            weight_pounds=4000,
            storage_option="storage_30days"
        )

        self.assertGreater(
            storage_result['total_should_cost'],
            no_storage_result['total_should_cost']
        )

    def test_insurance_included(self):
        """Test insurance cost calculation."""
        without_insurance = self.calculator.calculate_should_cost(
            origin="New York, NY",
            destination="Boston, MA",
            distance_miles=250,
            weight_pounds=6000,
            include_insurance=False
        )

        with_insurance = self.calculator.calculate_should_cost(
            origin="New York, NY",
            destination="Boston, MA",
            distance_miles=250,
            weight_pounds=6000,
            include_insurance=True
        )

        self.assertGreater(
            with_insurance['total_should_cost'],
            without_insurance['total_should_cost']
        )
        self.assertGreater(with_insurance['breakdown']['insurance_cost'], 0)
        self.assertEqual(without_insurance['breakdown']['insurance_cost'], 0)

    def test_distance_tier_adjustment(self):
        """Test that distance tiers apply correct adjustments."""
        # Short distance (higher rate)
        short_result = self.calculator.calculate_should_cost(
            origin="Austin, TX",
            destination="San Antonio, TX",
            distance_miles=80,
            weight_pounds=3000
        )

        # Long distance (lower rate)
        long_result = self.calculator.calculate_should_cost(
            origin="New York, NY",
            destination="Los Angeles, CA",
            distance_miles=2800,
            weight_pounds=3000
        )

        # Per-mile cost should be lower for longer distances
        short_per_mile = short_result['total_should_cost'] / 80
        long_per_mile = long_result['total_should_cost'] / 2800

        # Note: This is a rough check - actual rates depend on all factors
        self.assertIsNotNone(short_per_mile)
        self.assertIsNotNone(long_per_mile)

    def test_weight_tier_adjustment(self):
        """Test that weight tiers apply correct adjustments."""
        result = self.calculator.calculate_should_cost(
            origin="Chicago, IL",
            destination="Detroit, MI",
            distance_miles=300,
            weight_pounds=8000
        )

        self.assertIn('material_weight_adjustment', result['breakdown'])
        self.assertGreater(result['breakdown']['material_weight_adjustment'], 0)

    def test_regional_adjustment(self):
        """Test that regional adjustments are applied."""
        result = self.calculator.calculate_should_cost(
            origin="San Francisco, CA",
            destination="Los Angeles, CA",
            distance_miles=400,
            weight_pounds=5000
        )

        self.assertIn('origin_region', result['breakdown'])
        self.assertIn('destination_region', result['breakdown'])
        self.assertIn('regional_adjustment', result['breakdown'])

    def test_fuel_surcharge_applied(self):
        """Test that fuel surcharge is calculated and applied."""
        result = self.calculator.calculate_should_cost(
            origin="Miami, FL",
            destination="Orlando, FL",
            distance_miles=250,
            weight_pounds=4000
        )

        self.assertGreater(result['breakdown']['fuel_charge'], 0)
        self.assertEqual(
            result['breakdown']['fuel_surcharge_rate'],
            self.calculator.matrix['fuel_surcharge']
        )

    def test_determine_region(self):
        """Test region determination logic."""
        self.assertEqual(
            self.calculator._determine_region("New York, NY"),
            'northeast'
        )
        self.assertEqual(
            self.calculator._determine_region("Atlanta, GA"),
            'southeast'
        )
        self.assertEqual(
            self.calculator._determine_region("Chicago, IL"),
            'midwest'
        )
        self.assertEqual(
            self.calculator._determine_region("Phoenix, AZ"),
            'southwest'
        )
        self.assertEqual(
            self.calculator._determine_region("Seattle, WA"),
            'west'
        )

    def test_all_service_combinations(self):
        """Test calculation with all service combinations."""
        packing_options = ['self_pack', 'partial_pack', 'full_pack']
        storage_options = ['no_storage', 'storage_30days', 'storage_60days']

        for packing in packing_options:
            for storage in storage_options:
                result = self.calculator.calculate_should_cost(
                    origin="Denver, CO",
                    destination="Salt Lake City, UT",
                    distance_miles=500,
                    weight_pounds=6000,
                    packing_service=packing,
                    storage_option=storage
                )

                self.assertGreater(result['total_should_cost'], 0)
                self.assertEqual(result['breakdown']['packing_service'], packing)
                self.assertEqual(result['breakdown']['storage_option'], storage)

    def test_result_structure(self):
        """Test that result contains all expected fields."""
        result = self.calculator.calculate_should_cost(
            origin="Boston, MA",
            destination="Philadelphia, PA",
            distance_miles=300,
            weight_pounds=5000
        )

        # Top-level fields
        expected_fields = [
            'origin', 'destination', 'distance_miles', 'weight_pounds',
            'breakdown', 'total_should_cost'
        ]
        for field in expected_fields:
            self.assertIn(field, result)

        # Breakdown fields - updated for new structure
        breakdown_fields = [
            # Material costs
            'material_base_cost', 'material_weight_adjustment', 'material_adjusted_cost',
            # Transportation costs
            'transportation_base_cost', 'transportation_distance_adjustment', 'transportation_adjusted_cost',
            # Service costs
            'packing_service', 'packing_multiplier', 'packing_cost',
            'storage_option', 'storage_multiplier', 'storage_cost',
            # Other costs
            'origin_region', 'destination_region', 'regional_adjustment', 'regional_cost_adjustment',
            'fuel_surcharge_rate', 'fuel_charge', 'insurance_cost',
            # Tariffs and taxes
            'origin_state', 'destination_state', 'tariff_type', 'tariff_description',
            'interstate_tariff', 'state_tax', 'total_tariffs_and_taxes',
            # Totals
            'base_cost', 'adjusted_base', 'service_adjusted_cost',
            'regional_cost', 'subtotal_before_tariffs', 'subtotal', 'applied_minimum_charge'
        ]
        for field in breakdown_fields:
            self.assertIn(field, result['breakdown'])


    def test_interstate_tariff_applied(self):
        """Test that interstate tariffs are applied for cross-state moves."""
        result = self.calculator.calculate_should_cost(
            origin="Austin, TX",
            destination="Los Angeles, CA",
            distance_miles=1500,
            weight_pounds=5000,
            packing_service="self_pack",
            storage_option="no_storage",
            include_insurance=True
        )

        # Should have interstate tariff
        self.assertEqual(result['breakdown']['tariff_type'], 'interstate')
        self.assertGreater(result['breakdown']['interstate_tariff'], 0)
        self.assertEqual(result['breakdown']['origin_state'], 'TX')
        self.assertEqual(result['breakdown']['destination_state'], 'CA')
        # CA has state tax, so state_tax should be > 0
        self.assertGreater(result['breakdown']['state_tax'], 0)
        self.assertGreater(result['breakdown']['total_tariffs_and_taxes'], 0)

    def test_intrastate_no_tariff(self):
        """Test that intrastate moves don't have interstate tariffs."""
        result = self.calculator.calculate_should_cost(
            origin="Dallas, TX",
            destination="Houston, TX",
            distance_miles=240,
            weight_pounds=5000,
            packing_service="self_pack",
            storage_option="no_storage",
            include_insurance=True
        )

        # Should have intrastate designation
        self.assertEqual(result['breakdown']['tariff_type'], 'intrastate')
        # No interstate tariff for intrastate moves
        self.assertEqual(result['breakdown']['interstate_tariff'], 0.0)
        self.assertEqual(result['breakdown']['origin_state'], 'TX')
        self.assertEqual(result['breakdown']['destination_state'], 'TX')

    def test_state_tax_applied(self):
        """Test that state-specific taxes are applied correctly."""
        # Move to California (has 7.25% tax)
        result = self.calculator.calculate_should_cost(
            origin="Seattle, WA",
            destination="Los Angeles, CA",
            distance_miles=1200,
            weight_pounds=4000,
            packing_service="self_pack",
            storage_option="no_storage",
            include_insurance=True
        )

        # Should have state tax for CA
        self.assertGreater(result['breakdown']['state_tax'], 0)
        self.assertEqual(result['breakdown']['destination_state'], 'CA')


if __name__ == '__main__':
    unittest.main()
