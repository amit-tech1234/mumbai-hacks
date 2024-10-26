import json
import openai
import os

from RAG import load_user_data , retrieve_relevant_documents

# Constants
API_KEY = '<APIKEY>'  # Replace with your actual API key
BASE_URL = "https://api.groq.com/openai/v1"

# Initialize OpenAI client
client = openai.OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


format_structure = {
  "churn_status": {
    "risk": "Medium",
    "email_engagement": {
      "open_rate": "10",
      "click_rate": "5"
    },
    "push_notification_engagement": {
      "opt_in": True,
      "interaction_rate": "15"
    },
    "inapp_message_engagement": {
      "interaction_rate": "25"
    }
  },
  "churn_reasons": [
    "Low engagement with emails and push notifications may lead to reduced interest.",
    "Content across channels may not align with current user interests.",
    "Insufficiently tailored notifications and messages.",
    "Lack of timely relevance to user's cultural interests."
  ],
  "retention_strategies": {
    "email": {
      "why": "Low open and click rates suggest a need for more relevant and engaging content.",
      "how": [
        "Segment email lists based on user interests in cricket and Bollywood.",
        "Create dynamic content that highlights upcoming events in Los Angeles.",
        "Run targeted re-engagement campaigns."
      ],
      "what": [
        "Focus on upcoming cricket matches and Bollywood movie releases.",
        "Use engaging subject lines and visuals."
      ],
      "when": "Send emails during late afternoons or weekends when users are more likely to engage.",
      "cultural_based_content": [
        {
          "event_name": "Diwali Celebrations",
          "date": "2024-11-11",
          "content": "Feature special Diwali movie recommendations and celebration ideas."
        },
        {
          "event_name": "Bollywood Movie Screenings",
          "date": "2024-10-20",
          "content": "Notify users about local screenings of new Bollywood releases."
        }
      ]
    },
    "push_notifications": {
      "why": "Moderate opt-in but low interaction shows the potential for improvement.",
      "how": [
        "Send notifications about upcoming cricket matches and Bollywood movie releases.",
        "Incorporate multimedia content in notifications to boost engagement.",
        "Offer exclusive deals for interactions through notifications."
      ],
      "what": [
        "Share personalized updates, movie trailers, and match highlights.",
        "Prompt user interaction through polls or votes."
      ],
      "when": "Send notifications shortly before significant events, like match days or movie releases.",
      "cultural_based_content": [
        {
          "event_name": "Cricket World Cup",
          "date": "2024-10-05 to 2024-11-19",
          "content": "Provide live updates, match schedules, and exclusive behind-the-scenes content."
        },
        {
          "event_name": "Los Angeles Film Festival",
          "date": "2024-10-30",
          "content": "Invite users to local film festival events and screenings."
        }
      ]
    },
    "sms": {
      "why": "SMS provides a direct channel for urgent or time-sensitive updates.",
      "how": [
        "Send alerts about cricket match results and Bollywood news.",
        "Use SMS for exclusive promotions or reminders."
      ],
      "what": [
        "Compose brief messages with clear calls to action.",
        "Highlight local events and screenings in Los Angeles."
      ],
      "when": "Send SMS notifications leading up to critical events or during live matches.",
      "cultural_based_content": [
        {
          "event_name": "Diwali Festivities",
          "date": "2024-11-11",
          "content": "Share ideas for celebrating Diwali, including movie recommendations."
        }
      ]
    },
    "whatsapp": {
      "why": "WhatsApp is a popular platform that enhances user engagement and direct communication.",
      "how": [
        "Utilize WhatsApp for personalized updates and reminders.",
        "Share multimedia content, including trailers and highlights."
      ],
      "what": [
        "Engage users with updates about local events and movie screenings."
      ],
      "when": "Send messages leading up to significant events or during live matches.",
      "cultural_based_content": [
        {
          "event_name": "Bollywood Movie Releases",
          "date": "2024-10-20",
          "content": "Notify users about premieres and provide ticket offers."
        }
      ]
    }
  }
}


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