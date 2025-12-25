import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import sys

import heat
import scatter
import line
import bar
import ml_predict  

class GreenlightDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Project AI ANALYSIS | Executive Dashboard")
        self.root.geometry("900x700") 
        self.root.configure(bg="#f0f2f5") 

        self.df = self.load_data()

        header_frame = tk.Frame(root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(
            header_frame, 
            text="DATA ANALYSIS: EXECUTIVE OVERVIEW", 
            font=("Segoe UI", 20, "bold"), 
            bg="#2c3e50", 
            fg="white"
        )
        title_label.pack(pady=15)

        subtitle_label = tk.Label(
            header_frame, 
            text="Video Game Sales Analysis & Strategy", 
            font=("Segoe UI", 10), 
            bg="#2c3e50", 
            fg="#bdc3c7"
        )
        subtitle_label.pack(pady=(0, 10))

        content_frame = tk.Frame(root, bg="#f0f2f5")
        content_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        if self.df is None:
            err_label = tk.Label(content_frame, text="CRITICAL ERROR: Dataset not found.", fg="#c0392b", bg="#f0f2f5", font=("Segoe UI", 12, "bold"))
            err_label.pack(pady=20)
            return

        status_label = tk.Label(content_frame, text="✓ DATASET LOADED SUCCESSFULLY", fg="#27ae60", bg="#f0f2f5", font=("Segoe UI", 10, "bold"))
        status_label.pack(pady=(0, 10))

        grid_frame = tk.Frame(content_frame, bg="#f0f2f5")
        grid_frame.pack()

        modules = [
            ("REGIONAL ANALYST", lambda: self.run_module(heat.run_analysis), "#3498db", "Global Heatmap Distribution"),
            ("RISK MANAGER", lambda: self.run_module(scatter.run_analysis), "#e67e22", "Critic Score vs. Sales ROI"),
            ("LIFECYCLE ANALYST", lambda: self.run_module(line.run_analysis_wrapper), "#27ae60", "Console Lifespan Trends"),
            ("CORPORATE STRATEGIST", lambda: self.run_module(bar.run_analysis), "#9b59b6", "Publisher Performance Metrics"),
            ("FUTURE AI PREDICTOR", lambda: self.run_module(ml_predict.run_analysis), "#34495e", "ML-Based Future Trend Forecast") # <--- NEW BUTTON
        ]

        for i, (text, cmd, color, desc) in enumerate(modules):
            row = i // 2
            col = i % 2
            
            if i == 4:
                self.create_dashboard_card(grid_frame, text, cmd, color, desc, row, 0, colspan=2)
            else:
                self.create_dashboard_card(grid_frame, text, cmd, color, desc, row, col)

        footer_frame = tk.Frame(root, bg="#ecf0f1", height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        exit_btn = tk.Button(
            footer_frame, 
            text="CLOSE DASHBOARD", 
            command=root.quit, 
            font=("Segoe UI", 10, "bold"), 
            bg="#c0392b", 
            fg="white", 
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        exit_btn.pack(pady=10)

    def create_dashboard_card(self, parent, text, command, color, desc, r, c, colspan=1):
        card = tk.Frame(parent, bg="white", highlightbackground="#bdc3c7", highlightthickness=1, width=300 if colspan==1 else 630, height=90)
        
        if colspan == 2:
            card.grid(row=r, column=c, columnspan=2, padx=15, pady=10, sticky="") 
        else:
            card.grid(row=r, column=c, padx=15, pady=10, sticky="nsew")
            
        card.pack_propagate(False) 

        btn = tk.Button(
            card, 
            text=text, 
            command=command, 
            font=("Segoe UI", 12, "bold"), 
            bg=color, 
            fg="white", 
            relief="flat",
            activebackground="white",
            activeforeground=color,
            cursor="hand2"
        )
        btn.pack(fill=tk.X, ipady=5)

        desc_lbl = tk.Label(card, text=desc, font=("Segoe UI", 9, "italic"), fg="#7f8c8d", bg="white")
        desc_lbl.pack(expand=True)

    def run_module(self, analysis_func):
        if analysis_func.__name__ == 'run_analysis_wrapper':
            analysis_func(self.df, self.root)
        else:
            analysis_func(self.df)

    def load_data(self):
        csv_filename = 'Video_Games_Sales_as_at_22_Dec_2016.csv'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, csv_filename)

        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"Could not find '{csv_filename}'")
            return None
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading CSV: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = GreenlightDashboard(root)
    root.mainloop()