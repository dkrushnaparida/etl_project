import pandas as pd
from .models import SalesData

def run_etl_pipeline(file_path_a, file_path_b):

    # Load CSVs
    df_a = pd.read_csv(file_path_a)
    df_b = pd.read_csv(file_path_b)

    # Assign region labels
    df_a['region'] = 'A'
    df_b['region'] = 'B'


    df = pd.concat([df_a, df_b], ignore_index=True)

    # Normalize columns: strip whitespace + lowercase
    df.columns = df.columns.str.strip().str.lower()

    df['quantityordered'] = pd.to_numeric(df['quantityordered'].astype(str).str.strip(), errors='coerce')
    df['itemprice'] = pd.to_numeric(df['itemprice'].astype(str).str.strip(), errors='coerce')
    df['promotiondiscount'] = pd.to_numeric(df['promotiondiscount'].astype(str).str.strip(), errors='coerce').fillna(0.0)

    # Drop invalid rows
    df.dropna(subset=['quantityordered', 'itemprice'], inplace=True)

    # Calculate totals
    df['total_sales'] = df['quantityordered'] * df['itemprice']
    df.drop_duplicates(subset='orderid', keep='first', inplace=True)
    df['net_sale'] = df['total_sales'] - df['promotiondiscount']
    df = df[df['net_sale'] > 0]

    # Clear existing records
    SalesData.objects.all().delete()

    # Insert to DB
    objects = [
        SalesData(
            OrderId=row['orderid'],
            OrderItemId=row['orderitemid'],
            QuantityOrdered=int(row['quantityordered']),
            ItemPrice=float(row['itemprice']),
            PromotionDiscount=float(row['promotiondiscount']),
            total_sales=float(row['total_sales']),
            net_sale=float(row['net_sale']),
            region=row['region']
        )
        for _, row in df.iterrows()
    ]

    SalesData.objects.bulk_create(objects, batch_size=1000)

