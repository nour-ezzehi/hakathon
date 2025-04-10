# app/data/crisis_resources.py
from langchain.text_splitter import CharacterTextSplitter
import os
from typing import Dict, List, Optional
import re

# Store resources in a global variable
_crisis_resources = None

def get_crisis_resources():
    """Get or initialize the crisis resources list"""
    global _crisis_resources
    if _crisis_resources is None:
        _crisis_resources = create_crisis_resources()
    return _crisis_resources

def create_crisis_resources():
    """Create and populate a list with crisis resources"""
    # This would ideally load from a CSV or database in production
    crisis_resources = [
        # Global Resources
        {
            "name": "National Suicide Prevention Lifeline",
            "contact": "1-800-273-8255",
            "description": "Available 24/7 for anyone in suicidal crisis or emotional distress",
            "tags": ["suicide", "crisis", "depression", "mental health", "global"]
        },
        {
            "name": "Crisis Text Line",
            "contact": "Text HOME to 741741",
            "description": "Free 24/7 text support for people in crisis",
            "tags": ["suicide", "crisis", "depression", "mental health", "text", "global"]
        },
        {
            "name": "International Association for Suicide Prevention",
            "contact": "https://www.iasp.info/resources/Crisis_Centres/",
            "description": "Global directory of crisis centers",
            "tags": ["suicide", "crisis", "international", "global", "directory"]
        },
        
        # United States Resources
        {
            "name": "Veterans Crisis Line",
            "contact": "1-800-273-8255 (Press 1)",
            "description": "Crisis support for veterans and their loved ones",
            "tags": ["veterans", "military", "united states", "us", "ptsd"]
        },
        {
            "name": "Trevor Project",
            "contact": "1-866-488-7386",
            "description": "Crisis intervention for LGBTQ+ youth",
            "tags": ["lgbtq", "youth", "teenager", "united states", "us", "identity"]
        },
        {
            "name": "SAMHSA's National Helpline",
            "contact": "1-800-662-4357",
            "description": "Treatment referral for mental health and substance use disorders",
            "tags": ["substance abuse", "addiction", "mental health", "united states", "us"]
        },
        
        # Regional Resources (US)
        {
            "name": "NYC Well",
            "contact": "1-888-NYC-WELL",
            "description": "New York City mental health support and crisis intervention",
            "tags": ["new york", "nyc", "local", "united states"]
        },
        {
            "name": "California Peer-Run Warm Line",
            "contact": "1-855-845-7415",
            "description": "Non-emergency support for California residents",
            "tags": ["california", "non-emergency", "peer support", "united states"]
        },
        {
            "name": "Chicago Crisis Line",
            "contact": "1-800-248-7475",
            "description": "Crisis intervention for Chicago residents",
            "tags": ["chicago", "illinois", "local", "united states"]
        },
        
        # International Resources
        {
            "name": "Samaritans UK",
            "contact": "116 123",
            "description": "24/7 crisis support throughout United Kingdom",
            "tags": ["uk", "united kingdom", "england", "britain", "international"]
        },
        {
            "name": "Lifeline Australia",
            "contact": "13 11 14",
            "description": "24/7 crisis support and suicide prevention in Australia",
            "tags": ["australia", "international", "suicide"]
        },
        {
            "name": "Distress Centres of Canada",
            "contact": "1-833-456-4566",
            "description": "Crisis services across Canada",
            "tags": ["canada", "international", "crisis"]
        },
    ]
    
    return crisis_resources

def get_emergency_resources() -> List[Dict]:
    """Get critical emergency resources that should always be shown in crisis situations"""
    return [
        {
            "name": "Emergency Services",
            "contact": "911 (US) or local emergency number",
            "description": "For immediate life-threatening emergencies"
        },
        {
            "name": "National Suicide Prevention Lifeline",
            "contact": "1-800-273-8255",
            "description": "Available 24/7 for anyone in suicidal crisis or emotional distress"
        }
    ]

def simple_keyword_matching(text: str, resources: List[Dict], k: int = 3) -> List[Dict]:
    """Simple keyword-based matching instead of embeddings"""
    # Extract keywords from the text
    keywords = set(re.findall(r'\b\w+\b', text.lower()))
    
    # Score resources by number of matching tags
    scored_resources = []
    for resource in resources:
        score = 0
        for tag in resource.get("tags", []):
            if any(keyword in tag.lower() for keyword in keywords):
                score += 1
        
        scored_resources.append((score, resource))
    
    # Sort by score (descending) and take top k
    scored_resources.sort(reverse=True, key=lambda x: x[0])
    return [resource for score, resource in scored_resources[:k]]

def get_resources_by_crisis_type(crisis_text: str, location: Optional[str] = None) -> List[Dict]:
    """Get crisis resources based on the nature of the crisis and optional location"""
    resources = get_crisis_resources()
    
    # Craft the search query based on available information
    search_query = crisis_text
    if location:
        search_query += " " + location
        
    # Use simple keyword matching instead of embeddings
    results = simple_keyword_matching(search_query, resources)
    
    return results