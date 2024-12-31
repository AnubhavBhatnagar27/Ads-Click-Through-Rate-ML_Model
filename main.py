import pandas as pd
import IPython.display as display
import seaborn as sns
import warnings
import matplotlib.pyplot as plt
# %matplotlib inline

# Loading the CSV File
df=pd.read_csv('Marketing campaign dataset.csv')

# Checking the first few rows of dataset
df.head()
# print(df.head())

# Gathering basic information about the dataset
df.info()
# print(df.info)

# Check for missing values
total_missing=df.isnull().sum()
percent_missing=(total_missing*100)/df.isnull().sum()
percent_missing=percent_missing.round(decimals=0)

# Missing Data
missing_data=pd.DataFrame({
    'Total':total_missing,
    'Percentage of Missing Values ': percent_missing,
    'Type':df.dtypes
})
missing_data=missing_data.sort_values(by='Total',ascending=False)
missing_data

# Filling Missing values with zeroes for the following columns
df['creative_width'].fillna(0)
df['creative_height'].fillna(0)
df['template_id'].fillna(0)
df['approved_budget'].fillna(0)

# Dropping columns where nearly 80% of the data is missing
df.drop(columns=['position_in_content','unique_reach','total_reach','max_bid_cpm'],inplace=True)

# Summaric Statistics of the numeric Column
print(df.columns)
df.describe()

# Checking the data types
df.dtypes

# CTR
df['ctr']=(df['clicks']/df['impressions'])*100

# Visualizing the Exploration
df['time']=pd.to_datetime(df['time'],errors="coerce")

# Plotting Histogram of a numeric column
plt.figure(figsize=(10,6))
sns.lineplot(x='time', y='ctr', data=df, color='#FF6361')
plt.title('CTR over time(Full Duration)')
plt.xlabel('Time')
plt.ylabel('CTR')
plt.xticks(rotation=45)
# CTR over last 7 days
last_7_days = pd.to_datetime(df['time'].max()) - pd.DateOffset(days=7)
df_last_7_days = df[df['time'] >= last_7_days]

plt.figure(figsize=(10, 6))
sns.lineplot(x='time', y='ctr', data=df_last_7_days, color='#58508D')
plt.title('CTR over Time (Last 7 Days)')
plt.xlabel('Time')
plt.ylabel('CTR')
plt.xticks(rotation=45)
plt.show()

# compare the spent budget with the number of days

df['spent_budget_per_day'] = df['campaign_budget_usd'] / df['no_of_days']

plt.figure(figsize=(10, 6))
plt.plot(df['no_of_days'], df['spent_budget_per_day'], marker='*')
plt.xlabel("Number of Days")
plt.ylabel("Spent Budget per Day (USD)")
plt.title("Spent Budget per Day vs. Number of Days")
plt.grid(True)
plt.show()

# checking scatter plots for no of days v/s impressions

# Create subplots 
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Scatter plot: no_of_days vs impressions
sns.scatterplot(data=df, x="no_of_days", y="impressions", ax=axes[0])
axes[0].set_xlabel("Number of Days")
axes[0].set_ylabel("Impressions")
axes[0].set_title("Number of Days vs Impressions")

# Scatter plot: no_of_days vs clicks
sns.scatterplot(data=df, x="no_of_days", y="clicks", ax=axes[1])
axes[1].set_xlabel("Number of Days")
axes[1].set_ylabel("Clicks")
axes[1].set_title("Number of Days vs Clicks")

# Adjust the spacing between subplots
plt.tight_layout()

# Show the combined plot
plt.show()

#checking impressions and click with channel distributions 
# Remove rows with missing values in the columns we are using for plotting
df = df.dropna(subset=['impressions', 'clicks', 'channel_name'])
df['channel_name'] = df['channel_name'].astype(str)
sns.lmplot(x = "impressions", y = "clicks", data = df, fit_reg=False, hue='channel_name')  
plt.show()