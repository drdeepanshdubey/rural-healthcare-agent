"""
Urgency Assessment Tool
Determines medical urgency from symptoms
"""

def assess_urgency(symptoms: str, age: int = 30) -> dict:
    """
    Assess medical urgency based on symptoms and age
    
    Args:
        symptoms: Patient symptoms as string
        age: Patient age (default 30)
    
    Returns:
        dict with urgency_level (1-5), recommendation, and priority
    """
    
    # Critical symptoms that need immediate attention
    urgent_keywords = [
        "chest pain", "heart attack", "stroke",
        "difficulty breathing", "can't breathe", "breathless",
        "severe bleeding", "heavy bleeding",
        "unconscious", "fainted", "collapsed",
        "severe head injury", "head trauma",
        "seizure", "convulsion",
        "poisoning", "overdose",
        "severe burn", "high fever"
    ]
    
    # Moderate symptoms
    moderate_keywords = [
        "fever", "high temperature",
        "vomiting", "diarrhea",
        "severe pain", "intense pain",
        "injury", "fracture", "broken",
        "infection", "wound"
    ]
    
    # Convert to lowercase for matching
    symptoms_lower = symptoms.lower()
    
    # Default urgency
    urgency_score = 1
    reason = "General consultation recommended"
    
    # Check for critical symptoms
    for keyword in urgent_keywords:
        if keyword in symptoms_lower:
            urgency_score = 5
            reason = f"Critical: '{keyword}' detected - Emergency care needed"
            break
    
    # If not critical, check for moderate symptoms
    if urgency_score == 1:
        for keyword in moderate_keywords:
            if keyword in symptoms_lower:
                urgency_score = 3
                reason = f"Moderate: '{keyword}' detected - Medical consultation recommended"
                break
    
    # Age-based adjustments
    if age > 65 or age < 5:
        urgency_score = min(urgency_score + 1, 5)
        reason += " (Age factor: High-risk group)"
    
    # Determine priority level
    if urgency_score >= 4:
        priority = "HIGH"
        recommendation = "Seek immediate emergency care"
    elif urgency_score >= 2:
        priority = "MEDIUM"
        recommendation = "Schedule medical consultation soon"
    else:
        priority = "LOW"
        recommendation = "General consultation when convenient"
    
    return {
        "urgency_level": urgency_score,
        "priority": priority,
        "recommendation": recommendation,
        "reason": reason
    }