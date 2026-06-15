import requests
import json

def search_indian_competitors(company_name, niche):
    """
    Simulates a search for Indian competitors in a specific niche.
    In a real implementation, this would use Google Custom Search API or Serper.
    """
    print(f"[CompetitorSearch] Checking for '{company_name}'-like startups in India (Niche: {niche})...")
    
    # Mock data based on niche
    if "skincare" in niche.lower():
        return [
            {"name": "Mamaearth", "relevance": "High", "notes": "Major player in natural skincare."},
            {"name": "Dot & Key", "relevance": "Medium", "notes": "Focus on ingredient-led skincare."}
        ]
    elif "fintech" in niche.lower():
        return [
            {"name": "Paytm", "relevance": "High", "notes": "Payments giant."},
            {"name": "Razorpay", "relevance": "High", "notes": "B2B payments."}
        ]
    
    return []

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    niche = sys.argv[2] if len(sys.argv) > 2 else "General"
    results = search_indian_competitors(name, niche)
    print(json.dumps(results, indent=2))
