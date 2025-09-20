# recommend.py

# Read authentication keys from environmental variables
import os
from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()

# Define different prompt templates
def basic_prompt(weather, wardrobe_items, feedback_history):
    """
    The original basic prompt you're currently using
    """
    return f"""
You are a wardrobe assistant.
Today's weather:
- Temperature: {weather['temp']} °F
- Wind Speed: {weather['wind']} mph
- Precipitation: {weather['precip']} mm
User wardrobe items:
{[item['item_name'] for item in wardrobe_items]}
Past feedback:
{feedback_history[-3:] if feedback_history else "No feedback yet."}
Recommend an outfit that suits the weather and learns from past feedback.
Respond in 1-2 sentences.
"""

def detailed_prompt(weather, wardrobe_items, feedback_history):
    """
    A detailed prompt that includes all attributes and more guidance
    """
    # Group items by type for better organization
    outerwear = [item for item in wardrobe_items if item['type'] == 'outerwear']
    tops = [item for item in wardrobe_items if item['type'] == 'top']
    bottoms = [item for item in wardrobe_items if item['type'] == 'bottom']
    dresses = [item for item in wardrobe_items if item['type'] == 'dress']
    footwear = [item for item in wardrobe_items if item['type'] == 'footwear']
    accessories = [item for item in wardrobe_items if item['type'] == 'accessory']
    
    return f"""
You are a wardrobe assistant recommending clothes based on weather conditions.
Today's weather:
- Temperature: {weather['temp']} °F
- Wind Speed: {weather['wind']} mph
- Precipitation: {weather['precip']} mm

Available clothing with ratings (warmth 1-5, water resistance 1-5, wind resistance 1-5):

OUTERWEAR:
{['- ' + item['item_name'] + f" (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in outerwear]}

TOPS:
{['- ' + item['item_name'] + f" (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in tops]}

BOTTOMS:
{['- ' + item['item_name'] + f" (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in bottoms]}

DRESSES:
{['- ' + item['item_name'] + f" (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in dresses]}

FOOTWEAR:
{['- ' + item['item_name'] + f" (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in footwear]}

ACCESSORIES:
{['- ' + item['item_name'] + f" (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in accessories]}

Past feedback:
{feedback_history[-3:] if feedback_history else "No feedback yet."}

Guidelines:
- For temperatures above 80°F, prioritize light, breathable clothing
- For temperatures below 40°F, prioritize warm layers
- For precipitation above 5mm, include water-resistant items
- For wind speeds above 15mph, include wind-resistant items

Recommend a complete outfit that includes at least one top, one bottom (or dress), footwear, and any appropriate accessories or outerwear.
Respond in 1-2 sentences.
"""

def feedback_focused_prompt(weather, wardrobe_items, feedback_history):
    """
    A prompt that puts more emphasis on past feedback
    """
    return f"""
You are a wardrobe assistant who learns from feedback.
Today's weather:
- Temperature: {weather['temp']} °F
- Wind Speed: {weather['wind']} mph
- Precipitation: {weather['precip']} mm

User wardrobe items:
{[item['item_name'] for item in wardrobe_items]}

Past feedback (IMPORTANT - Learn from this!):
{feedback_history if feedback_history else "No feedback yet."}

Based on the feedback history, recommend an outfit that will not be too hot or too cold for today's weather. The user's comfort is the top priority. Include at least one top, one bottom (or dress), and any appropriate accessories or footwear.
Respond in 1-2 sentences.
"""

def comparative_prompt(weather, wardrobe_items, feedback_history):
    """
    A prompt that asks the model to consider multiple options
    """
    return f"""
You are a wardrobe assistant.
Today's weather:
- Temperature: {weather['temp']} °F
- Wind Speed: {weather['wind']} mph
- Precipitation: {weather['precip']} mm

User wardrobe items:
{[f"{item['item_name']} (warmth: {item['warmth_rating']}, water: {item['water_resistance']}, wind: {item['wind_resistance']})" for item in wardrobe_items]}

Past feedback:
{feedback_history[-3:] if feedback_history else "No feedback yet."}

First, consider 2-3 different outfit combinations that might work for today's weather.
Then, select the best one based on warmth, water resistance, wind resistance, and past feedback.
Recommend one complete outfit that includes at least one top, one bottom (or dress), footwear, and any appropriate accessories or outerwear.
Respond in 1-2 sentences.
"""

def recommend_outfit(weather, wardrobe_items, feedback_history, prompt_type="basic"):
    # Load environment variables
    _open_ai_tkn = os.environ.get('OPENAI_KEY')

    # Create OpenAI client
    client = OpenAI(
        api_key=_open_ai_tkn
    )

    # Select the appropriate prompt based on prompt_type
    prompt_functions = {
        "basic": basic_prompt,
        "detailed": detailed_prompt,
        "feedback_focused": feedback_focused_prompt,
        "comparative": comparative_prompt
    }
    
    prompt_function = prompt_functions.get(prompt_type, basic_prompt)
    prompt = prompt_function(weather, wardrobe_items, feedback_history)
    
    # Make request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        
        messages=[{
            "role": "user",
            "instructions": "You are a wardrobe/clothing recommender assistant.",
            "content": prompt
        }],
        max_completion_tokens=100,
        temperature=1,
        top_p= 1.00
    )
    # print(response) # for debugging
    
    return response.choices[0].message.content


