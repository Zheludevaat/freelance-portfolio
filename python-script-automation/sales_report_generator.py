import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def load_sales_data(data_dir='data'):
    """Load all CSV files from the data directory and combine them into a single DataFrame"""
    all_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    df_list = []
    
    for file in all_files:
        file_path = os.path.join(data_dir, file)
        try:
            df = pd.read_csv(file_path)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if not df_list:
        raise ValueError("No valid CSV files found in data directory")
    
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def clean_data(df):
    """Clean and validate the sales data"""
    # Remove rows with missing critical data
    df = df.dropna(subset=['date', 'product', 'quantity', 'unit_price'])
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    
    # Ensure numeric values
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df = df.dropna(subset=['quantity', 'unit_price'])
    
    # Calculate total sales
    df['total_sales'] = df['quantity'] * df['unit_price']
    
    # Filter out negative or zero quantities/prices
    df = df[(df['quantity'] > 0) & (df['unit_price'] >= 0)]
    
    return df

def aggregate_monthly_sales(df):
    """Aggregate sales data by month"""
    # Extract year-month for grouping
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Group by month and sum sales
    monthly_sales = df.groupby('year_month').agg({
        'quantity': 'sum',
        'total_sales': 'sum'
    }).reset_index()
    
    # Convert year_month back to timestamp for sorting
    monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
    
    return monthly_sales

def create_charts(monthly_sales):
    """Create charts for the Excel report"""
    # Create a bar chart for monthly sales
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(monthly_sales)), monthly_sales['total_sales'], color='skyblue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales ($)')
    ax.set_title('Monthly Sales Summary')
    ax.set_xticks(range(len(monthly_sales)))
    ax.set_xticklabels(monthly_sales['year_month'], rotation=45)
    plt.tight_layout()
    
    # Save chart to file (ensure the output directory exists first)
    os.makedirs('output', exist_ok=True)
    chart_path = 'output/sales_chart.png'
    plt.savefig(chart_path)
    plt.close()
    
    return chart_path

def export_to_excel(monthly_sales, chart_path, output_path='output/sales_report.xlsx'):
    """Export the aggregated data and chart to an Excel file"""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create a Pandas Excel writer
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Write monthly sales to sheet
        monthly_sales.to_excel(writer, sheet_name='Monthly Sales', index=False)
        
        # Access the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Monthly Sales']
        
        # Add chart to worksheet
        from openpyxl.drawing.image import Image
        img = Image(chart_path)
        img.width = img.width // 2  # Scale image
        img.height = img.height // 2
        worksheet.add_image(img, 'D2')

def main():
    """Main function to run the sales report generator"""
    print("Loading sales data...")
    df = load_sales_data()
    
    print("Cleaning data...")
    df = clean_data(df)
    
    print("Aggregating monthly sales...")
    monthly_sales = aggregate_monthly_sales(df)
    
    print("Creating charts...")
    chart_path = create_charts(monthly_sales)
    
    print("Exporting to Excel...")
    export_to_excel(monthly_sales, chart_path)
    
    print("Sales report generated successfully at output/sales_report.xlsx")

if __name__ == "__main__":
    main()