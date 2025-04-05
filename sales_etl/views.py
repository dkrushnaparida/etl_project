from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import connection
from .forms import SalesUploadForm
from .etl import run_etl_pipeline
from .models import SalesData


def upload_sales_data(request):
    if request.method == 'POST':
        form = SalesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            run_etl_pipeline(upload.region_a_file.path, upload.region_b_file.path)
            messages.success(request, "ETL completed successfully. You can now view the data.")
            return redirect('upload')
    else:
        form = SalesUploadForm()
    return render(request, 'sales_etl/upload.html', {'form': form})


def view_sales_data(request):
    data = SalesData.objects.all().order_by('OrderId')
    paginator = Paginator(data, 10)  # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales_etl/view_data.html', {'page_obj': page_obj})


def validation_dashboard(request):
    def run_query(sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # SQL queries for reporting
    total_records = run_query("SELECT COUNT(*) AS count FROM sales_etl_salesdata;")[0]['count']
    total_sales_by_region = run_query("SELECT region, SUM(total_sales) AS total FROM sales_etl_salesdata GROUP BY region;")
    avg_net_sale = run_query("SELECT AVG(net_sale) AS average FROM sales_etl_salesdata;")[0]['average']
    duplicates = run_query("SELECT OrderId, COUNT(*) AS count FROM sales_etl_salesdata GROUP BY OrderId HAVING count > 1;")

    context = {
        'total_records': total_records,
        'total_sales_by_region': total_sales_by_region,
        'avg_net_sale': avg_net_sale,
        'duplicates': duplicates,
    }

    return render(request, 'sales_etl/validation.html', context)
