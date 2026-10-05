import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# SAMPLE DATA
# ============================================================

sample_data = {
    "Date": [
        "2026-01-05",
        "2026-01-10",
        "2026-01-15",
        "2026-02-03",
        "2026-02-12",
        "2026-02-20",
        "2026-03-02",
        "2026-03-15",
        "2026-03-25",
        "2026-04-05",
        "2026-04-18",
        "2026-04-28",
        "2026-05-08",
        "2026-05-19",
        "2026-05-30",
        "2026-06-07",
        "2026-06-18",
        "2026-06-29",
        "2026-07-10",
        "2026-07-22",
    ],

    "Product": [
        "Laptop",
        "Monitor",
        "Keyboard",
        "Mouse",
        "Laptop",
        "Monitor",
        "Keyboard",
        "Mouse",
        "Laptop",
        "Monitor",
        "Keyboard",
        "Mouse",
        "Laptop",
        "Monitor",
        "Keyboard",
        "Mouse",
        "Laptop",
        "Monitor",
        "Keyboard",
        "Laptop",
    ],

    "Category": [
        "Electronics",
        "Electronics",
        "Accessories",
        "Accessories",
        "Electronics",
        "Electronics",
        "Accessories",
        "Accessories",
        "Electronics",
        "Electronics",
        "Accessories",
        "Accessories",
        "Electronics",
        "Electronics",
        "Accessories",
        "Accessories",
        "Electronics",
        "Electronics",
        "Accessories",
        "Electronics",
    ],

    "Region": [
        "Nairobi",
        "Mombasa",
        "Nairobi",
        "Kisumu",
        "Mombasa",
        "Nairobi",
        "Kisumu",
        "Nairobi",
        "Mombasa",
        "Nairobi",
        "Kisumu",
        "Mombasa",
        "Nairobi",
        "Mombasa",
        "Nairobi",
        "Kisumu",
        "Mombasa",
        "Nairobi",
        "Kisumu",
        "Mombasa",
    ],

    "Sales": [
        120000,
        75000,
        15000,
        8000,
        135000,
        82000,
        18000,
        9000,
        145000,
        88000,
        17000,
        11000,
        155000,
        95000,
        22000,
        12000,
        140000,
        105000,
        25000,
        13000,
    ],

    "Profit": [
        30000,
        18000,
        5000,
        2500,
        35000,
        20000,
        6000,
        3000,
        38000,
        22000,
        5500,
        3500,
        42000,
        24000,
        7000,
        4000,
        36000,
        27000,
        8000,
        4500,
    ]
}


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Sales Performance Dashboard")

st.caption(
    "Interactive business intelligence dashboard built with "
    "Python, Pandas, Plotly and Streamlit"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Dashboard Controls")


# ============================================================
# FILE UPLOAD
# ============================================================

st.sidebar.subheader("📁 Data Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"],
    help="Upload a sales dataset containing Date, Product, Category, Region, Sales and Profit."
)


# ============================================================
# LOAD DATA
# ============================================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.lower().endswith(".xlsx"):

            df = pd.read_excel(uploaded_file)

        else:

            st.error("Unsupported file type.")
            st.stop()

    except Exception as error:

        st.error(
            f"Could not read the uploaded file: {error}"
        )

        st.stop()

    data_source_name = uploaded_file.name

else:

    df = pd.DataFrame(sample_data)

    data_source_name = "Sample data"


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Date",
    "Product",
    "Category",
    "Region",
    "Sales",
    "Profit"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error(
        "The uploaded file is missing required columns:"
    )

    st.write(missing_columns)

    st.info(
        "Required columns: "
        + ", ".join(required_columns)
    )

    st.stop()


# ============================================================
# ORIGINAL ROW COUNT
# ============================================================

original_rows = len(df)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

duplicate_rows = df.duplicated().sum()

df = df.drop_duplicates().copy()


# ============================================================
# CLEAN DATE COLUMN
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)


# ============================================================
# CLEAN NUMERIC COLUMNS
# ============================================================

df["Sales"] = pd.to_numeric(
    df["Sales"],
    errors="coerce"
)

