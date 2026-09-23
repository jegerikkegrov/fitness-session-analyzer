

from main import analyze_session

result = analyze_session("resting")
assert result["classification"] == "resting"
print("resting test passed")


result = analyze_session("moderate_activity")
assert result["classification"] == "moderate activity"
print("Moderate test passed")

result = analyze_session("high_activity")
assert result["classification"] == "high activity"
print("High test passed")

result = analyze_session("recovery")
assert result["classification"] == "recovering"
print("Recovery test passed")

result = analyze_session("poor_quality")
assert result["classification"] == "insufficient data"
print("Poor quality test passed")