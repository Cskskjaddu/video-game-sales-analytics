import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings('ignore')

def run_analysis(df):
    print(">>> Initializing AI Prediction Model (Linear Regression)...")
    print("    (Training on historical data to forecast future trends...)")

    df_recent = df[df['Year_of_Release'] >= 2010].copy()
    df_recent = df_recent.dropna(subset=['Year_of_Release', 'Global_Sales'])

    def get_top_predictions(group_col, n=5):
        items = df_recent[group_col].unique()
        predictions = []

        for item in items:
            item_data = df_recent[df_recent[group_col] == item]
            
            years = item_data['Year_of_Release'].unique()
            if len(years) < 2:
                continue

            yearly_sales = item_data.groupby('Year_of_Release')['Global_Sales'].sum().reset_index()
            
            X = yearly_sales['Year_of_Release'].values.reshape(-1, 1)
            y = yearly_sales['Global_Sales'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            next_year = np.array([[yearly_sales['Year_of_Release'].max() + 1]])
            predicted_sales = model.predict(next_year)[0]
            
            if predicted_sales > 0:
                predictions.append((item, predicted_sales))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        return pd.DataFrame(predictions[:n], columns=[group_col, 'Predicted_Sales'])


    top_consoles = get_top_predictions('Platform')
    
    top_games = get_top_predictions('Name')
    
    top_genres = get_top_predictions('Genre')
    
    top_publishers = get_top_predictions('Publisher')

    root = tk.Tk()
    root.withdraw()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.destroy()

    fig, axes = plt.subplots(2, 2, figsize=(screen_w/100, screen_h/100))
    plt.subplots_adjust(wspace=0.3, hspace=0.4)
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']

    ax1 = axes[0,0]
    if not top_consoles.empty:
        ax1.bar(top_consoles['Platform'], top_consoles['Predicted_Sales'], color=colors[0])
        ax1.set_title('1. Future Console Dominance (Projected)', fontweight='bold')
        ax1.set_ylabel('Projected Annual Sales (M)')
    else:
        ax1.text(0.5, 0.5, "Insufficient Trend Data", ha='center')

    ax2 = axes[0,1]
    if not top_games.empty:
        short_names = [name[:15] + '...' if len(name) > 15 else name for name in top_games['Name']]
        ax2.bar(short_names, top_games['Predicted_Sales'], color=colors[1])
        ax2.set_title('2. Games with Highest Projected Growth', fontweight='bold')
        ax2.tick_params(axis='x', rotation=15)
    else:
        ax2.text(0.5, 0.5, "Insufficient Trend Data", ha='center')

    ax3 = axes[1,0]
    if not top_genres.empty:
        ax3.bar(top_genres['Genre'], top_genres['Predicted_Sales'], color=colors[2])
        ax3.set_title('3. Genres Predicted to Boost', fontweight='bold')
        ax3.set_ylabel('Projected Annual Sales (M)')
        ax3.tick_params(axis='x', rotation=15)
    else:
        ax3.text(0.5, 0.5, "Insufficient Trend Data", ha='center')

    ax4 = axes[1,1]
    if not top_publishers.empty:
        short_pubs = [name[:15] + '...' if len(name) > 15 else name for name in top_publishers['Publisher']]
        ax4.bar(short_pubs, top_publishers['Predicted_Sales'], color=colors[3])
        ax4.set_title('4. Most Successful Future Publishers', fontweight='bold')
        ax4.tick_params(axis='x', rotation=15)
    else:
        ax4.text(0.5, 0.5, "Insufficient Trend Data", ha='center')

    manager = plt.get_current_fig_manager()
    if hasattr(manager, 'window'):
        if hasattr(manager.window, 'state'):
            manager.window.state('zoomed')
        elif hasattr(manager.window, 'showMaximized'):
            manager.window.showMaximized()
        
        try:
            manager.window.attributes('-topmost', 1)
            manager.window.attributes('-topmost', 0)
            manager.window.focus_force()
        except:
            pass

    fig.suptitle("AI PREDICTIVE ANALYSIS: TOP 5 FUTURE TRENDS", fontsize=16, color='darkblue')
    plt.show()

if __name__ == "__main__":
    print("Please run 'main.py' to load real data.")