df["Profit"] = pd.to_numeric(
    df["Profit"],
    errors="coerce"
)


# ============================================================
# REMOVE INVALID REQUIRED ROWS
# ============================================================

invalid_rows = df[
    df["Date"].isna()
    | df["Sales"].isna()
    | df["Profit"].isna()
].shape[0]


df = df.dropna(
    subset=[
        "Date",
        "Sales",
        "Profit"
    ]
).copy()


# ============================================================
# HANDLE TEXT MISSING VALUES
# ============================================================

for column in [
    "Product",
    "Category",
    "Region"
]:

    df[column] = (
        df[column]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )


# ============================================================
# HANDLE NEGATIVE SALES / PROFIT
# ============================================================

negative_sales_rows = (
    df["Sales"] < 0
).sum()


# ============================================================
# DATA QUALITY SUMMARY
# ============================================================

cleaned_rows = len(df)

rows_removed = original_rows - cleaned_rows


# ============================================================
# DATA SOURCE STATUS
# ============================================================

if uploaded_file is not None:

    st.success(
        f"Successfully loaded: {data_source_name}"
    )

else:

    st.info(
        "Using sample data. Upload a CSV or Excel file from the sidebar to analyze your own data."
    )


# ============================================================
# DATA QUALITY EXPANDER
# ============================================================

with st.expander("🔎 Data Quality Summary"):

    quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)

    with quality_col1:

        st.metric(
            "Original Rows",
            f"{original_rows:,}"
        )

    with quality_col2:

        st.metric(
            "Clean Rows",
            f"{cleaned_rows:,}"
        )

    with quality_col3:

        st.metric(
            "Duplicates Removed",
            f"{duplicate_rows:,}"
        )

    with quality_col4:

        st.metric(
            "Invalid Rows Removed",
            f"{invalid_rows:,}"
        )

    if negative_sales_rows > 0:

        st.warning(
            f"{negative_sales_rows} row(s) contain negative sales values. "
            "These may represent refunds or returns."
        )

    if rows_removed > 0:

        st.info(
            f"{rows_removed} row(s) were removed during data cleaning."
        )

    else:

        st.success(
            "No rows were removed during data cleaning."
        )


# ============================================================
# CHECK IF DATA IS EMPTY
# ============================================================

if df.empty:

    st.error(
        "There is no usable data after cleaning."
    )

    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("🎯 Filters")


# ============================================================
# DATE FILTER
# ============================================================

minimum_date = df["Date"].min().date()

maximum_date = df["Date"].max().date()


date_range = st.sidebar.date_input(
    "Date Range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)


# ============================================================
# REGION FILTER
# ============================================================

region_options = sorted(
    df["Region"].dropna().unique()
)


selected_regions = st.sidebar.multiselect(
    "Region",
    options=region_options,
    default=region_options
)


# ============================================================
# CATEGORY FILTER
# ============================================================

category_options = sorted(
    df["Category"].dropna().unique()
)


selected_categories = st.sidebar.multiselect(
    "Category",
    options=category_options,
    default=category_options
)


# ============================================================
# PRODUCT FILTER
# ============================================================

product_options = sorted(
    df["Product"].dropna().unique()
)


selected_products = st.sidebar.multiselect(
    "Product",
    options=product_options,
    default=product_options
)


# ============================================================
# APPLY DATE FILTER
# ============================================================

if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

else:

    start_date = pd.Timestamp(
        minimum_date
    )

    end_date = pd.Timestamp(
        maximum_date
    )


# ============================================================
# APPLY ALL FILTERS
# ============================================================

filtered_df = df[
    (df["Date"] >= start_date)
    & (df["Date"] <= end_date)
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Product"].isin(selected_products))
].copy()


# ============================================================
# NO FILTERED DATA
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data matches the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = len(filtered_df)

total_products = filtered_df["Product"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


# ============================================================
# HEADER
# ============================================================

st.subheader("📈 Business Overview")


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.metric(
        "Total Sales",
        f"KSh {total_sales:,.0f}"
    )


with col2:

    st.metric(
        "Total Profit",
        f"KSh {total_profit:,.0f}"
    )


with col3:

    st.metric(
        "Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "Products",
        f"{total_products:,}"
    )


with col5:

    st.metric(
        "Profit Margin",
        f"{profit_margin:.1f}%"
    )


with col6:

    st.metric(
        "Avg. Order Value",
        f"KSh {average_order_value:,.0f}"
    )


st.divider()


# ============================================================
# SALES BY REGION
# ============================================================

region_sales = (
    filtered_df
    .groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region",
    text_auto=".2s"
)


fig_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Sales (KSh)",
    hovermode="x unified"
)


st.plotly_chart(
    fig_region,
    use_container_width=True
)


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# SALES BY CATEGORY
# ============================================================

with col1:

    category_sales = (
        filtered_df
        .groupby(
            "Category",
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )


    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
        hole=0.45
    )


    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ============================================================
# PROFIT BY CATEGORY
# ============================================================

with col2:

    category_profit = (
        filtered_df
        .groupby(
            "Category",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
    )


    fig_profit_category = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        title="Profit by Category",
        text_auto=".2s"
    )


    fig_profit_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Profit (KSh)"
    )


    st.plotly_chart(
        fig_profit_category,
        use_container_width=True
    )


