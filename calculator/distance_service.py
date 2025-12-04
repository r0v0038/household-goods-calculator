"""Distance calculation service using Google Maps and geopy fallback."""

import os
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Tuple, Optional


class DistanceService:
    """Service for calculating distances between locations."""

    def __init__(self, google_api_key: Optional[str] = None):
        """Initialize the distance service.
        
        Args:
            google_api_key: Google Maps API key for distance calculations.
                          If not provided, will check GOOGLE_MAPS_API_KEY env var.
                          Falls back to geopy if no API key available.
        """
        self.google_api_key = google_api_key or os.environ.get('GOOGLE_MAPS_API_KEY')
        self.geolocator = Nominatim(user_agent="household-goods-calculator")
        self.use_google_maps = bool(self.google_api_key)
    
    def _geocode_location(self, location: str) -> Optional[Tuple[float, float]]:
        """Convert location string to coordinates.
        
        Args:
            location: Location string (address, city, state, ZIP)
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        try:
            result = self.geolocator.geocode(location)
            if result:
                return (result.latitude, result.longitude)
            return None
        except Exception as e:
            print(f"Geocoding error for '{location}': {e}")
            return None
    
    def _calculate_google_maps_distance(self, origin: str, destination: str) -> Optional[float]:
        """Calculate driving distance using Google Maps Distance Matrix API.
        
        Args:
            origin: Origin location string
            destination: Destination location string
            
        Returns:
            Driving distance in miles, or None if calculation fails
        """
        if not self.google_api_key:
            return None
        
        try:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            params = {
                'origins': origin,
                'destinations': destination,
                'units': 'imperial',  # Get results in miles
                'key': self.google_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"Google Maps API error: {data.get('status')}")
                return None
            
            # Extract distance from response
            rows = data.get('rows', [])
            if not rows or not rows[0].get('elements'):
                return None
            
            element = rows[0]['elements'][0]
            
            if element.get('status') != 'OK':
                print(f"Google Maps route error: {element.get('status')}")
                return None
            
            # Distance is in meters, convert to miles
            distance_meters = element.get('distance', {}).get('value')
            if distance_meters is None:
                return None
            
            distance_miles = distance_meters * 0.000621371  # meters to miles
            return round(distance_miles, 2)
            
        except requests.exceptions.RequestException as e:
            print(f"Google Maps API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error calculating Google Maps distance: {e}")
            return None
    
    def _calculate_geodesic_distance(self, origin: str, destination: str) -> Optional[float]:
        """Calculate straight-line distance using geopy (fallback method).
        
        Args:
            origin: Origin location string
            destination: Destination location string
            
        Returns:
            Geodesic distance in miles, or None if calculation fails
        """
        origin_coords = self._geocode_location(origin)
        destination_coords = self._geocode_location(destination)
        
        if origin_coords is None or destination_coords is None:
            return None
        
        # Calculate distance using geodesic (great circle distance)
        distance_km = geodesic(origin_coords, destination_coords).kilometers
        distance_miles = distance_km * 0.621371  # Convert km to miles
        
        return round(distance_miles, 2)
    
    def calculate_distance(self, origin: str, destination: str) -> Optional[float]:
        """Calculate distance in miles between two locations.
        
        Uses Google Maps API for driving distance if available,
        falls back to geodesic (straight-line) distance otherwise.
        
        Args:
            origin: Origin location string
            destination: Destination location string
            
        Returns:
            Distance in miles, or None if calculation fails
        """
        # Try Google Maps first if API key is available
        if self.use_google_maps:
            distance = self._calculate_google_maps_distance(origin, destination)
            if distance is not None:
                print(f"Google Maps distance: {distance} miles (driving)")
                return distance
            else:
                print("Google Maps failed, falling back to geodesic distance")
        
        # Fallback to geodesic distance
        distance = self._calculate_geodesic_distance(origin, destination)
        if distance is not None:
            print(f"Geodesic distance: {distance} miles (straight-line)")
        
        return distance
