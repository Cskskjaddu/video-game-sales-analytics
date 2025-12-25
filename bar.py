import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tkinter as tk
import os

def run_analysis(df):
    df['Global_Sales'] = pd.to_numeric(df['Global_Sales'], errors='coerce')
    df['Critic_Score'] = pd.to_numeric(df['Critic_Score'], errors='coerce')

    publisher_stats = df.groupby('Publisher').agg(
        Total_Revenue=('Global_Sales', 'sum'),
        Game_Count=('Name', 'count'),
        Max_Critic_Score=('Critic_Score', 'max')
    ).reset_index()

    publisher_stats['Average_Revenue'] = publisher_stats['Total_Revenue'] / publisher_stats['Game_Count']
    top_20 = publisher_stats.sort_values('Total_Revenue', ascending=False).head(20)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plt.subplots_adjust(hspace=0.4, wspace=0.5, bottom=0.1, top=0.9, left=0.15, right=0.95)

    ax1 = axes[0, 0]
    data_1 = top_20.sort_values('Average_Revenue', ascending=False)
    sns.barplot(data=data_1, y='Publisher', x='Average_Revenue', ax=ax1, palette='viridis')
    ax1.set_title('1. Efficiency: Avg Revenue per Game', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Avg Sales ($M)')
    ax1.set_ylabel('')
    ax1.tick_params(axis='y', labelsize=8)

    ax2 = axes[0, 1]
    data_2 = top_20.sort_values('Total_Revenue', ascending=False)
    sns.barplot(data=data_2, y='Publisher', x='Total_Revenue', ax=ax2, palette='magma')
    ax2.set_title('2. Market Leaders: Total Revenue', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Total Sales ($M)')
    ax2.set_ylabel('')
    ax2.tick_params(axis='y', labelsize=8)

    ax3 = axes[1, 0]
    data_3 = top_20.sort_values('Max_Critic_Score', ascending=False)
    sns.barplot(data=data_3, y='Publisher', x='Max_Critic_Score', ax=ax3, palette='rocket')
    ax3.set_title('3. Critical Peak: Highest Game Score', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Max Critic Score')
    ax3.set_ylabel('')
    ax3.tick_params(axis='y', labelsize=8)
    ax3.set_xlim(50, 100)

    ax4 = axes[1, 1]
    data_4 = top_20.sort_values('Game_Count', ascending=False)
    sns.barplot(data=data_4, y='Publisher', x='Game_Count', ax=ax4, palette='crest')
    ax4.set_title('4. Volume: Total Games Released', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Number of Games')
    ax4.set_ylabel('')
    ax4.tick_params(axis='y', labelsize=8)

    fig.suptitle(f'Top 20 Publishers: 4-Part Analysis', fontsize=18)

    manager = plt.get_current_fig_manager()
    if hasattr(manager, 'window'):
        if hasattr(manager.window, 'state'):
            manager.window.state('zoomed')
        elif hasattr(manager.window, 'showMaximized'):
            manager.window.showMaximized()
            
        # --- NEW CODE: FORCE TO TOP ---
        try:
            manager.window.attributes('-topmost', 1)
            manager.window.attributes('-topmost', 0)
            manager.window.focus_force()
        except:
            pass
        # ------------------------------

    plt.show()

if __name__ == "__main__":
    df = pd.read_csv('Video_Games_Sales_as_at_22_Dec_2016.csv')
    run_analysis(df)