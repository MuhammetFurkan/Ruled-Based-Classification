########################## Importing Libraries ##########################
import numpy as np
import pandas as pd
import seaborn as sns

########################## Importing  The Data ##########################

df = pd.read_csv('persona.csv')
df

########################### Describing The Data ################################

def check_df(dataframe,head =5):
    print("############################### Shape ###############################")
    print(dataframe.shape)
    print("############################### Types ###############################")
    print(dataframe.dtypes)
    print("############################### Head ###############################")
    print(dataframe.head(head))
    print("############################### Tail ###############################")
    print(dataframe.tail(head))
    print("############################### NA ###############################")
    print(dataframe.isnull().sum())
    print("############################### Quantiles ###############################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# How many unique SOURCE are there? What are their frequencies?

df["SOURCE"].nunique()

# How many unique PRICEs are there?

df["PRICE"].nunique()

# How many sales were made from which PRICE?

df["PRICE"].value_counts()

# How many sales were made from which country?
df["COUNTRY"].value_counts()

# How much was earned in total from sales by country?

df.groupby(["COUNTRY"])[["PRICE"]].agg("sum")

# What is the number of sales by SOURCE types?

df.groupby(["SOURCE"])[["PRICE"]].agg("sum")

# What are the PRICE averages by country?

df.groupby(["COUNTRY"])[["PRICE"]].agg("mean")

# What are the PRICE averages by SOURCEs?

df.groupby(["SOURCE"])[["PRICE"]].agg("mean")

# What are the PRICE averages in the COUNTRY-SOURCE breakdown?

df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": ("mean")})

# What are the average earnings in breakdown of COUNTRY, SOURCE, SEX, AGE?

df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})

# Sort the output by PRICE
# Adjust the sort_values method according to PRICE in descending order so that the output can be seen better.

agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})
agg_df.sort_values(by ="PRICE" , ascending=False)

# Convert the names in the index to variable names.

agg_df.reset_index()
agg_df.head()

# Convert age variable to categorical variable and add it to agg_df.
# Specified Range Values
# '0_18', '19_23', '24_30', '31_40', '41_70'

bins = [0,18,23,30,40, agg_df["AGE"].max()]

mylabels = ["0_18","19_23","24_30","31_40" + str(agg_df["AGE"].max())]
df["AGE"].isnull().sum()

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)

# Identify new level-based customers (personas).

agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

# Removing unnecessary variables

agg_df = agg_df[["customer_level_based","PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))

agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df = agg_df.reset_index()
agg_df.head()

agg_df["customers_level_based"].value_counts()
agg_df.head()

# Segment new customers (personas).

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})

# Classify new customers and estimate how much revenue they can generate.
# Which segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected on average?

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]


# What segment does a 35-year-old French woman using IOS belong to and how much income is expected to earn on average?

new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

