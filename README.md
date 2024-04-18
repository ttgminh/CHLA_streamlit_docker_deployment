# CHLA No Show Prediction App

This repository hosts a Streamlit-based web application for predicting no-show probabilities at CHLA (Children's Hospital Los Angeles). The application is containerized using Docker for easy deployment and scalability.

## Features

- Machine learning model to predict appointment no-shows.
- Streamlit interface for user interactions.
- Docker deployment for ease of use.

## Installation and Setup

1. **Build the Docker image:**
   ```bash
   docker build -t chlaprediction .
2. **Run the Application**
   ```bash
   docker run -p 8501:8501 chla-prediction

## Usage

After starting the application, access it by navigating to `http://localhost:8501` in your web browser. Through the web interface, you can:

- **Select Date Ranges:** Input start and end dates to analyze the likelihood of no-shows for appointments within that range.
- **View Predictions:** After entering the dates, the application processes the data and displays predictions of no-show probabilities.

## Future Improvements

- **Facility Selection:** Plans are in place to add a feature allowing users to select different CHLA facilities from which they want to view or analyze data. This enhancement will help in providing more tailored predictions based on specific facility characteristics and historical performance.

