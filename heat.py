import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import numpy as np
import tkinter as tk
import geopandas as gpd
from shapely.geometry import Point

def run_analysis(df):
    print(">>> Generating World Map (Split Screen View)...")
    print("    (Generating dots for the entire world, please wait...)")
    
    df = df.dropna(subset=['Genre']).copy()
    
    all_genres = sorted(df['Genre'].unique().tolist())
    
    cmap = plt.get_cmap('tab20', len(all_genres))
    genre_colors = {genre: cmap(i) for i, genre in enumerate(all_genres)}

    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    try:
        world = gpd.read_file(url)
    except:
        print("Error: Could not download map data. Check internet connection.")
        return

    excluded_countries = ['Antarctica', 'Dem. Rep. Korea', 'North Korea']
    world = world[~world['NAME'].isin(excluded_countries)]

    na_countries = ['United States of America', 'Canada', 'Mexico']
    na_geo = world[world['NAME'].isin(na_countries)].dissolve()
    
    if 'CONTINENT' in world.columns:
        eu_geo = world[world['CONTINENT'] == 'Europe'].dissolve()
    else:
        eu_list = ['France', 'Germany', 'United Kingdom', 'Italy', 'Spain', 'Poland', 'Sweden', 
                   'Norway', 'Finland', 'Greece', 'Ireland', 'Portugal', 'Austria', 'Switzerland', 
                   'Belgium', 'Netherlands', 'Denmark', 'Russia', 'Ukraine', 'Belarus', 'Romania']
        eu_geo = world[world['NAME'].isin(eu_list)].dissolve()

    jp_geo = world[world['NAME'] == 'Japan'].dissolve()
    
    rest_of_world = world[
        (~world['NAME'].isin(na_countries)) & 
        (world['NAME'] != 'Japan') & 
        (world['CONTINENT'] != 'Europe' if 'CONTINENT' in world.columns else ~world['NAME'].isin(eu_list))
    ]
    other_geo = rest_of_world.dissolve()

    def generate_random_points(poly, num_points):
        points = []
        if poly.empty or num_points <= 0:
            return []
        minx, miny, maxx, maxy = poly.total_bounds
        geom = poly.geometry.iloc[0]
        attempts = 0
        while len(points) < num_points and attempts < num_points * 20:
            pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            if geom.contains(pnt):
                points.append([pnt.x, pnt.y])
            attempts += 1
        return np.array(points)

    
    fig, (ax_map, ax_table) = plt.subplots(
        nrows=2, 
        ncols=1, 
        figsize=(14, 10),
        gridspec_kw={'height_ratios': [1.5, 1]} 
    )
    
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

    offsets = [-360, 0, 360]
    for offset in offsets:
        shifted_world = world.copy()
        shifted_world['geometry'] = shifted_world.translate(xoff=offset)
        shifted_world.plot(ax=ax_map, color='#f0f0f0', edgecolor='#d0d0d0')

    SALES_PER_DOT = 15
    table_data = []
    cell_colors = []

    for genre in all_genres:
        genre_data = df[df['Genre'] == genre]
        
        n_na = int(genre_data['NA_Sales'].sum() / SALES_PER_DOT)
        n_eu = int(genre_data['EU_Sales'].sum() / SALES_PER_DOT)
        n_jp = int(genre_data['JP_Sales'].sum() / SALES_PER_DOT)
        n_other = int(genre_data['Other_Sales'].sum() / SALES_PER_DOT)
        
        dots_na = generate_random_points(na_geo, n_na)
        dots_eu = generate_random_points(eu_geo, n_eu)
        dots_jp = generate_random_points(jp_geo, n_jp)
        dots_other = generate_random_points(other_geo, n_other)
        
        all_dots_list = [dots_na, dots_eu, dots_jp, dots_other]
        
        for offset in offsets:
            def plot_dots(dots_array):
                if len(dots_array) > 0:
                    shifted = dots_array.copy()
                    shifted[:, 0] += offset
                    ax_map.scatter(
                        shifted[:, 0], shifted[:, 1], 
                        s=15, 
                        c=[genre_colors[genre]], 
                        alpha=0.7, 
                        edgecolors='none'
                    )
            for dots in all_dots_list:
                plot_dots(dots)

        sales_summary = {
            'North America': genre_data['NA_Sales'].sum(),
            'Europe': genre_data['EU_Sales'].sum(),
            'Japan': genre_data['JP_Sales'].sum(),
            'Rest of World': genre_data['Other_Sales'].sum()
        }
        top_region = max(sales_summary, key=sales_summary.get)
        
        table_data.append([genre, top_region])
        cell_colors.append([genre_colors[genre], 'white'])

    ax_map.set_title(f"Global Sales Distribution (1 Dot ≈ {SALES_PER_DOT}M Sales)", fontsize=16)
    ax_map.set_aspect('equal')
    ax_map.set_xlim([-180, 180])
    ax_map.set_ylim([-90, 90])
    ax_map.axis('off')

    ax_table.axis('off')
    
    the_table = ax_table.table(
        cellText=table_data,
        cellColours=cell_colors,
        colLabels=["Genre", "Most Popular Region"],
        loc='center',
        cellLoc='center'
    )
    
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.scale(1, 1.5)

    plt.tight_layout()
    print("   Insight: Top half shows Map, Bottom half shows detailed Table.")
    print("   (Close window to continue.)")
    plt.show()

if __name__ == "__main__":
    print("Please run 'main.py' to load real data.")