def apply_conditional_logic(state):
    """Applies conditional logic based on urgency and certainty."""
    urgency = state.get("urgency", "Low")
    certainty = state.get("certainty", "Low")
    if urgency == "High":
        return "Expedite treatment and specialty referral"
    if "Low" in certainty:
        return "Gather more evidence or consult additional sources"
    return "Proceed with standard treatment recommendation" 
