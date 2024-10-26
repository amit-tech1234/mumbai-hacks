import json
import openai
import os

from getRAG import load_user_data , retrieve_relevant_documents

# Constants
API_KEY = '<APIKEY>'  # Replace with your actual API key
BASE_URL = "https://api.groq.com/openai/v1"

# Initialize OpenAI client
client = openai.OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

def generate_retention_strategy_with_context(user_data, relevant_docs):
    context_data = {
        "user_data": user_data,
        "similar_profiles": relevant_docs.to_dict(orient='records')
    }
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f"Using the following user data and similar profiles, suggest a retention strategy: {json.dumps(context_data)}, calculate the churn status with reason based on last_interaction_days & average_session_length,along with user details also add regional_language_content translated based on user's language_preference including all channels"
            },
            {
                "role": "user",
                "content": f"Provide a retention strategy in this desired JSON format in user's first and second language both.{json.dumps(format_structure)} , Provide only the output in valid JSON format with no additional commentary with balanced parenthesis"
            }
        ],
        response_format = {"type": "json_object"},
        stream=False,
    )

    if response and response.choices:
        raw_response = response.choices[0].message.content
    try:
        json_response = json.loads(raw_response)
        return json_response
    except json.JSONDecodeError:
        return json.loads(jsonresponse)
        return None
    else:
        print("Failed to generate retention strategy.")
        return None


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0,)
    return response.choices[0].message["content"]

# Main function
def main():
 # Load user interaction data from CSV
    csv_file = "user_engagement_data.csv"  # Path to your CSV file
    user_data = load_user_data(csv_file)

    # Define the feature columns we want to base similarity on
    feature_columns = [
        'email_open_rate', 'email_click_rate', 'push_opt_in',
        'push_interaction_rate', 'inapp_interaction_rate' # Include only numerical fields for distance computation
    ]

    target_user = {
        "user_id": 16,  # Use a user_id that exists in your dataset
        "location": "San Francisco",
        "cultural_interests": "Jazz, Theater",
        "email_open_rate": 12,  # Example values
        "email_click_rate": 7,
        "push_opt_in": True,
        "push_interaction_rate": 20,
        "inapp_interaction_rate": 30
    }

    relevant_docs = retrieve_relevant_documents(user_data, target_user, feature_columns, top_n=2)
    strategy = generate_retention_strategy_with_context(target_user , relevant_docs)
    print(f"Recommended Retention Strategy: {strategy}")

if __name__ == "__main__":
    main()