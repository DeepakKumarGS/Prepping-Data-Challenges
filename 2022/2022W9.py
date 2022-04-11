# Prepping Data 2022 Week 9
## Recreated from Solution by @arseneXie (Arsene)
import pandas as pd
import numpy as np
import re

classification = {"N": "New", "C": "Consistent", "S": "Sleeping", "R": "Returning"}


orders = pd.read_excel("data/PD 2022 Wk 9 Sample - Superstore.xls", sheet_name="Orders")
# Aggregate the data to the years each customer made an order

orders["year"] = orders["Order Date"].dt.year
# Calculate the year each customer made their First Purchase

customer_purchase = orders[["Customer ID", "Customer Name", "year"]].drop_duplicates()

customer_purchase["Order?"] = 1

customer_purchase["First Purchase"] = customer_purchase.groupby("Customer ID")[
    "year"
].transform("min")
# Scaffold the dataset so that there is a row for each year after a customers First Purchase, even if they did not make an order
customer_purchase = customer_purchase.pivot_table(
    index=["Customer ID", "Customer Name", "First Purchase"],
    columns="year",
    values="Order?",
    aggfunc="max",
).reset_index()
# Create a field to flag these new rows, making it clear whether a customer placed an order in that year or not
customer_purchase = customer_purchase.melt(
    id_vars=["Customer ID", "Customer Name", "First Purchase"],
    value_name="Order?",
    var_name="year",
)

customer_purchase["Order?"] = customer_purchase["Order?"].apply(
    lambda x: 0 if pd.isnull(x) else 1
)

# Calculate the Year on Year difference in the number of customers from each Cohort in each year

customer_purchase["Power"] = customer_purchase["year"].max() - customer_purchase["year"]

customer_purchase["Position"] = (
    customer_purchase["year"] - customer_purchase["year"].min()
)

customer_purchase["temp"] = customer_purchase["Order?"] * (
    10 ** customer_purchase["Power"]
)

customer_purchase["OrderString"] = (
    customer_purchase["temp"].groupby(customer_purchase["Customer ID"]).transform("sum")
)

customer_purchase["OrderString"] = customer_purchase["OrderString"].apply(
    lambda x: re.sub(
        "0",
        "S",
        re.sub("(?<=0)(1)", "R", re.sub("(?<!0)(1)", "C", re.sub("(^1)", "N", str(x)))),
    ).rjust(4, "-")
)

customer_purchase["Customer Classification"] = customer_purchase.apply(
    lambda x: classification.get(x["OrderString"][x["Position"]], "-"), axis=1
)

customer_purchase = customer_purchase[
    customer_purchase["Customer Classification"] != "-"
][
    [
        "Customer ID",
        "Customer Name",
        "First Purchase",
        "year",
        "Order?",
        "Customer Classification",
    ]
]

cohort = customer_purchase.groupby(["First Purchase", "year"], as_index=False).agg(
    {"Order?": "sum"}
)

cohort = cohort.sort_values(["First Purchase", "year"])

cohort["Previous"] = cohort.groupby("First Purchase")["Order?"].transform(
    lambda x: x.shift(1)
)

cohort["YoY Difference"] = cohort["Order?"] - cohort["Previous"]

customer = pd.merge(
    customer_purchase,
    cohort[["First Purchase", "year", "YoY Difference"]],
    on=["First Purchase", "year"],
)

final = pd.merge(
    customer, orders, on=["Customer ID", "Customer Name", "year"], how="left"
)
