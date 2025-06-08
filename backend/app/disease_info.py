DISEASE_INFO = {
    "healthy_basil": {
        "name": "Healthy Basil",
        "description": "No symptoms of infection or damage. All key bioactives are retained in full capacity.",
        "compounds_affected": "None",
        "properties_lost": "None",
        "properties_retained": "All retained",
        "usability": "Yes – Fully usable for all purposes",
        "medicinal_uses": [
            "Herbal teas",
            "Ayurveda and Unani medicine", 
            "Culinary use",
            "Cosmetic and essential oil extraction"
        ],
        "color": "#4CAF50",
        "severity": "none"
    },
    "downy_mildew": {
        "name": "Downy Mildew",
        "description": "Causes interveinal chlorosis, leading to yellowing of tissue and fungal spore development.",
        "compounds_affected": "Flavonoids, carotenoids",
        "properties_lost": "Antioxidant, anti-inflammatory",
        "properties_retained": "Aroma compounds (mild stages)",
        "usability": "Yes, for topical use / aroma (early only)",
        "medicinal_uses": [
            "Mild aroma-based preparations",
            "Herbal infusions (non-ingestible)",
            "Air purifiers"
        ],
        "color": "#FF9800",
        "severity": "moderate"
    },
    "fusarium_wilt": {
        "name": "Fusarium Wilt",
        "description": "Fungal invasion through roots blocks xylem vessels, disrupting nutrient flow.",
        "compounds_affected": "Eugenol, linalool, methyl chavicol",
        "properties_lost": "Antibacterial, antifungal, digestive",
        "properties_retained": "Almost none",
        "usability": "No – Unfit for any medicinal use",
        "medicinal_uses": [
            "Compost or biowaste (if completely dried and sterilized)"
        ],
        "color": "#F44336",
        "severity": "severe"
    },
    "gray_mold": {
        "name": "Gray Mold",
        "description": "Leads to soft rot and fuzzy gray fungal growth on the surface.",
        "compounds_affected": "Polyphenols, phenolic acids, tannins",
        "properties_lost": "Antioxidant, anti-aging, hepatoprotective",
        "properties_retained": "Faint smell (early stage only)",
        "usability": "Slight topical use only (early); discard later",
        "medicinal_uses": [
            "Topical balms (very early stage)",
            "Incense (non-ingestion)"
        ],
        "color": "#9C27B0",
        "severity": "severe"
    },
    "septoria_leaf_spot": {
        "name": "Septoria Leaf Spot",
        "description": "Develops brown to black necrotic spots surrounded by yellow halos.",
        "compounds_affected": "Chlorophyll, vitamin C, polyphenols",
        "properties_lost": "Immunity, rejuvenation, detoxification",
        "properties_retained": "Minor essential oils in unaffected areas",
        "usability": "Limited non-oral use (early stage only)",
        "medicinal_uses": [
            "Aromatherapy (localized spots only)",
            "Topical use (if <20% affected)"
        ],
        "color": "#795548",
        "severity": "moderate"
    }
}

def get_disease_info(disease_name):
    """Get disease information by name"""
    return DISEASE_INFO.get(disease_name.lower(), DISEASE_INFO.get("healthy_basil"))

def get_all_diseases():
    """Get all disease information"""
    return DISEASE_INFO