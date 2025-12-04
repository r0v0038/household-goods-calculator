#!/usr/bin/env python3
"""Test script for Google Maps distance calculation."""

import os
from calculator.distance_service import DistanceService


def main():
    print("\n" + "="*70)
    print(" GOOGLE MAPS DISTANCE SERVICE TEST")
    print("="*70 + "\n")
    
    # Check if API key is set
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    if api_key:
        print(f"✅ Google Maps API Key found: {api_key[:10]}...")
        print("➡️  Will use Google Maps for driving distances\n")
    else:
        print("⚠️  No Google Maps API Key found")
        print("➡️  Will use geodesic (straight-line) distances\n")
        print("To enable Google Maps:")
        print("  1. Get API key from https://console.cloud.google.com/")
        print("  2. Enable Distance Matrix API")
        print("  3. Set environment variable:")
        print("     Windows: set GOOGLE_MAPS_API_KEY=your_key")
        print("     Linux/Mac: export GOOGLE_MAPS_API_KEY=your_key")
        print("")
    
    # Initialize service
    service = DistanceService()
    
    # Test routes
    test_routes = [
        ("Austin, TX", "Los Angeles, CA"),
        ("Dallas, TX", "Houston, TX"),
        ("New York, NY", "Miami, FL"),
        ("Seattle, WA", "Portland, OR")
    ]
    
    print("="*70)
    print(" TESTING DISTANCE CALCULATIONS")
    print("="*70 + "\n")
    
    for origin, destination in test_routes:
        print(f"Route: {origin} → {destination}")
        
        try:
            distance = service.calculate_distance(origin, destination)
            
            if distance:
                if service.use_google_maps:
                    print(f"  ✅ Driving Distance: {distance:,.1f} miles (Google Maps)")
                else:
                    print(f"  ✅ Straight-line Distance: {distance:,.1f} miles (Geodesic)")
            else:
                print(f"  ❌ Failed to calculate distance")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print("")
    
    print("="*70)
    print(" TEST COMPLETE")
    print("="*70 + "\n")
    
    if not api_key:
        print("💡 TIP: Enable Google Maps API for more accurate distances!")
        print("   See GOOGLE_MAPS_SETUP.md for instructions.\n")


if __name__ == '__main__':
    main()
