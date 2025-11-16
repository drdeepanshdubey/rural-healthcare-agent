"""
Basic tests for urgency assessment tool
"""
from tools.urgency_tool import UrgencyTool

def test_critical_urgency():
    """Test critical urgency detection"""
    tool = UrgencyTool()
    result = tool.assess_urgency("severe chest pain", 55)
    assert result['urgency_level'] == 5
    assert result['priority'] == "CRITICAL"
    print("✅ Critical urgency test passed")

def test_routine_urgency():
    """Test routine urgency"""
    tool = UrgencyTool()
    result = tool.assess_urgency("mild headache", 30)
    assert result['urgency_level'] <= 2
    print("✅ Routine urgency test passed")

def test_age_adjustment():
    """Test age-based risk adjustment"""
    tool = UrgencyTool()
    # Child with fever should get higher urgency
    result = tool.assess_urgency("fever", 4)
    assert result['urgency_level'] >= 3
    print("✅ Age adjustment test passed")

if __name__ == "__main__":
    test_critical_urgency()
    test_routine_urgency()
    test_age_adjustment()
    print("\n✅ All tests passed!")
