import pandas as pd
from recommend import recommend_outfit
from feedback import load_feedback, save_feedback
import os

def main():
    print("=== Wardrobe Recommender ===")
    temp_cur = input("Enter Current temperature (°F): ")
    wind_cur = input("Enter Current wind speed (mph): ")
    precip_cur = input("Enter Current precipitation (mm): ") 
    weather = {'temp': temp_cur, 'wind': wind_cur, 'precip': precip_cur}
    
    # Load wardrobe
    wardrobe = pd.read_csv('wardrobe.csv')
    

    # Load past feedback
    feedback = load_feedback("feedback.json")

    # Ask for prompt type
    test = os.environ.get('OPENAI_KEY')
    print("OpenAI Token:", test)
    print("\nPrompt types:")
    print("1. Basic (default)")
    print("2. Detailed (with attributes)")
    print("3. Feedback-focused")
    print("4. Comparative (considers multiple options)")
    prompt_choice = input("Select prompt type (1-4, default is 1): ").strip()
    
    prompt_type = "basic"  # default
    if prompt_choice == "2":
        prompt_type = "detailed"
    elif prompt_choice == "3":
        prompt_type = "feedback_focused"
    elif prompt_choice == "4":
        prompt_type = "comparative"
    
    # Get recommendation
    outfit = recommend_outfit(weather, wardrobe.to_dict(orient='records'), feedback, prompt_type)
    print("\nRecommended outfit:")
    print(outfit)

    # Record user feedback
    rating = input("\nHow was the outfit? (too cold / too hot / just right): ").strip()
    save_feedback("feedback.json", weather, outfit, rating)
    print("Thanks for your feedback!")

if __name__ == "__main__":
    main()

