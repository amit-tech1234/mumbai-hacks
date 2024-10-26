import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import euclidean_distances

# Load CSV data into a pandas DataFrame
def load_user_data(csv_file):
    return pd.read_csv(csv_file)

# Normalize the features to ensure fair distance computation
def normalize_data(df, feature_columns):
    df_norm = df.copy()
    # Normalize only the numerical features
    df_norm[feature_columns] = (df[feature_columns] - df[feature_columns].mean()) / df[feature_columns].std()
    return df_norm

# Compute Euclidean distance between the target user and all other users
def compute_similarity(df, target_user, feature_columns, top_n=5):

    if isinstance(target_user, str):
     target_user = json.loads(target_user)
    # Convert the target_user dictionary to a DataFrame with one row
    target_user_df = pd.DataFrame([target_user])
    print(target_user_df)

    # Extract target user's features and reshape them for distance calculation
    target_features = target_user_df[feature_columns].values.reshape(1, -1)

    # Compute the distance between the target user and all other users
    distances = euclidean_distances(df[feature_columns], target_features)

    # Add the distances to the DataFrame
    df['distance'] = distances

    # print(df.nsmallest(top_n, 'distance'))
    # Return the top N most similar users (excluding the target user)
    return df.nsmallest(top_n, 'distance')

# Example function to retrieve relevant documents based on a target user
def retrieve_relevant_documents(df, target_user, feature_columns, top_n=5):
    df_norm = normalize_data(df, feature_columns)
    similar_users = compute_similarity(df_norm, target_user, feature_columns, top_n)
    # print(similar_users)
    return similar_users

# Main function
if __name__ == "__main__":
    # Load user interaction data from CSV
    csv_file = "test-data.csv"  # Path to your CSV file
    user_data = load_user_data(csv_file)

    # Define the feature columns we want to base similarity on
    feature_columns = [
        'email_open_rate', 'email_click_rate', 'push_opt_in',
        'push_interaction_rate', 'inapp_interaction_rate',
        'churn_risk'  # Include only numerical fields for distance computation
    ]

    # Define a sample target user
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

    # Retrieve relevant documents based on the target user
    relevant_docs = retrieve_relevant_documents(user_data, target_user, feature_columns, top_n=5)

    # Print the retrieved relevant documents (similar user profiles)
    print(relevant_docs)