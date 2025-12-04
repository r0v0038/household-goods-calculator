# 🗺️ Google Maps Distance Integration

## Overview

The Household Goods Calculator now uses **Google Maps Distance Matrix API** to calculate accurate **driving distances** between locations!

## ✨ Features

- ✅ **Automatic distance calculation** when mileage not provided
- ✅ **Driving distance** (actual road routes, not straight-line)
- ✅ **Smart fallback** to geodesic distance if Google Maps unavailable
- ✅ **No API key required** (optional enhancement)

## 🚀 Setup Instructions

### Option 1: With Google Maps API (Recommended)

**Step 1: Get a Google Maps API Key**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Distance Matrix API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Distance Matrix API"
   - Click "Enable"
4. Create API Key:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the generated API key

**Step 2: Configure the Application**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Replace 'your_google_maps_api_key_here' with your actual key
GOOGLE_MAPS_API_KEY=AIzaSy...
```

**Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Run the Application**

```bash
python app.py
```

### Option 2: Without Google Maps API (Fallback)

If you don't provide a Google Maps API key, the calculator will use **geopy** to calculate straight-line (geodesic) distances.

```bash
# Just run without setting GOOGLE_MAPS_API_KEY
python app.py
```

**Note:** Geodesic distances are shorter than actual driving distances, so costs may be underestimated.

## 📊 How It Works

### When User PROVIDES Mileage
```
User Input → Use provided distance → Calculate cost ✓
```

### When User DOES NOT Provide Mileage

**With Google Maps API:**
```
Origin + Destination
    ↓
Google Maps Distance Matrix API
    ↓
Driving Distance (actual road routes)
    ↓
Calculate cost ✓
```

**Without Google Maps API (Fallback):**
```
Origin + Destination
    ↓
Geopy Geocoding + Geodesic Calculation
    ↓
Straight-line Distance
    ↓
Calculate cost ✓
```

## 🧪 Testing

### Test 1: With Manual Distance
```
Origin: Austin, TX
Destination: Los Angeles, CA
Distance: 1500 (manually provided)

Result: Uses 1500 miles ✓
```

### Test 2: Auto-Calculate with Google Maps
```
Origin: Austin, TX
Destination: Los Angeles, CA
Distance: (leave blank)

Result: Google Maps calculates ~1,370 miles (driving) ✓
```

### Test 3: Auto-Calculate without API Key
```
Origin: Austin, TX
Destination: Los Angeles, CA
Distance: (leave blank)
No API Key set

Result: Geopy calculates ~1,230 miles (straight-line) ✓
```

## 💰 Google Maps API Pricing

**Distance Matrix API:**
- **Free tier:** $200/month credit = ~40,000 requests
- **Cost:** $0.005 per request (after free tier)
- **For most users:** Completely FREE!

**Monthly estimates:**
- 100 calculations/day = 3,000/month = **FREE**
- 1,000 calculations/day = 30,000/month = **FREE**
- 2,000 calculations/day = 60,000/month = ~$100/month

## 🔒 Security Best Practices

### Restrict Your API Key

1. **API Restrictions** (Recommended):
   - In Google Cloud Console → Credentials
   - Click your API key → "Edit"
   - Under "API restrictions"
   - Select "Restrict key"
   - Choose "Distance Matrix API"
   - Save

2. **Application Restrictions** (Optional):
   - HTTP referrers: `localhost:5000/*`, `yourdomain.com/*`
   - Or IP addresses: Your server IP

### Environment Variables

**Never commit `.env` file to git!**

The `.gitignore` should include:
```
.env
*.env
```

## 📝 API Response Example

### Google Maps Distance Matrix Response

```json
{
  "destination_addresses": ["Los Angeles, CA, USA"],
  "origin_addresses": ["Austin, TX, USA"],
  "rows": [
    {
      "elements": [
        {
          "distance": {
            "text": "1,370 mi",
            "value": 2204544  // meters
          },
          "duration": {
            "text": "20 hours 15 mins",
            "value": 72900  // seconds
          },
          "status": "OK"
        }
      ]
    }
  ],
  "status": "OK"
}
```

The calculator extracts `distance.value` and converts to miles.

## 🐛 Troubleshooting

### Error: "Could not calculate distance"

**Possible causes:**
1. Invalid location names
2. Google Maps API quota exceeded
3. API key not configured
4. Network connectivity issues

**Solutions:**
1. Provide distance manually
2. Check API key configuration
3. Verify API is enabled in Google Cloud Console
4. Check console logs for specific errors

### Error: "OVER_QUERY_LIMIT"

**Cause:** Exceeded free tier quota

**Solutions:**
1. Enable billing in Google Cloud Console
2. Reduce request frequency
3. Cache distance calculations
4. Use geodesic fallback

### API Key Not Working

**Checklist:**
- ✅ Distance Matrix API is enabled
- ✅ API key has no IP/referrer restrictions (for testing)
- ✅ Environment variable is set correctly
- ✅ Server restarted after setting env var

## 📊 Distance Comparison

| Route | Geodesic | Google Maps | Difference |
|-------|----------|-------------|------------|
| Austin, TX → Los Angeles, CA | ~1,230 mi | ~1,370 mi | +11% |
| Dallas, TX → Houston, TX | ~225 mi | ~240 mi | +7% |
| New York, NY → Miami, FL | ~1,092 mi | ~1,280 mi | +17% |

**Recommendation:** Use Google Maps for accurate cost estimates!

## 🔄 Migration from Geodesic

If you were using the old geodesic distance calculation:

**Before:**
```python
# Straight-line distance only
distance_service.calculate_distance(origin, destination)
# Result: 1,230 miles (geodesic)
```

**After (with API key):**
```python
# Driving distance via Google Maps
distance_service.calculate_distance(origin, destination)
# Result: 1,370 miles (actual driving route)
```

**After (without API key):**
```python
# Automatically falls back to geodesic
distance_service.calculate_distance(origin, destination)
# Result: 1,230 miles (geodesic fallback)
```

No code changes required! It's backward compatible.

## ✅ Verification

Check which method is being used:

```bash
# Run the app and watch console output
python app.py

# When calculating distance, you'll see:
"Google Maps distance: 1370.5 miles (driving)"
# OR
"Geodesic distance: 1230.2 miles (straight-line)"
```

## 🚀 Production Deployment

### Set Environment Variable

**Linux/Mac:**
```bash
export GOOGLE_MAPS_API_KEY="your_key_here"
python app.py
```

**Windows:**
```cmd
set GOOGLE_MAPS_API_KEY=your_key_here
python app.py
```

**Docker:**
```dockerfile
ENV GOOGLE_MAPS_API_KEY=your_key_here
```

**Heroku/Cloud:**
```bash
heroku config:set GOOGLE_MAPS_API_KEY=your_key_here
```

---

## 📞 Support

**Need help?**
- Google Maps API Docs: https://developers.google.com/maps/documentation/distance-matrix
- Issue with calculator: Check console logs
- API key issues: Verify in Google Cloud Console

---

**Built with ❤️ by Batman the Code Puppy** 🐶  
*Making distances accurate, one Google Maps call at a time!*
