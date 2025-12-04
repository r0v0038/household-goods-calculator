"""Core cost calculation engine for household goods moves."""

import json
from typing import Dict, Tuple
from pathlib import Path


class HouseholdGoodsCostCalculator:
    """Calculate should cost estimates for household goods moves."""

    def __init__(self, matrix_file: str = None):
        """Initialize calculator with household goods matrix data.
        
        Args:
            matrix_file: Path to JSON file containing rate matrix
        """
        if matrix_file is None:
            matrix_file = Path(__file__).parent.parent / "data" / "household_goods_matrix.json"
        
        with open(matrix_file, 'r') as f:
            self.matrix = json.load(f)
    
    def _get_tier_adjustment(self, value: float, tiers: list) -> float:
        """Get rate adjustment based on tier thresholds.
        
        Args:
            value: The value to check (miles or pounds)
            tiers: List of tier dictionaries with max and rate_adjustment
            
        Returns:
            Rate adjustment multiplier
        """
        for tier in tiers:
            if value <= tier['max_pounds' if 'max_pounds' in tier else 'max_miles']:
                return tier['rate_adjustment']
        return tiers[-1]['rate_adjustment']
    
    def _get_transportation_cost_from_matrix(self, weight_pounds: float, distance_miles: float) -> Tuple[float, str, str]:
        """Get transportation cost from weight-distance matrix (CapRelo style).
        
        Args:
            weight_pounds: Total weight in pounds
            distance_miles: Distance in miles
            
        Returns:
            Tuple of (cost, weight_bracket_label, distance_bracket_label)
        """
        matrix = self.matrix.get('transportation_matrix', {})
        
        # Find weight bracket
        weight_bracket_idx = 0
        weight_label = "Unknown"
        for idx, bracket in enumerate(matrix['weight_brackets']):
            if bracket['min'] <= weight_pounds <= bracket['max']:
                weight_bracket_idx = idx
                weight_label = bracket['label']
                break
        
        # Find distance bracket
        distance_bracket_idx = 0
        distance_label = "Unknown"
        for idx, bracket in enumerate(matrix['distance_brackets']):
            if bracket['min'] <= distance_miles <= bracket['max']:
                distance_bracket_idx = idx
                distance_label = bracket['label']
                break
        
        # Get rate from matrix
        rate = matrix['rates'][weight_bracket_idx][distance_bracket_idx]
        
        return rate, weight_label, distance_label
    
    def _extract_state_code(self, location: str) -> str:
        """Extract state code from location string.
        
        Args:
            location: Location string (city, state, or ZIP)
            
        Returns:
            Two-letter state code or empty string if not found
        """
        import re
        location_upper = location.upper()
        
        # Common US state abbreviations
        states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]
        
        # Look for state code with word boundaries (comma, space, or end of string)
        # This prevents matching "IN" in "Austin" or "OR" in "York"
        for state in states:
            # Match state code preceded by comma+space or just space, followed by space or end
            pattern = r'(?:,\s*|\s)' + re.escape(state) + r'(?:\s|$)'
            if re.search(pattern, location_upper):
                return state
        
        return ''
    
    def _determine_region(self, location: str) -> str:
        """Determine region from location string.
        
        This is a simplified version. In production, you'd use a proper
        ZIP code to region mapping.
        
        Args:
            location: Location string (city, state, or ZIP)
            
        Returns:
            Region identifier
        """
        location_lower = location.lower()
        
        northeast_states = ['ny', 'ma', 'ct', 'ri', 'nh', 'vt', 'me', 'nj', 'pa']
        southeast_states = ['fl', 'ga', 'sc', 'nc', 'va', 'wv', 'ky', 'tn', 'al', 'ms', 'ar', 'la']
        midwest_states = ['oh', 'in', 'il', 'mi', 'wi', 'mn', 'ia', 'mo', 'nd', 'sd', 'ne', 'ks']
        southwest_states = ['tx', 'ok', 'nm', 'az']
        west_states = ['ca', 'or', 'wa', 'nv', 'id', 'ut', 'mt', 'wy', 'co', 'ak', 'hi']
        
        for state in northeast_states:
            if state in location_lower:
                return 'northeast'
        for state in southeast_states:
            if state in location_lower:
                return 'southeast'
        for state in midwest_states:
            if state in location_lower:
                return 'midwest'
        for state in southwest_states:
            if state in location_lower:
                return 'southwest'
        for state in west_states:
            if state in location_lower:
                return 'west'
        
        return 'default'
    
    def calculate_should_cost(
        self,
        origin: str,
        destination: str,
        distance_miles: float,
        weight_pounds: float,
        packing_service: str = 'self_pack',
        storage_option: str = 'no_storage',
        include_insurance: bool = True,
        custom_rates: Dict = None
    ) -> Dict:
        """Calculate the should cost for a household goods move.
        
        Args:
            origin: Origin location (city, state, or ZIP)
            destination: Destination location (city, state, or ZIP)
            distance_miles: Distance of move in miles
            weight_pounds: Total weight of household goods in pounds
            packing_service: Type of packing service ('full_pack', 'partial_pack', 'self_pack')
            storage_option: Storage option ('no_storage', 'storage_30days', 'storage_60days')
            include_insurance: Whether to include insurance in calculation
            custom_rates: Optional dictionary of custom rate overrides
            
        Returns:
            Dictionary containing cost breakdown and total
        """
        # Use custom rates if provided, otherwise use defaults from matrix
        if custom_rates is None:
            custom_rates = {}
        
        # Get transportation cost from weight-distance matrix
        transportation_cost, weight_bracket, distance_bracket = self._get_transportation_cost_from_matrix(
            weight_pounds, distance_miles
        )
        
        # Material costs (packing materials, supplies, etc.)
        material_cost = weight_pounds * self.matrix['base_rate_per_pound']
        
        # Base cost is now matrix-based transportation + material costs
        base_cost = transportation_cost + material_cost
        
        # Apply weight tier adjustment to material cost only
        weight_adjustment = self._get_tier_adjustment(
            weight_pounds,
            self.matrix['weight_tiers']
        )
        
        # Transportation cost is already from matrix, so only adjust material cost
        adjusted_cost = transportation_cost + (material_cost * weight_adjustment)
        
        # Apply service multipliers (use custom rates if provided)
        packing_multiplier = custom_rates.get(
            packing_service,
            self.matrix['service_multipliers'].get(packing_service, 1.0)
        )
        storage_multiplier = custom_rates.get(
            storage_option,
            self.matrix['service_multipliers'].get(storage_option, 1.0)
        )
        
        service_cost = adjusted_cost * packing_multiplier * storage_multiplier
        
        # Regional adjustment
        origin_region = self._determine_region(origin)
        dest_region = self._determine_region(destination)
        
        # Use average of origin and destination regional adjustments
        origin_adjustment = self.matrix['regional_adjustments'].get(origin_region, 1.0)
        dest_adjustment = self.matrix['regional_adjustments'].get(dest_region, 1.0)
        regional_adjustment = (origin_adjustment + dest_adjustment) / 2
        
        regional_cost = service_cost * regional_adjustment
        
        # Add insurance if requested (use custom rate if provided)
        insurance_cost = 0.0
        if include_insurance:
            insurance_rate = custom_rates.get('insurance_per_1000', self.matrix['insurance_rate_per_1000'])
            insurance_cost = (weight_pounds / 1000) * insurance_rate
        
        # Calculate cost subtotal (before fuel, tariffs, and discount)
        # This is the base amount to which discount will apply
        subtotal_base = regional_cost + insurance_cost
        
        # Calculate fuel surcharge BEFORE discount (it should not be discounted)
        fuel_surcharge_rate = custom_rates.get('fuel_surcharge', self.matrix['fuel_surcharge'])
        fuel_charge = subtotal_base * fuel_surcharge_rate
        
        # Apply discount ONLY to the base cost (excludes fuel surcharge and tariffs)
        # Discount applies to: material + transportation + services + regional + insurance
        # But NOT fuel surcharge or tariffs
        discount_rate = custom_rates.get('discount', 0.0)
        discount_amount = subtotal_base * discount_rate
        subtotal_after_discount = subtotal_base - discount_amount
        
        # Subtotal is now: (base costs - discount) + fuel charge (which is pre-discount)
        subtotal = subtotal_after_discount + fuel_charge
        
        # Calculate tariffs and taxes
        tariff_config = self.matrix.get('tariffs', {})
        origin_state = self._extract_state_code(origin)
        dest_state = self._extract_state_code(destination)
        
        interstate_tariff = 0.0
        state_tax = 0.0
        tariff_type = 'none'
        
        # Check if interstate tariffs are enabled
        if tariff_config.get('enable_interstate_tariffs', False):
            # Determine move type and calculate interstate tariff if applicable
            if origin_state and dest_state and origin_state != dest_state:
                tariff_type = 'interstate'
                interstate_rate = custom_rates.get(
                    'interstate_tariff_rate',
                    tariff_config.get('interstate_tariff_rate', 0.03)
                )
                interstate_tariff = subtotal * interstate_rate
            elif origin_state and dest_state and origin_state == dest_state:
                tariff_type = 'intrastate'
                intrastate_rate = custom_rates.get(
                    'intrastate_tariff_rate',
                    tariff_config.get('intrastate_tariff_rate', 0.0)
                )
                interstate_tariff = subtotal * intrastate_rate
        else:
            # Even if interstate tariffs disabled, still determine move type
            if origin_state and dest_state:
                if origin_state != dest_state:
                    tariff_type = 'interstate'
                else:
                    tariff_type = 'intrastate'
        
        # Apply state-specific sales tax based on destination state
        # State sales taxes are always applied (legitimate and legal)
        state_taxes = tariff_config.get('state_specific_taxes', {})
        if dest_state in state_taxes:
            state_tax_rate = custom_rates.get(
                f'state_tax_{dest_state}',
                state_taxes[dest_state]
            )
            state_tax = subtotal * state_tax_rate
        
        total_tariffs_and_taxes = interstate_tariff + state_tax
        total_cost = subtotal + insurance_cost + total_tariffs_and_taxes
        
        # Apply minimum charge (use custom rate if provided)
        minimum_charge = custom_rates.get('minimum_charge', self.matrix['minimum_charge'])
        if total_cost < minimum_charge:
            total_cost = minimum_charge
            applied_minimum = True
        else:
            applied_minimum = False
        
        # Calculate component costs for detailed breakdown
        # Material cost gets weight adjustment
        adjusted_material_cost = material_cost * weight_adjustment
        # Transportation cost is from matrix (no distance adjustment needed)
        adjusted_transportation_cost = transportation_cost
        
        # Service costs (packing and storage) - difference from adjusted base
        packing_cost = adjusted_cost * (packing_multiplier - 1.0)
        storage_cost = (adjusted_cost * packing_multiplier) * (storage_multiplier - 1.0)
        
        # Regional adjustment cost - difference from service cost
        regional_cost_difference = service_cost * (regional_adjustment - 1.0)
        
        # Determine move description
        tariff_description = 'None'
        if tariff_type == 'interstate' and dest_state:
            tariff_description = f'Interstate ({origin_state} → {dest_state})'
        elif tariff_type == 'intrastate' and dest_state:
            tariff_description = f'Intrastate ({dest_state})'
        
        return {
            'origin': origin,
            'destination': destination,
            'distance_miles': distance_miles,
            'weight_pounds': weight_pounds,
            'breakdown': {
                # Material costs
                'material_base_cost': round(material_cost, 2),
                'material_weight_adjustment': round(weight_adjustment, 2),
                'material_adjusted_cost': round(adjusted_material_cost, 2),
                
                # Transportation costs (matrix-based)
                'transportation_cost': round(transportation_cost, 2),
                'transportation_weight_bracket': weight_bracket,
                'transportation_distance_bracket': distance_bracket,
                'transportation_matrix_note': 'Rate from weight-distance matrix (CapRelo style)',
                
                # Service costs
                'packing_service': packing_service,
                'packing_multiplier': round(packing_multiplier, 2),
                'packing_cost': round(packing_cost, 2),
                'storage_option': storage_option,
                'storage_multiplier': round(storage_multiplier, 2),
                'storage_cost': round(storage_cost, 2),
                
                # Other costs
                'origin_region': origin_region,
                'destination_region': dest_region,
                'regional_adjustment': round(regional_adjustment, 2),
                'regional_cost_adjustment': round(regional_cost_difference, 2),
                'fuel_surcharge_rate': round(fuel_surcharge_rate, 2),
                'fuel_charge': round(fuel_charge, 2),
                'insurance_cost': round(insurance_cost, 2),
                
                # Discount
                'discount_rate': round(discount_rate, 2),
                'discount_amount': round(discount_amount, 2),
                'subtotal_after_discount': round(subtotal, 2),
                
                # Sales taxes (state-specific)
                'origin_state': origin_state,
                'destination_state': dest_state,
                'move_type': tariff_type,
                'move_description': tariff_description,
                'state_sales_tax': round(state_tax, 2),
                'total_sales_tax': round(total_tariffs_and_taxes, 2),
                # Legacy fields for backward compatibility
                'tariff_type': tariff_type,
                'tariff_description': tariff_description,
                'interstate_tariff': 0.0,
                'state_tax': round(state_tax, 2),
                'total_tariffs_and_taxes': round(total_tariffs_and_taxes, 2),
                
                # Totals
                'base_cost': round(base_cost, 2),
                'adjusted_base': round(adjusted_cost, 2),
                'service_adjusted_cost': round(service_cost, 2),
                'regional_cost': round(regional_cost, 2),
                'subtotal_before_tariffs': round(subtotal, 2),
                'subtotal': round(subtotal + total_tariffs_and_taxes, 2),
                'applied_minimum_charge': applied_minimum
            },
            'total_should_cost': round(total_cost, 2)
        }