# ============================================================
# SALES TREND
# ============================================================

st.subheader("📅 Sales Trend")


daily_sales = (
    filtered_df
    .groupby(
        "Date",
        as_index=False
    )["Sales"]
    .sum()
)


fig_trend = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Sales Over Time",
    markers=True
)


fig_trend.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales (KSh)",
    hovermode="x unified"
)


st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ============================================================
# TOP PRODUCTS
# ============================================================

st.subheader("🏆 Product Performance")


product_sales = (
    filtered_df
    .groupby(
        "Product",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


fig_products = px.bar(
    product_sales,
    x="Sales",
    y="Product",
    orientation="h",
    title="Sales by Product",
    text_auto=".2s"
)


fig_products.update_layout(
    xaxis_title="Sales (KSh)",
    yaxis_title="Product"
)


st.plotly_chart(
    fig_products,
    use_container_width=True
)


# ============================================================
# PROFIT BY REGION
# ============================================================

col1, col2 = st.columns(2)


with col1:

    region_profit = (
        filtered_df
        .groupby(
            "Region",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
    )


    fig_region_profit = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s"
    )


    fig_region_profit.update_layout(
        xaxis_title="Region",
        yaxis_title="Profit (KSh)"
    )


    st.plotly_chart(
        fig_region_profit,
        use_container_width=True
    )


# ============================================================
# SALES VS PROFIT
# ============================================================

with col2:

    region_performance = (
        filtered_df
        .groupby(
            "Region",
            as_index=False
        )[["Sales", "Profit"]]
        .sum()
    )


    performance_long = region_performance.melt(
        id_vars="Region",
        value_vars=["Sales", "Profit"],
        var_name="Metric",
        value_name="Amount"
    )


    fig_performance = px.bar(
        performance_long,
        x="Region",
        y="Amount",
        color="Metric",
        barmode="group",
        title="Sales vs Profit by Region"
    )


    fig_performance.update_layout(
        xaxis_title="Region",
        yaxis_title="Amount (KSh)"
    )


    st.plotly_chart(
        fig_performance,
        use_container_width=True
    )


# ============================================================
# DETAILED DATA
# ============================================================

st.subheader("📋 Detailed Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD CSV
# ============================================================

st.subheader("📥 Export Data")


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download CSV",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)


# ============================================================
# DOWNLOAD EXCEL
# ============================================================

excel_buffer = BytesIO()


with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="Sales Data"
    )


excel_buffer.seek(0)


st.download_button(
    label="📊 Download Excel",
    data=excel_buffer,
    file_name="filtered_sales_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    f"Data source: {data_source_name} | "
    f"Showing {len(filtered_df):,} of {len(df):,} cleaned records"
)

st.caption(
    "Built with Python • Pandas • Plotly • Streamlit"
)