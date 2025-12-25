import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import tkinter as tk
import math

def run_analysis_wrapper(df, root=None):
    run_analysis(df, root)

def run_analysis(df, existing_root=None):
    print(">>> Generating Sales Timeline (Split into 4 Chronological Eras)...")
    
    df_clean = df.dropna(subset=['Year_of_Release', 'Global_Sales']).copy()
    df_clean['Year_of_Release'] = df_clean['Year_of_Release'].astype(int)
    
    platform_start_years = df_clean.groupby('Platform')['Year_of_Release'].min().sort_values()
    all_platforms_sorted = platform_start_years.index.tolist()
    
    platform_groups = np.array_split(all_platforms_sorted, 4)
    
    if existing_root:
        screen_w = existing_root.winfo_screenwidth()
        screen_h = existing_root.winfo_screenheight()
    else:
        root = tk.Tk()
        root.withdraw()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        root.destroy()
    
    fig, axes = plt.subplots(2, 2, figsize=(screen_w/100, screen_h/100), constrained_layout=True)
    axes_flat = axes.flatten() 
    
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

    titles = ["Era 1: The Classics", "Era 2: The Transition", "Era 3: Modern Gaming", "Era 4: Next Gen"]
    
    for i, platforms_in_group in enumerate(platform_groups):
        ax = axes_flat[i]
        
        group_data = df_clean[df_clean['Platform'].isin(platforms_in_group)]
        
        timeline_data = group_data.groupby(['Platform', 'Year_of_Release'])['Global_Sales'].sum().reset_index()
        
        if not timeline_data.empty:
            g_min_year = timeline_data['Year_of_Release'].min()
            g_max_year = timeline_data['Year_of_Release'].max()
            
            sns.lineplot(
                data=timeline_data, 
                x='Year_of_Release', 
                y='Global_Sales', 
                hue='Platform', 
                marker='o', 
                linewidth=2,
                palette='tab10', 
                ax=ax
            )
            
            ax.set_title(f"{titles[i]} ({g_min_year} - {g_max_year})", fontsize=14, fontweight='bold')
            ax.set_xlabel('Year', fontsize=10)
            ax.set_ylabel('Sales (Millions)', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.5)
            
            ax.set_xticks(range(g_min_year, g_max_year + 1, 2))
            ax.tick_params(axis='x', rotation=45)
            
            ax.legend(title='Platform', loc='upper right', fontsize=8)

    fig.suptitle(f'Console Lifecycles: Chronological Progression ({len(all_platforms_sorted)} Platforms)', fontsize=18)
    
    print("   Insight: Splitting into 4 graphs prevents clutter and shows the rise/fall of each generation clearly.")
    print("   (Close the graph window to continue)")
    plt.show()

if __name__ == "__main__":
    print("Please run 'main.py' to load real data.")