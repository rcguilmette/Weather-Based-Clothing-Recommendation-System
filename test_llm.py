import os
import json
import pandas as pd
from recommend import recommend_outfit

def load_test_scenarios(path):
    """Load test scenarios from JSON file"""
    with open(path, 'r') as f:
        return json.load(f)

def load_wardrobe(csv_path):
    """Load wardrobe items from CSV"""
    return pd.read_csv(csv_path).to_dict(orient='records')

def evaluate_recommendation(recommendation, weather):
    """
    Simple evaluation function - returns a score based on:
    1. Appropriate warmth for temperature
    2. Appropriate water resistance for precipitation
    3. Appropriate wind resistance for wind speed
    """
    score = 0
    max_score = 3
    
    # Check for warmth appropriateness
    if weather["temp"] > 80 and any(warm_item in recommendation.lower() for warm_item in ["light", "short", "thin", "tank top", "t-shirt", "shorts"]):
        score += 1
    elif weather["temp"] < 40 and any(cold_item in recommendation.lower() for cold_item in ["warm", "heavy", "thick", "winter", "coat", "sweater", "thermal"]):
        score += 1
    elif 40 <= weather["temp"] <= 80:
        score += 1
        
    # Check for water resistance
    if weather["precip"] > 5 and any(water_item in recommendation.lower() for water_item in ["raincoat", "umbrella", "waterproof", "rain boots", "water-resistant"]):
        score += 1
    elif weather["precip"] <= 5:
        score += 1
        
    # Check for wind resistance
    if weather["wind"] > 15 and any(wind_item in recommendation.lower() for wind_item in ["windbreaker", "wind-resistant", "heavy", "jacket", "coat"]):
        score += 1
    elif weather["wind"] <= 15:
        score += 1
        
    # Calculate percentage score
    percentage_score = (score / max_score) * 100
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": percentage_score,
        "recommendation": recommendation
    }

def main():
    # Load test data
    print("Loading test scenarios...")
    option1 = 'test_scenarios.json'
    option2 = 'test_scenariosv2.json'
    scenarios = load_test_scenarios(option2)
    
    print("Loading wardrobe items...")
    wardrobe = load_wardrobe("wardrobe.csv")
    
    # Define prompt types to test
    prompt_types = ["basic", "detailed", "feedback_focused", "comparative"]
    
    # Create results structure
    results = {
        "scenarios": [],
        "prompt_performance": {p: {"total_score": 0, "max_possible": 0} for p in prompt_types}
    }
    
    # Run tests for each scenario
    print(f"\nTesting {len(scenarios)} scenarios with {len(prompt_types)} prompt types...")
    
    for scenario in scenarios:
        print(f"\nTesting scenario {scenario['scenario_id']}: {scenario['description']}")
        print(f"Weather: Temp {scenario['weather']['temp']}°F, Wind {scenario['weather']['wind']}mph, Precipitation {scenario['weather']['precip']}mm")
        
        scenario_results = {
            "scenario_id": scenario['scenario_id'],
            "description": scenario['description'],
            "weather": scenario['weather'],
            "evaluations": {}
        }
        
        # Test each prompt type
        for prompt_type in prompt_types:
            print(f"  Testing {prompt_type} prompt...")
            
            # Get recommendation
            try:
                recommendation = recommend_outfit(
                    scenario['weather'], 
                    wardrobe, 
                    [],  # Empty feedback history for testing
                    prompt_type
                )
                
                # Evaluate recommendation
                evaluation = evaluate_recommendation(recommendation, scenario['weather'])
                scenario_results["evaluations"][prompt_type] = evaluation
                
                # Print result
                print(f"    Score: {evaluation['score']}/{evaluation['max_score']} ({evaluation['percentage']}%)")
                print(f"    Recommendation: {recommendation}")
                
                # Update totals
                results["prompt_performance"][prompt_type]["total_score"] += evaluation["score"]
                results["prompt_performance"][prompt_type]["max_possible"] += evaluation["max_score"]
                
            except Exception as e:
                print(f"    Error: {e}")
                scenario_results["evaluations"][prompt_type] = {
                    "error": str(e),
                    "score": 0,
                    "max_score": 3,
                    "percentage": 0,
                    "recommendation": ""
                }
        
        results["scenarios"].append(scenario_results)
    
    # Calculate overall performance percentages
    for prompt_name in results["prompt_performance"]:
        total = results["prompt_performance"][prompt_name]["total_score"]
        maximum = results["prompt_performance"][prompt_name]["max_possible"]
        if maximum > 0:
            percentage = (total / maximum) * 100
            results["prompt_performance"][prompt_name]["percentage"] = percentage
    
    # Save results to file
    with open("test_results{datetime.now().strftime('%Y%m%d%H%M%S')}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\nPrompt Performance Summary:")
    for prompt_name, performance in results["prompt_performance"].items():
        if "percentage" in performance:
            print(f"{prompt_name}: {performance['percentage']:.2f}%")
    
    print("\nResults saved")
    print("\nYou can now create a visualization of these results using analyze_results.py") ## TODO

if __name__ == "__main__":
    main()
