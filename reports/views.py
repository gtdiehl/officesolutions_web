from django.http import HttpResponse, Http404
from django.shortcuts import render
import os
from datetime import date
import numpy as np

from .models import Reports
import pandas as pd


def index(request):
    context = {
        "reports": Reports.objects.all()
    }
    return render(request, "reports/index.html", context)


def report(request, report_id):
    try:
        report = Reports.objects.get(pk=report_id)
    except Reports.DoesNotExist:
        raise Http404("Report does not exist.")

    categories, values_y1, values_y2, table_content, title, template = graph(report_id)

    context = {"categories": categories, 'values_y1': values_y1, 'values_y2': values_y2, 'table_data': table_content,
               'report': report, 'title': title}
    return render(request, template, context=context)


def graph(report_num):

    xl = pd.ExcelFile(os.path.join(os.path.dirname(__file__), "data/SalesDataFull.xlsx"))
    df = xl.parse("Orders")

    if report_num == 1:
        rs = profit_of_ten_products_ave(df, 1, 2015, 1, 2015, False)
        title = "Top 10 Products"
        categories = list(rs["Product Name"])
        values_y1 = list(rs["Average Profit/Unit"])
        values_y2 = ""
        template = "reports/report.html"
    elif report_num == 2:
        rs = profit_of_ten_products_ave(df, 1, 2015, 1, 2015, True)
        title = "Bottom 10 Products"
        categories = list(rs["Product Name"])
        values_y1 = list(rs["Average Profit/Unit"])
        values_y2 = ""
        template = "reports/report.html"
    elif report_num == 3:
        rs = active_customer_report(df, 1, 2015, 1, 2015, False)
        title = "Most Profitable Customer Report"
        categories = list(rs["Customer Name"])
        values_y1 = list(rs["Profit"])
        values_y2 = list(rs["Total Num of Orders"])
        template = "reports/report_two_y_axis_2.html"
    elif report_num == 4:
        rs = active_customer_report(df, 1, 2015, 1, 2015, True)
        title = "Least Profitable Customer Report"
        categories = list(rs["Customer Name"])
        values_y1 = list(rs["Profit"])
        values_y2 = list(rs["Total Num of Orders"])
        template = "reports/report_two_y_axis_2.html"

    table_content = df.to_html(index=None)
    table_content = table_content.replace("", "")
    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    table_content = table_content.replace('border="1"', "")

    return categories, values_y1, values_y2, table_content, title, template


def profit_of_ten_products_ave(df, from_month, from_year, to_month, to_year, sort):
    fitered_orders_info = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month, to_year)

    fitered_orders_info_sum = fitered_orders_info[["Product Name", "Profit", "Quantity", "Order Date"]] \
        .groupby(["Product Name"]).sum()

    fitered_orders_info_sum = fitered_orders_info_sum.reset_index()

    fitered_orders_info_sum["Average Profit/Unit"] = fitered_orders_info_sum.loc[:, "Profit"].apply(np.float) / \
        fitered_orders_info_sum.loc[:, "Quantity"].apply(np.float)

    fitered_orders_info_sum = fitered_orders_info_sum.sort_values(by="Average Profit/Unit", ascending=sort)

    return fitered_orders_info_sum[:10]


def active_customer_report(df, from_month, from_year, to_month, to_year, sort):
    customers = df[["Order Date", "Customer Name", "Profit"]]
    filtered_customers = _filter_df_by_date(customers, "Order Date", from_month, from_year, to_month, to_year)

    unique_customer_list = filtered_customers["Customer Name"].unique()
    num_of_orders_dic = {}
    for cust in unique_customer_list:
        customer_select = filtered_customers.loc[filtered_customers["Customer Name"] == cust]
        my_len = customer_select["Customer Name"].count()
        num_of_orders_dic[cust] = my_len

    filtered_customers_sum = filtered_customers.groupby(["Customer Name"]).sum()
    filtered_customers_sum = filtered_customers_sum.reset_index()
    filtered_customers_sum['Total Num of Orders'] = filtered_customers_sum['Customer Name'].map(num_of_orders_dic)
    filtered_customers_sum = filtered_customers_sum.sort_values(by="Profit", ascending=sort)
    return filtered_customers_sum[:10]


def _filter_df_by_date(df, date_column, from_month, from_year, to_month,
                       to_year):
    if to_month == 12:
        to_month = 1
        to_year = to_year + 1
    else:
        to_month += 1

    filtered_data = df[
        (df[date_column] >= pd.Timestamp(date(from_year, from_month, 1))) &
        (df[date_column] < pd.Timestamp(date(to_year, to_month, 1)))
        ]
    return filtered_data