"""
Healthcare Facility Search Tool
Simulates searching for healthcare facilities
"""

def search_healthcare_facilities(location: str, urgency: str = "MEDIUM") -> dict:
    """
    Search for healthcare facilities near location
    """
    
    # Sample facilities in Jabalpur, MP
    facilities_database = {
        "jabalpur": [
            {
                "name": "Netaji Subhash Chandra Bose Medical College",
                "type": "Government Hospital",
                "distance_km": 5.2,
                "specialties": ["Emergency", "General Medicine", "Surgery"],
                "contact": "0761-2628073",
                "available_24x7": True
            },
            {
                "name": "Civil Hospital Jabalpur",
                "type": "Government Hospital",
                "distance_km": 3.8,
                "specialties": ["General Medicine", "Pediatrics"],
                "contact": "0761-2677777",
                "available_24x7": True
            },
            {
                "name": "PHC Gwarighat",
                "type": "Primary Health Centre",
                "distance_km": 2.1,
                "specialties": ["General Medicine", "Maternal Health"],
                "contact": "0761-XXXXXX",
                "available_24x7": False
            }
        ]
    }
    
    location_lower = location.lower()
    city = "jabalpur"
    
    facilities = facilities_database.get(city, facilities_database["jabalpur"])
    
    # Filter based on urgency
    if urgency == "HIGH":
        facilities = [f for f in facilities if f["available_24x7"]]
        facilities.sort(key=lambda x: x["distance_km"])
    else:
        facilities.sort(key=lambda x: x["distance_km"])
    
    return {
        "location": location,
        "urgency": urgency,
        "facilities_found": len(facilities),
        "facilities": facilities[:3],
        "message": f"Found {len(facilities)} facilities near {location}"
    }


def search_telemedicine_services() -> dict:
    """
    Search for available telemedicine services
    """
    
    telemedicine_options = [
        {
            "name": "eSanjeevani (Government)",
            "type": "Government Telemedicine",
            "availability": "24x7",
            "cost": "Free",
            "url": "https://esanjeevani.in/",
            "languages": ["Hindi", "English"],
            "specialties": ["General Medicine", "Pediatrics", "Gynecology"]
        }
    ]
    
    return {
        "services_available": len(telemedicine_options),
        "services": telemedicine_options,
        "message": "Government telemedicine services available for free consultation"
    }