"""Bulk processing module for handling Excel file uploads and batch calculations."""

import pandas as pd
from typing import Dict, List, Any, Optional
import io
from .cost_engine import HouseholdGoodsCostCalculator
from .distance_service import DistanceService


class BulkProcessor:
    """Process bulk calculations from Excel files."""
    
    REQUIRED_COLUMNS = ['origin', 'destination', 'weight']
    OPTIONAL_COLUMNS = [
        'distance_miles',
        'packing_service', 
        'storage_option',
        'include_insurance'
    ]
    
    def __init__(self):
        """Initialize bulk processor with calculator and distance service."""
        self.calculator = HouseholdGoodsCostCalculator()
        self.distance_service = DistanceService()
    
    def validate_excel_file(self, file_stream) -> Dict[str, Any]:
        """Validate Excel file format and return validation results.
        
        Args:
            file_stream: File-like object containing Excel data
            
        Returns:
            Dict with validation results:
            - valid (bool): Whether file is valid
            - errors (List[str]): List of validation errors
            - warnings (List[str]): List of warnings
            - row_count (int): Number of data rows
        """
        try:
            df = pd.read_excel(file_stream)
            errors = []
            warnings = []
            
            # Check for required columns
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                errors.append(f"Missing required columns: {', '.join(missing_cols)}")
            
            # Check for empty dataframe
            if df.empty:
                errors.append("Excel file contains no data rows")
            
            # Check for null values in required columns
            if not df.empty and not missing_cols:
                for col in self.REQUIRED_COLUMNS:
                    null_count = df[col].isnull().sum()
                    if null_count > 0:
                        errors.append(f"Column '{col}' has {null_count} empty cell(s)")
                
                # Validate weight values
                if 'weight' in df.columns:
                    try:
                        weights = pd.to_numeric(df['weight'], errors='coerce')
                        invalid_weights = weights[weights <= 0].count()
                        if invalid_weights > 0:
                            errors.append(f"Found {invalid_weights} row(s) with invalid weight (must be > 0)")
                    except Exception as e:
                        errors.append(f"Error validating weights: {str(e)}")
            
            # Check for optional columns and warn if missing
            missing_optional = [col for col in self.OPTIONAL_COLUMNS if col not in df.columns]
            if missing_optional:
                warnings.append(f"Optional columns not provided (defaults will be used): {', '.join(missing_optional)}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'row_count': len(df) if not df.empty else 0
            }
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Error reading Excel file: {str(e)}"],
                'warnings': [],
                'row_count': 0
            }
    
    def process_bulk_calculations(self, file_stream, custom_rates: Optional[Dict] = None) -> Dict[str, Any]:
        """Process bulk calculations from Excel file.
        
        Args:
            file_stream: File-like object containing Excel data
            custom_rates: Optional custom rate overrides
            
        Returns:
            Dict containing:
            - success (bool): Overall success status
            - results (List[Dict]): List of calculation results
            - errors (List[str]): List of processing errors
            - summary (Dict): Summary statistics
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_stream)
            
            results = []
            errors = []
            successful = 0
            failed = 0
            
            # Process each row
            for idx, row in df.iterrows():
                row_num = idx + 2  # Excel row number (accounting for header)
                
                try:
                    # Extract required fields
                    origin = str(row.get('origin', '')).strip()
                    destination = str(row.get('destination', '')).strip()
                    weight = float(row.get('weight', 0))
                    
                    # Extract optional fields with defaults
                    distance_miles = row.get('distance_miles')
                    packing_service = str(row.get('packing_service', 'self_pack')).strip().lower()
                    storage_option = str(row.get('storage_option', 'no_storage')).strip().lower()
                    include_insurance = row.get('include_insurance', True)
                    
                    # Convert insurance to boolean if it's a string
                    if isinstance(include_insurance, str):
                        include_insurance = include_insurance.lower() in ['true', 'yes', '1', 'y']
                    
                    # Validate required fields
                    if not origin or not destination:
                        raise ValueError("Origin and destination are required")
                    
                    if weight <= 0:
                        raise ValueError(f"Weight must be greater than 0, got {weight}")
                    
                    # Calculate distance if not provided
                    if pd.isna(distance_miles) or distance_miles == '':
                        distance = self.distance_service.calculate_distance(origin, destination)
                        if distance is None:
                            raise ValueError("Could not calculate distance. Please provide distance manually.")
                    else:
                        distance = float(distance_miles)
                    
                    # Perform calculation
                    result = self.calculator.calculate_should_cost(
                        origin=origin,
                        destination=destination,
                        distance_miles=distance,
                        weight_pounds=weight,
                        packing_service=packing_service,
                        storage_option=storage_option,
                        include_insurance=include_insurance,
                        custom_rates=custom_rates
                    )
                    
                    # Add row metadata
                    result['row_number'] = row_num
                    result['status'] = 'success'
                    results.append(result)
                    successful += 1
                    
                except Exception as e:
                    error_msg = f"Row {row_num}: {str(e)}"
                    errors.append(error_msg)
                    
                    # Add failed row to results with error
                    results.append({
                        'row_number': row_num,
                        'status': 'failed',
                        'error': str(e),
                        'origin': origin if 'origin' in locals() else 'N/A',
                        'destination': destination if 'destination' in locals() else 'N/A',
                        'total_should_cost': 0
                    })
                    failed += 1
            
            # Generate summary
            summary = {
                'total_rows': len(df),
                'successful': successful,
                'failed': failed,
                'success_rate': f"{(successful / len(df) * 100):.1f}%" if len(df) > 0 else "0%"
            }
            
            return {
                'success': True,
                'results': results,
                'errors': errors,
                'summary': summary
            }
            
        except Exception as e:
            return {
                'success': False,
                'results': [],
                'errors': [f"Error processing file: {str(e)}"],
                'summary': {'total_rows': 0, 'successful': 0, 'failed': 0, 'success_rate': '0%'}
            }
    
    def generate_results_excel(self, results: List[Dict]) -> bytes:
        """Generate Excel file with calculation results.
        
        Args:
            results: List of calculation result dictionaries
            
        Returns:
            bytes: Excel file content
        """
        # Prepare data for Excel export
        export_data = []
        
        for result in results:
            if result.get('status') == 'failed':
                export_data.append({
                    'Row Number': result.get('row_number'),
                    'Status': 'FAILED',
                    'Error': result.get('error', 'Unknown error'),
                    'Origin': result.get('origin', 'N/A'),
                    'Destination': result.get('destination', 'N/A'),
                    'Total Should Cost': 0
                })
            else:
                breakdown = result.get('breakdown', {})
                
                # Calculate additional costs (packing + storage + fuel + insurance)
                packing_cost = breakdown.get('packing_cost', 0)
                storage_cost = breakdown.get('storage_cost', 0)
                fuel_charge = breakdown.get('fuel_charge', 0)
                insurance_cost = breakdown.get('insurance_cost', 0)
                additional_costs = packing_cost + storage_cost + fuel_charge + insurance_cost
                
                # Calculate cost per pound
                total_cost = result.get('total_should_cost', 0)
                weight = result.get('weight_pounds', 1)  # Avoid division by zero
                cost_per_lb = total_cost / weight if weight > 0 else 0
                
                export_data.append({
                    'Row Number': result.get('row_number'),
                    'Status': 'SUCCESS',
                    'Origin': result.get('origin'),
                    'Destination': result.get('destination'),
                    'Distance (miles)': result.get('distance_miles'),
                    'Weight (lbs)': result.get('weight_pounds'),
                    'Total Should Cost': total_cost,
                    'Cost per Lb': round(cost_per_lb, 2),
                    'Material Cost': breakdown.get('material_adjusted_cost', 0),
                    'Transportation Cost': breakdown.get('transportation_adjusted_cost', 0),
                    'Tariffs & Taxes': breakdown.get('total_tariffs_and_taxes', 0),
                    'Additional Costs': round(additional_costs, 2),
                    'Packing Cost': packing_cost,
                    'Storage Cost': storage_cost,
                    'Fuel Charge': fuel_charge,
                    'Insurance Cost': insurance_cost,
                    'Origin Region': breakdown.get('origin_region', ''),
                    'Destination Region': breakdown.get('destination_region', ''),
                    'Packing Service': breakdown.get('packing_service', ''),
                    'Storage Option': breakdown.get('storage_option', '')
                })
        
        # Create DataFrame
        df = pd.DataFrame(export_data)
        
        # Write to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')
        
        return output.getvalue()
    
    def generate_template(self) -> bytes:
        """Generate Excel template file with proper columns and examples.
        
        Returns:
            bytes: Excel template file content
        """
        template_data = {
            'origin': ['Bentonville, AR', 'Austin, TX', 'New York, NY'],
            'destination': ['Seattle, WA', 'Miami, FL', 'Los Angeles, CA'],
            'weight': [5000, 8000, 3500],
            'distance_miles': ['', '', ''],  # Optional - leave blank for auto-calc
            'packing_service': ['self_pack', 'partial_pack', 'full_pack'],
            'storage_option': ['no_storage', 'storage_30days', 'storage_60days'],
            'include_insurance': [True, True, False]
        }
        
        df = pd.DataFrame(template_data)
        
        # Write to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Template')
            
            # Get workbook and worksheet to add formatting
            workbook = writer.book
            worksheet = writer.sheets['Template']
            
            # Add notes/instructions
            worksheet.append([])
            worksheet.append(['INSTRUCTIONS:'])
            worksheet.append(['- origin: City, State or ZIP code (required)'])
            worksheet.append(['- destination: City, State or ZIP code (required)'])
            worksheet.append(['- weight: Total weight in pounds (required, must be > 0)'])
            worksheet.append(['- distance_miles: Optional, leave blank for auto-calculation'])
            worksheet.append(['- packing_service: self_pack, partial_pack, or full_pack'])
            worksheet.append(['- storage_option: no_storage, storage_30days, or storage_60days'])
            worksheet.append(['- include_insurance: TRUE or FALSE'])
        
        return output.getvalue()
