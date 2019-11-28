from django.http import HttpResponse, Http404
from django.shortcuts import render
import os
from datetime import date
import numpy as np

from .models import Reports
import pandas as pd


def index(request):
    return render(request, "reports/index.html")

def reports(request):
    context = {
        "reports": Reports.objects.all()
    }
    return render(request, "reports/report.html", context)

def report(request, report_id):
    try:
        report = Reports.objects.get(pk=report_id)
    except Reports.DoesNotExist:
        raise Http404("Report does not exist.")

    input_from = request.GET.get('from').split("/")
    input_to = request.GET.get('to').split("/")

    categories, values_y1, values_y2, values_y3, table_content, title, template, title_axis_y1, title_axis_y2, title_axis_y3, title_axis_x,\
        title_series_names = graph(report_id, int(input_from[0]), int(input_from[1]), int(input_to[0]), int(input_to[1]))

    context = {"categories": categories, 'values_y1': values_y1, 'values_y2': values_y2, 'values_y3': values_y3, 'table_data': table_content,
               'report': report, 'title': title, 'from_month': input_from[0], 'from_year': input_from[1],
               'to_month': input_to[0], 'to_year': input_to[1], 'title_axis_y1': title_axis_y1,
               'title_axis_y2': title_axis_y2, 'title_axis_y3': title_axis_y3, 'title_axis_x': title_axis_x, 'title_series_names': title_series_names}
    return render(request, template, context=context)


def graph(report_num, from_month, from_year, to_month, to_year):

    xl = pd.ExcelFile(os.path.join(os.path.dirname(__file__), "data/SalesDataFull.xlsx"))
    df = xl.parse("Orders")

    if report_num == 1:
        rs = profit_of_ten_products_ave(df, from_month, from_year, to_month, to_year, False)
        title = "Top 10 Products"
        categories = list(rs["Product Name"])
        title_axis_y1 = "Average Profit Per Unit ($ USD)"
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = "Product Name"
        values_y1 = list(rs["Average Profit/Unit"])
        values_y2 = ""
        values_y3 = ""
        template = "reports/report_single_column.html"
    elif report_num == 2:
        rs = profit_of_ten_products_ave(df, from_month, from_year, to_month, to_year, True)
        title = "Bottom 10 Products"
        categories = list(rs["Product Name"])
        title_axis_y1 = "Average Profit Per Unit ($ USD)"
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = "Product Name"
        values_y1 = list(rs["Average Profit/Unit"])
        values_y2 = ""
        values_y3 = ""
        template = "reports/report_single_column.html"
    elif report_num == 3:
        rs = active_customer_report(df, from_month, from_year, to_month, to_year, False)
        title = "Most Profitable Customer Report"
        categories = list(rs["Customer Name"])
        title_axis_y1 = "Profit ($ USD)"
        title_axis_y2 = "Total Number of Orders"
        title_axis_y3 = ""
        title_axis_x = "Customer Name"
        title_series_names = "Profit,Total Number of Orders"
        values_y1 = list(rs["Profit"])
        values_y2 = list(rs["Total Num of Orders"])
        values_y3 = ""
        template = "reports/report_two_y_axis.html"
    elif report_num == 4:
        rs = active_customer_report(df, from_month, from_year, to_month, to_year, True)
        title = "Least Profitable Customer Report"
        categories = list(rs["Customer Name"])
        title_axis_y1 = "Profit ($ USD)"
        title_axis_y2 = "Total Number of Orders"
        title_axis_y3 = ""
        title_axis_x = "Customer Name"
        title_series_names = "Profit,Total Number of Orders"
        values_y1 = list(rs["Profit"])
        values_y2 = list(rs["Total Num of Orders"])
        values_y3 = ""
        template = "reports/report_two_y_axis.html"
    elif report_num == 5:
        rs = sales_and_profits_by_region(df, from_month, from_year, to_month, to_year)
        title = "Sales and Profits by Region"
        categories = list(rs["Region"])
        title_axis_y1 = "Dollar Amount ($ USD)"
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = "Region"
        title_series_names = "Profit,Sales"
        values_y1 = list(rs["Profit"])
        values_y2 = list(rs["Sales"])
        values_y3 = ""
        template = "reports/report_grouped_columns.html"
    elif report_num == 6:
        discount_values, region_values, series_data, category_values, charts_drilldown_list, sub_category_values, \
            charts_drilldown_sub_list = discounts_by_region(df, from_month, from_year, to_month, to_year)
        title = "Discounts Given out by Region"
        categories = region_values
        title_axis_y1 = "Percentage of Orders"
        title_axis_y2 = category_values
        title_axis_y3 = sub_category_values
        title_axis_x = "Region"
        title_series_names = discount_values
        values_y1 = series_data
        values_y2 = charts_drilldown_list
        values_y3 = charts_drilldown_sub_list
        template = "reports/report_stacked_columns.html"

    table_content = df.to_html(index=None)
    table_content = table_content.replace("", "")
    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    table_content = table_content.replace('border="1"', "")

    return categories, values_y1, values_y2, values_y3, table_content, title, template, title_axis_y1, title_axis_y2, title_axis_y3, title_axis_x,\
           title_series_names


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


def sales_and_profits_by_region(df, from_month, from_year, to_month, to_year):
    df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month,
                            to_year)

    df = df[['Sales', 'Profit', 'Region']]
    df_groupby_sales = df.groupby(['Region']).sum()
    return df_groupby_sales.reset_index()


def discounts_by_region(df, from_month, from_year, to_month, to_year):
    df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month,
                            to_year)

    df['Discount'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['Discount']], index=df.index)

    discount_values = sorted(df['Discount'].unique(), reverse=True)
    region_values = sorted(df['Region'].unique(), reverse=True)
    category_values = sorted(df['Category'].unique(), reverse=True)
    sub_category_values = sorted(df['Sub-Category'].unique(), reverse=True)

    series_data = []
    for discount in discount_values:
        l = []
        for region in region_values:
            a = df[(df['Region'] == f'{region}')]
            a = a[(a['Discount'] == f'{discount}')]
            l.append(len(a.index))
        series_data.append(l)

    charts_drilldown_list = []

    for region in region_values:
        series_drilldown_data = []
        z = df[(df['Region'] == f"{region}")]
        for discount in discount_values:
            l = []
            for category in category_values:
                a = z[(z['Category'] == f'{category}')]
                a = a[(a['Discount'] == f'{discount}')]
                l.append(len(a.index))
            series_drilldown_data.append(l)
        charts_drilldown_list.append(series_drilldown_data)

    charts_drilldown_sub_list = []

    for region in region_values:
        series_drilldown_sub_data = []
        z = df[(df['Region'] == f"{region}")]
        for discount in discount_values:
            l = []
            for sub_category in sub_category_values:
                a = z[(z['Sub-Category'] == f'{sub_category}')]
                a = a[(a['Discount'] == f'{discount}')]
                l.append(len(a.index))
            series_drilldown_sub_data.append(l)
        charts_drilldown_sub_list.append(series_drilldown_sub_data)

    return discount_values, region_values, series_data, category_values, charts_drilldown_list, sub_category_values, charts_drilldown_sub_list


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