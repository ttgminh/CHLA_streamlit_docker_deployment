import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
import pickle
from datetime import datetime
import warnings

# Ignore all warnings
warnings.filterwarnings('ignore')

# Load the predictor model from a pickle file
model = pickle.load(open('model.pkl', 'rb'))

# Load the encoder dictionary from a pickle file
with open('label_encoder.pkl', 'rb') as pkl_file:
    encoder_dict = pickle.load(pkl_file)

def encode_features(df, encoder_dict):
    # For each categorical feature, apply the encoding
    category_col = ['APPT_TYPE_STANDARDIZE']
    for col in category_col:
        if col in encoder_dict:
            classes = encoder_dict[col]
            # Convert the column to the encoded values
            df[col] = df[col].apply(lambda x: classes.index(x) if x in classes else -1)
            # If there's a category that is not in the encoder_dict, you can assign it a default value or handle it differently

    return df

def main():
    st.title("CHLA Predictor")
    html_temp = """
    <div style="background:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">CHLA No Show Predictor App </h2>
    </div>
    """

    # Bringing in CHLA data
    reference_df = pd.read_csv('CHLA_clean_data_until_2023.csv')
    reference_df['APPT_DATE'] = pd.to_datetime(reference_df['APPT_DATE'])

    max_df_date = max(reference_df['APPT_DATE'])
    min_df_date = min(reference_df['APPT_DATE'])

    st.markdown(html_temp, unsafe_allow_html = True)

    START_DATE  = st.date_input("Start date", 
                           value=None, 
                           min_value=min_df_date, 
                           max_value=max_df_date, 
                           key="start_date")
    END_DATE  = st.date_input("End date", 
                           value=None, 
                           min_value=pd.Timestamp(START_DATE) if START_DATE else min_df_date, 
                           max_value=max_df_date, 
                           key="end_date")

    if st.button("Predict"):
        
        # Formatting Date Inputs as Datetime objects
        start_date_timestamp = pd.Timestamp(START_DATE)
        end_date_timestamp = pd.Timestamp(END_DATE)

        # Filtering data based on date inputs
        output_df_all = reference_df[(reference_df['APPT_DATE'] >= start_date_timestamp) & (reference_df['APPT_DATE'] <= end_date_timestamp)]
        output_df = output_df_all[['LEAD_TIME', 'APPT_TYPE_STANDARDIZE', 'APPT_NUM', 'TOTAL_NUMBER_OF_CANCELLATIONS', 'TOTAL_NUMBER_OF_NOT_CHECKOUT_APPOINTMENT', 'TOTAL_NUMBER_OF_SUCCESS_APPOINTMENT', 'DAY_OF_WEEK', 'AGE']]

        # Encoding features from encoded dataset
        df = encode_features(output_df, encoder_dict)
        features_list = df.values

        # Generating predictions from model
        prediction = model.predict(features_list)
        output_df_all['PREDICTION'] = prediction
        output_df_all['MRN'] = output_df_all['MRN'].astype(str)

        # Output df
        st.write(output_df_all[['MRN', 'APPT_DATE', 'PREDICTION']])


if __name__ == '__main__':
    main()
