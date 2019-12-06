from django.http import HttpResponse, Http404
from django.shortcuts import render
import os
from datetime import date
import numpy as np

from .models import Reports, Dashboard_Report
from reports.apps import sales_db
import pandas as pd
import math

millnames = ['', 'K', 'M', 'B', 'T']

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def index(request):
    return render(request, "reports/index.html")


def dashboard(request):

    return render(request, "reports/dashboard.html")


def dashboard_report(request, dashboard_report_id):

    input_from = request.GET.get('from').split("/")
    input_to = request.GET.get('to').split("/")

    try:
        report = Dashboard_Report.objects.get(pk=dashboard_report_id)
    except Reports.DoesNotExist:
        raise Http404("Report does not exist.")

    categories, values_y1, values_y2, values_y3, title, template, title_axis_y1, title_axis_y2, title_axis_y3, title_axis_x,\
        title_series_names = dashboard_graph(dashboard_report_id, int(input_from[0]), int(input_from[1]), int(input_to[0]), int(input_to[1]))

    context = {"categories": categories, 'values_y1': values_y1, 'values_y2': values_y2, 'values_y3': values_y3,
               'report': report, 'title': title, 'from_month': int(input_from[0]), 'from_year': int(input_from[1]),
               'to_month': int(input_to[0]), 'to_year': int(input_to[1]), 'title_axis_y1': title_axis_y1,
               'title_axis_y2': title_axis_y2, 'title_axis_y3': title_axis_y3, 'title_axis_x': title_axis_x,
               'title_series_names': title_series_names}
    return render(request, template, context=context)


def dashboard_graph(report_num, from_month, from_year, to_month, to_year):

    if report_num == 1:
        rs = profit_map(sales_db, from_month, from_year, to_month, to_year)
        title = "Profits per State"
        categories = ""
        title_axis_y1 = "Profits"
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = ""
        values_y1 = rs
        values_y2 = ""
        values_y3 = ""
        template = "reports/report_map.html"
    elif report_num == 2:
        rs = sales_map(sales_db, from_month, from_year, to_month, to_year)
        title = "Sales per State"
        categories = ""
        title_axis_y1 = "Sales"
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = ""
        values_y1 = rs
        values_y2 = ""
        values_y3 = ""
        template = "reports/report_map.html"
    elif report_num == 3:
        rs = profit_pie_chart(sales_db, from_month, from_year, to_month, to_year)
        title = "Profit by Product Category"
        categories = ""
        title_axis_y1 = ""
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = ""
        values_y1 = rs
        values_y2 = ""
        values_y3 = ""
        template = "reports/dashboard_profit_pie.html"
    elif report_num == 4:
        rs = sales_pie_chart(sales_db, from_month, from_year, to_month, to_year)
        title = "Sales by Product Category"
        categories = ""
        title_axis_y1 = ""
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = ""
        values_y1 = rs
        values_y2 = ""
        values_y3 = ""
        template = "reports/dashboard_sales_pie.html"
    elif report_num == 5:
        rs = sales_profit_table(sales_db, from_month, from_year, to_month, to_year)
        title = ""
        categories = ""
        title_axis_y1 = rs["table_values"]
        title_axis_y2 = ""
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = ""
        values_y1 = ""
        values_y2 = ""
        values_y3 = ""
        template = "reports/dashboard_table.html"
    elif report_num == 6:
        rs = sales_profit_totals(sales_db, from_month, from_year, to_month, to_year)
        title = ""
        categories = ""
        title_axis_y1 = rs["total_sales"]
        title_axis_y2 = rs["total_profit"]
        title_axis_y3 = ""
        title_axis_x = ""
        title_series_names = ""
        values_y1 = ""
        values_y2 = ""
        values_y3 = ""
        template = "reports/dashboard_totals.html"


    return categories, values_y1, values_y2, values_y3, title, template, title_axis_y1, title_axis_y2, title_axis_y3, title_axis_x,\
           title_series_names


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

    categories, values_y1, values_y2, values_y3, title, template, title_axis_y1, title_axis_y2, title_axis_y3, title_axis_x,\
        title_series_names = graph(report_id, int(input_from[0]), int(input_from[1]), int(input_to[0]), int(input_to[1]))

    context = {"categories": categories, 'values_y1': values_y1, 'values_y2': values_y2, 'values_y3': values_y3,
               'report': report, 'title': title, 'from_month': input_from[0], 'from_year': input_from[1],
               'to_month': input_to[0], 'to_year': input_to[1], 'title_axis_y1': title_axis_y1,
               'title_axis_y2': title_axis_y2, 'title_axis_y3': title_axis_y3, 'title_axis_x': title_axis_x, 'title_series_names': title_series_names}
    return render(request, template, context=context)


