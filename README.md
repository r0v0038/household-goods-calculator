# 🏡 Household Goods Should Cost Calculator

A comprehensive web application for calculating estimated costs for household goods moves based on origin, destination, weight, and service requirements.

## Features

📁 **Bulk Upload Processing**
- Upload Excel files for batch calculations
- Process hundreds of moves at once
- Auto-validation with helpful error messages
- Download detailed Excel reports
- Template generator with examples
- Real-time progress tracking

✨ **Smart Cost Calculation**
- Distance-based pricing with tier adjustments
- Weight-based pricing with volume discounts
- Regional cost adjustments (Northeast, Southeast, Midwest, Southwest, West)
- Service multipliers (packing, storage)
- Fuel surcharge calculation
- Optional insurance coverage
- Minimum charge protection

🌐 **Auto Distance Calculation**
- Automatic geocoding of addresses, cities, states, or ZIP codes
- Great circle distance calculation
- Manual distance override option

♿ **WCAG 2.2 Level AA Compliant**
- Full keyboard navigation support
- ARIA labels and live regions
- High contrast mode support
- Reduced motion support
- Screen reader friendly
- Proper focus management

## Technology Stack

- **Backend**: Python 3.x, Flask
- **Geocoding**: geopy with Nominatim
- **Data Processing**: pandas, numpy
- **Frontend**: Vanilla JavaScript, Modern CSS
- **Standards**: WCAG 2.2 Level AA

## Pages

### Single Calculator (`/`)
Calculate should cost for individual moves with interactive form interface.

### Bulk Upload (`/bulk`)
Process multiple moves at once via Excel file upload. See [BULK_UPLOAD_GUIDE.md](BULK_UPLOAD_GUIDE.md) for detailed instructions.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or uv package manager

### Setup (Using uv - Walmart Recommended)

```bash
# Navigate to project directory
cd household-goods-calculator

# Install dependencies using uv with Walmart's artifactory
uv pip install -r requirements.txt \
  --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple \
  --allow-insecure-host pypi.ci.artifacts.walmart.com
```

### Setup (Alternative - Using pip)

```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Deployment

See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for 5-minute deployment guide or [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for comprehensive options.

**Quick Options:**
- ⚡ **Render.com** (FREE, 5 min) - Recommended for quick sharing
- 🚀 **Railway.app** (FREE, 3 min) - Best free tier, no sleep
- 🏢 **Azure App Service** - Walmart internal deployment
- 🐳 **Docker** - Self-hosted option

## Usage

1. **Configure Rates (Optional)**:
   - Click "⚙️ Advanced Rate Settings" to expand configuration panel
   - Adjust packing service percentages (Self Pack, Partial Pack, Full Pack)
   - Modify storage option percentages (No Storage, 30 Days, 60 Days)
   - Change insurance rate per $1,000 lbs
   - Update fuel surcharge percentage
   - Set minimum charge amount
   - Click "Reset to Defaults" to restore original values

2. **Enter Move Details**:
   - Origin: City, State, or ZIP code (e.g., "Bentonville, AR" or "72712")
   - Destination: City, State, or ZIP code (e.g., "Austin, TX" or "78701")
   - Weight: Total weight in pounds
   - Distance: Optional manual override (auto-calculated if blank)

3. **Select Service Options**:
   - Packing Service: Self Pack, Partial Pack, Full Pack
   - Storage Option: No Storage, 30 Days, 60 Days
   - Insurance: Optional coverage

4. **Calculate**: Click "Calculate Should Cost" to get your estimate

5. **Review Results**: 
   - Total should cost estimate
   - Detailed cost breakdown
   - Applied adjustments and multipliers

## Cost Calculation Methodology

The calculator uses a multi-factor pricing model:

### Base Rates
- **Per Mile**: $2.50
- **Per Pound**: $0.75

### Distance Tiers (Rate Adjustments)
| Distance | Adjustment |
|----------|------------|
| 0-100 mi | 100% |
| 101-500 mi | 90% |
| 501-1,000 mi | 85% |
| 1,001-2,000 mi | 80% |
| 2,001+ mi | 75% |

### Weight Tiers (Rate Adjustments)
| Weight | Adjustment |
|--------|------------|
| 0-1,000 lbs | 100% |
| 1,001-3,000 lbs | 95% |
| 3,001-5,000 lbs | 90% |
| 5,001-10,000 lbs | 85% |
| 10,001+ lbs | 80% |

### Regional Multipliers
- **Northeast**: 1.15x
- **Southeast**: 1.05x
- **Midwest**: 1.0x (baseline)
- **Southwest**: 1.10x
- **West**: 1.20x

### Additional Charges
- **Fuel Surcharge**: 12% of base cost
- **Insurance**: $5 per $1,000 of weight
- **Minimum Charge**: $500.00

## Project Structure

```
household-goods-calculator/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── calculator/
│   ├── __init__.py                # Module initialization
│   ├── cost_engine.py             # Core calculation logic
│   └── distance_service.py        # Geocoding and distance calculation
├── data/
│   └── household_goods_matrix.json # Rate matrix configuration
└── templates/
    └── index.html                 # Web interface (WCAG 2.2 AA compliant)
```

## Customization

### Updating Rate Matrix

Edit `data/household_goods_matrix.json` to adjust:
- Base rates per mile and pound
- Service multipliers
- Distance and weight tier adjustments
- Regional adjustments
- Fuel surcharge percentage
- Insurance rates
- Minimum charge

### Adding New Regions

Update the `_determine_region()` method in `calculator/cost_engine.py` to add new regional classifications.

## API Endpoints

### `POST /calculate`

Calculate should cost for a move.

**Request Body**:
```json
{
  "origin": "Bentonville, AR",
  "destination": "Austin, TX",
  "weight": 5000,
  "packing_service": "full_pack",
  "storage_option": "storage_30days",
  "include_insurance": true,
  "distance_miles": 500  // Optional
}
```

**Response**:
```json
{
  "success": true,
  "result": {
    "origin": "Bentonville, AR",
    "destination": "Austin, TX",
    "distance_miles": 500,
    "weight_pounds": 5000,
    "total_should_cost": 4567.89,
    "breakdown": { ... }
  }
}
```

### `GET /health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy"
}
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## Best Practices

- ✅ Keep files under 600 lines (following DRY, YAGNI, SOLID principles)
- ✅ Modular architecture for easy maintenance
- ✅ WCAG 2.2 Level AA accessibility compliance
- ✅ Responsive design for all screen sizes
- ✅ Error handling and validation
- ✅ Clear separation of concerns

## Future Enhancements

- [ ] Integration with real-time fuel price APIs
- [ ] Historical cost tracking and analytics
- [ ] PDF report generation
- [ ] Multiple move comparison
- [ ] Database integration for rate history
- [ ] Admin panel for rate matrix management
- [ ] Authentication and user accounts
- [ ] API rate limiting and caching

## License

Internal Walmart Global Tech Tool

## Support

For questions or issues, please contact the development team.

---

**Built with 🐶 by Batman (code-puppy) on a rainy weekend in May 2025**
