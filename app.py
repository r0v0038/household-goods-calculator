"""Flask web application for household goods should cost calculator."""

from flask import Flask, render_template, request, jsonify, send_file
from calculator import HouseholdGoodsCostCalculator
from calculator.distance_service import DistanceService
from calculator.bulk_processor import BulkProcessor
import traceback
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
calculator = HouseholdGoodsCostCalculator()
distance_service = DistanceService()
bulk_processor = BulkProcessor()


@app.route('/')
def index():
    """Render the main calculator page."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate should cost based on submitted form data."""
    try:
        data = request.get_json()
        
        origin = data.get('origin', '').strip()
        destination = data.get('destination', '').strip()
        weight = float(data.get('weight', 0))
        packing = data.get('packing_service', 'self_pack')
        storage = data.get('storage_option', 'no_storage')
        include_insurance = data.get('include_insurance', True)
        
        # Validate inputs
        if not origin or not destination:
            return jsonify({
                'success': False,
                'error': 'Origin and destination are required'
            }), 400
        
        if weight <= 0:
            return jsonify({
                'success': False,
                'error': 'Weight must be greater than 0'
            }), 400
        
        # Check if user provided manual distance
        manual_distance = data.get('distance_miles')
        
        if manual_distance:
            distance = float(manual_distance)
        else:
            # Calculate distance automatically
            distance = distance_service.calculate_distance(origin, destination)
            
            if distance is None:
                return jsonify({
                    'success': False,
                    'error': 'Could not calculate distance between locations. Please provide distance manually.'
                }), 400
        
        # Get custom rates if provided
        custom_rates = data.get('custom_rates', {})
        
        # Calculate should cost
        result = calculator.calculate_should_cost(
            origin=origin,
            destination=destination,
            distance_miles=distance,
            weight_pounds=weight,
            packing_service=packing,
            storage_option=storage,
            include_insurance=include_insurance,
            custom_rates=custom_rates
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        print(f"Error calculating cost: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Calculation error: {str(e)}'
        }), 500


@app.route('/bulk')
def bulk_upload():
    """Render the bulk upload page."""
    return render_template('bulk.html')


@app.route('/bulk/validate', methods=['POST'])
def validate_bulk_file():
    """Validate uploaded Excel file format."""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'Invalid file format. Please upload an Excel file (.xlsx or .xls)'
            }), 400
        
        # Validate file
        validation_result = bulk_processor.validate_excel_file(file.stream)
        
        return jsonify({
            'success': True,
            'validation': validation_result
        })
        
    except Exception as e:
        print(f"Error validating file: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Validation error: {str(e)}'
        }), 500


@app.route('/bulk/process', methods=['POST'])
def process_bulk_file():
    """Process bulk calculations from uploaded Excel file."""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Get custom rates from form data if provided
        custom_rates = None
        if request.form.get('custom_rates'):
            import json
            custom_rates = json.loads(request.form.get('custom_rates'))
        
        # Process bulk calculations
        result = bulk_processor.process_bulk_calculations(file.stream, custom_rates)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error processing bulk file: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        }), 500


@app.route('/bulk/download/<format>')
def download_results(format):
    """Download calculation results in specified format."""
    try:
        # Get results from session or request (in production, use proper storage)
        # For now, we'll accept results via query params (not ideal for production)
        import json
        results_json = request.args.get('results')
        
        if not results_json:
            return "No results to download", 400
        
        results = json.loads(results_json)
        
        if format == 'excel':
            excel_data = bulk_processor.generate_results_excel(results)
            return send_file(
                io.BytesIO(excel_data),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='household_goods_calculations.xlsx'
            )
        else:
            return "Invalid format", 400
            
    except Exception as e:
        print(f"Error downloading results: {traceback.format_exc()}")
        return f"Download error: {str(e)}", 500


@app.route('/bulk/template')
def download_template():
    """Download Excel template for bulk upload."""
    try:
        template_data = bulk_processor.generate_template()
        return send_file(
            io.BytesIO(template_data),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='household_goods_template.xlsx'
        )
    except Exception as e:
        print(f"Error generating template: {traceback.format_exc()}")
        return f"Template generation error: {str(e)}", 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    import os
    from waitress import serve
    
    port = int(os.environ.get('PORT', 5000))
    
    print(f'Starting Household Goods Calculator server on port {port}...')
    serve(app, host='0.0.0.0', port=port, _quiet=False)
