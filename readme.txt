Video Game Sales Analytics Dashboard

Video Game Sales Analytics (Project Greenlight) is a comprehensive business intelligence tool designed to analyze historical video game sales data and forecast future market trends. Built with Python, this application features a professional Tkinter Executive Dashboard that serves as a central hub for five distinct analytical modules, ranging from geospatial analysis to AI-driven predictions.

KEY FEATURES

Executive Dashboard: A modern, grid-based GUI (main.py) that acts as the central command center, offering easy access to all analysis modules with a "Business Executive" aesthetic.

Regional Analyst (Heatmap): Visualizes global sales distribution across North America, Europe, and Japan using GeoPandas. Generates a split-screen view with a dot-density map and a detailed breakdown table by genre.

Risk Manager (Scatter Plot): Analyzes the correlation between Critic Scores and Global Sales to determine the "Quality vs. Revenue" payoff. Identifies high-risk/high-reward genres versus safe bets.

Lifecycle Analyst (Line Graph): Splits console history into 4 Chronological Eras (Classics, Transition, Modern, Next-Gen). Visualizes the rise and fall of console sales lifecycles over time on a single screen.

Corporate Strategist (Bar Charts): A 4-part breakdown of Top 20 Publishers. Metrics include Efficiency (Avg Revenue/Game), Total Market Share, Critical Acclaim, and Release Volume.

Future AI Predictor (Machine Learning): Uses Linear Regression (scikit-learn) to train on historical data (2010+). Forecasts future trends for Consoles, Games, Genres, and Publishers.

TECHNOLOGIES USED

Language: Python 3.x

GUI: Tkinter (Standard Python Interface)

Data Analysis: Pandas, NumPy

Visualization: Matplotlib, Seaborn

Geospatial: GeoPandas, Shapely

Machine Learning: Scikit-Learn

INSTALLATION GUIDE

Follow these steps to set up the project locally.

Clone the Repository git clone https://github.com/your-username/video-game-sales-analytics.git cd video-game-sales-analytics

Install Dependencies This project requires several external libraries. You can install them all at once using pip.

pip install -r requirements.txt

(Note: If you are on Windows and have trouble installing geopandas, you may need to install standard binary wheels manually or use conda.)

Verify Data Ensure the dataset file "Video_Games_Sales_as_at_22_Dec_2016.csv" is located in the root directory of the project.

USAGE

To launch the Executive Dashboard, simply run the main script:

python main.py

The Dashboard window will open.

Click on any module (e.g., "1. Regional Analyst") to run that specific analysis.

The visualization window will pop up (maximized) for detailed viewing.

Close the visualization window to return to the dashboard.

PROJECT STRUCTURE

main.py: The entry point. Initializes the Tkinter GUI and dashboard logic.

heat.py: Handles geospatial data and generates the world map heatmap.

scatter.py: Generates scatter plots for Risk vs. Reward analysis.

line.py: Generates chronological line graphs for console lifecycles.

bar.py: Generates bar charts for publisher statistics.

ml_predict.py: Runs the Machine Learning model to forecast future trends.

requirements.txt: List of Python dependencies.

Video_Games_Sales_as_at_22_Dec_2016.csv: The dataset.