def graph(report_num, from_month, from_year, to_month, to_year):

    if report_num == 1:
        rs = profit_of_ten_products_ave(sales_db, from_month, from_year, to_month, to_year, False)
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
        rs = profit_of_ten_products_ave(sales_db, from_month, from_year, to_month, to_year, True)
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
        rs = active_customer_report(sales_db, from_month, from_year, to_month, to_year, False)
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
        rs = active_customer_report(sales_db, from_month, from_year, to_month, to_year, True)
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
        rs = sales_and_profits_by_region(sales_db, from_month, from_year, to_month, to_year)
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
            charts_drilldown_sub_list = discounts_by_region(sales_db, from_month, from_year, to_month, to_year)
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

    return categories, values_y1, values_y2, values_y3, title, template, title_axis_y1, title_axis_y2, title_axis_y3, title_axis_x,\
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


def profit_map(df, from_month, from_year, to_month, to_year):
    df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month,
                            to_year)

    df = df[['Region', 'State', 'Profit']]

    return df.groupby(['State']).sum().reset_index().replace(us_state_abbrev).rename(
        columns={"Profit": "value", "State": "code"}).to_json(orient='records')


def sales_map(df, from_month, from_year, to_month, to_year):
    df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month,
                            to_year)

    df = df[['Region', 'State', 'Sales']]

    return df.groupby(['State']).sum().reset_index().replace(us_state_abbrev).rename(
        columns={"Sales": "value", "State": "code"}).to_json(orient='records')


def profit_pie_chart(df, from_month, from_year, to_month, to_year):
    df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month,
                            to_year)

    df = df[["Category", "Profit"]]

    return df.groupby(["Category"]).sum().reset_index().rename(
        columns={"Category": "name", "Profit": "y"}).to_json(orient='records')


def sales_pie_chart(df, from_month, from_year, to_month, to_year):
    df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month,
                            to_year)

    df = df[["Category", "Sales"]]

    return df.groupby(["Category"]).sum().reset_index().rename(
        columns={"Category": "name", "Sales": "y"}).to_json(orient='records')


def sales_profit_table(df, from_month, from_year, to_month, to_year):
    metrics_df = _filter_df_by_date(sales_db, "Order Date", from_month, from_year, to_month, to_year)
    qty = metrics_df[['Category', 'Quantity']].groupby(['Category']).count()
    sales = metrics_df[['Category', 'Sales']].groupby(['Category']).sum()
    profit = metrics_df[['Category', 'Profit']].groupby(['Category']).sum()
    result = pd.concat([qty, sales, profit], axis=1, sort=False).reset_index()
    result['Profit Ratio'] = (result.loc[:, "Profit"] / result.loc[:, "Sales"]) * 100
    result.loc[3] = ['Total'] + [result['Quantity'].sum(), result['Sales'].sum(), result['Profit'].sum(),
                                 result['Profit Ratio'].sum()]
    result = result.round({'Profit Ratio': 1})
    result['Sales'] = result['Sales'].astype(int).apply(lambda x: "{:,}".format(x))
    result['Sales'] = '$' + result['Sales'].astype(str)

    result['Profit'] = result['Profit'].astype(int).apply(lambda x: "{:,}".format(x))
    result['Profit'] = '$' + result['Profit'].astype(str)
    result['Profit Ratio'] = result['Profit Ratio'].astype(str) + '%'
    table_values = [list(result['Category']), list(result['Quantity']), list(result['Sales']), list(result['Profit']),
                    list(result['Profit Ratio'])]

    context = {"table_values": table_values, }
    return context


def sales_profit_totals(df, from_month, from_year, to_month, to_year):
    metrics_df = _filter_df_by_date(df, "Order Date", from_month, from_year, to_month, to_year)

    total_sales = millify(metrics_df['Sales'].sum())
    total_profit = millify(metrics_df['Profit'].sum())

    context = {"total_sales": total_sales, "total_profit": total_profit,}
    return context


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


def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])