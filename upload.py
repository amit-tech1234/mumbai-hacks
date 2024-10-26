from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
from flask_cors import CORS
from LLM import generate_retention_strategy_with_context
from getRAG import *
import os
import csv
import json
import pandas as pd
from werkzeug.utils import secure_filename
import glob
from datetime import datetime

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
CORS(app)

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'This is your secret key to utilize session in Flask'

format_structure = {
  "user_id": 16,  # Use a user_id that exists in your dataset
  "user_name": "Amit",
  "location": "San Francisco",
  "cultural_interests": "Jazz, Theater",
  "language_preference":"English, Spanish",
  "email_open_rate": 12,  # Example values
  "email_click_rate": 7,
  "push_opt_in": True,
  "push_interaction_rate": 20,
  "inapp_interaction_rate": 30,
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
      ],"regional_language_content": [
        {
          "language": "English",
          "content": "Feature special Diwali movie recommendations and celebration ideas."
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
      ],"regional_language_content": [
        {
          "language": "Spanish",
          "content": "Incluye recomendaciones especiales de películas de Diwali e ideas de celebración."
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
      ],"regional_language_content": [
        {
          "language": "English",
          "content": "Feature special Diwali movie recommendations and celebration ideas."
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
      ],"regional_language_content": [
        {
          "language": "English",
          "content": "Feature special Diwali movie recommendations and celebration ideas."
        }
      ]
    }
  }
}

relevant_data = {
    "input": {
      "user_engagement": {
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
      "user_name":"Amit",
      "cultural_interests": ["Cricket", "Bollywood"],
      "location": "Los Angeles",
      "event_dates": [
        {
          "event_name": "Cricket World Cup",
          "date": "2024-10-05 to 2024-11-19"
        },
        {
          "event_name": "Diwali Celebrations",
          "date": "2024-11-11"
        },
        {
          "event_name": "Bollywood Movie Screenings",
          "date": "2024-10-20"
        },
        {
          "event_name": "Los Angeles Film Festival",
          "date": "2024-10-30"
        }
      ]
    },
    "output": {
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
  }

targetUserNew = {
        "userid": "James",
        "demographics": {
            "location": {
            "country": "USA",
            "state": "Illinois",
            "city": "Chicago",
            "time_zone": "CST"
            },
            "language_preferences": ["English"],
            "age": 33,
            "gender": "Male"
        },
        "regional_interests": ["football", "Hollywood movies"],
        "behavioral_data": {
            "engagement_frequency": {
            "daily_sessions": 0,
            "weekly_sessions": 1,
            "session_duration_avg": "4 minutes"
            },
            "channel_preferences": {
            "push_notifications": {
                "opt_in": False,
                "interaction_rate": "0"
            },
            "inapp_messages": {
                "interaction_rate": "5"
            },
            "email": {
                "open_rate": "2",
                "click_rate": "1"
            }
            }
        }
        }
# @app.route('/', methods=['GET', 'POST'])
# def uploadFile():
#     if request.method == 'POST':
#       # upload file flask
#         f = request.files.get('file')
#
#         # Extracting uploaded file name
#         data_filename = secure_filename(f.filename)
#
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'],
#                             data_filename))
#
#         session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
#
#         return render_template('index2.html')
#     return render_template("index.html")


# @app.route('/', methods=['GET', 'POST'])
# def uploadFile():
#     if request.method == 'POST':
#       # upload file flask
#         f = request.files.get('file')
#
#         # Extracting uploaded file name
#         data_filename = secure_filename(f.filename)
#
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'],
#                             data_filename))
#
#         session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
#         print(data_filename)
#
#         data = []
#         with open(data_filename, 'r') as csv_file:
#             csv_reader = csv.DictReader(csv_file)
#             for row in csv_reader:
#                 strategy = generate_retention_strategy_with_context(targetUserNew , relevant_data)
#                 data.append(strategy)
#            return jsonify({'data': data})

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # Use os.rmdir() for directories (if empty)
        except Exception as e:
            print(f'Error removing {file_path}: {e}')

@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    data = []
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')

        # Extracting uploaded file name
        #data_filename = secure_filename(f.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_filename = f"file_{timestamp}.csv"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))
        print(data_filename)
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
        print(data_filename)

         # Load user interaction data from CSV
        csv_file = "user_engagement_data.csv"  # Path to your CSV file
        test_user_data = load_user_data(csv_file)

             # Define the feature columns we want to base similarity on
        feature_columns = [
                 'email_open_rate', 'email_click_rate', 'push_opt_in',
                 'push_interaction_rate', 'inapp_interaction_rate','last_interaction_days','average_session_length' # Include only numerical fields for distance computation
             ]

#         target_user = {
#                  "user_id": 16,  # Use a user_id that exists in your dataset
#                  "location": "San Francisco",
#                  "cultural_interests": "Jazz, Theater",
#                  "email_open_rate": 12,  # Example values
#                  "email_click_rate": 7,
#                  "push_opt_in": True,
#                  "push_interaction_rate": 20,
#                  "inapp_interaction_rate": 30
#              }
        data_file_path = session.get('uploaded_data_file_path', None)
        print(data_file_path)
        userCSV = pd.read_csv(data_file_path)
        #userCSV = pd.read_csv(data_file_path)
        for index , row in userCSV.iterrows():
            #print(row.to_json())
            relevant_docs = retrieve_relevant_documents(test_user_data, row.to_json(), feature_columns, top_n=1)
            print('------------- Relevant docs ------------------')
            print(relevant_docs)
            #print('-----------------------------------------')
            strategy = generate_retention_strategy_with_context(row.to_json() , relevant_docs)
            #print(f"Recommended Retention Strategy: {strategy}")
            data.append(strategy)
        print(data)
        print('-----------------------------------------')
        return jsonify({'data': data})
    return render_template("index.html")

@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path, encoding='unicode_escape')
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',data_var=uploaded_df_html)


if __name__ == '__main__':
    app.run(debug=True)
