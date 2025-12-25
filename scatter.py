import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import tkinter as tk

def run_analysis(df):
    print(">>> Generating Risk Assessment Scatter Plot (All Genres)...")
    
    df_scored = df.dropna(subset=['Critic_Score', 'Global_Sales']).copy()
    
    df_scored['Critic_Score'] = pd.to_numeric(df_scored['Critic_Score'], errors='coerce')
    
    genre_stats = df_scored.groupby('Genre').agg({
        'Critic_Score': 'mean',
        'Global_Sales': 'mean'
    }).reset_index()
    
    print(f"    Plotting {len(genre_stats)} genres...")
    
    plt.figure(figsize=(12, 8)) 
    
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
    sns.scatterplot(
        data=genre_stats, 
        x='Critic_Score', 
        y='Global_Sales', 
        s=150, 
        color='#ff7f50', 
        edgecolor='black',
        alpha=0.8
    )
    
    for i in range(len(genre_stats)):
        plt.text(
            genre_stats.iloc[i]['Critic_Score'] + 0.2, 
            genre_stats.iloc[i]['Global_Sales'], 
            genre_stats.iloc[i]['Genre'], 
            fontsize=10, 
            weight='bold',
            va='center' 
        )
        
    plt.title('Risk Assessment: Critical Praise vs. Financial Return (All Genres)', fontsize=16)
    plt.xlabel('Average Critic Score (Quality)', fontsize=12)
    plt.ylabel('Average Global Sales (Revenue in Millions)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.5)
    
    print("   Insight: Visualizing the relationship between critical reception and sales across all genres.")
    print("   (Close the graph window to continue)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Please run 'main.py' to load real data.")