#!/usr/bin/env python3
"""Simple test for distance calculations."""

import os
from calculator.distance_service import DistanceService


def main():
    print("\n" + "="*70)
    print(" DISTANCE CALCULATION TEST")
    print("="*70 + "\n")
    
    # Check if API key is set
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    if api_key:
        print(f"Google Maps API Key: {api_key[:15]}...***")
        print("Mode: Google Maps (driving distances)\n")
    else:
        print("Google Maps API Key: Not set")
        print("Mode: Geodesic (straight-line distances)\n")
    
    # Initialize service
    service = DistanceService()
    
    # Test route
    origin = "Austin, TX"
    destination = "Los Angeles, CA"
    
    print(f"Calculating distance: {origin} -> {destination}")
    print("-" * 70)
    
    try:
        distance = service.calculate_distance(origin, destination)
        
        if distance:
            print(f"\nDistance: {distance:,.1f} miles")
            if service.use_google_maps:
                print("Method: Google Maps API (driving route)")
            else:
                print("Method: Geodesic calculation (straight-line)")
            print("\nSUCCESS!")
        else:
            print("\nFailed to calculate distance")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
