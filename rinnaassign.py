#rinna's assignment 3
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

app.title = "MCM7003 Data Visualization Interactive Demo"

# Specify the encoding as 'ISO-8859-1' when reading the CSV file
csv_file_path = "https://raw.githubusercontent.com/RinnaEberaj/assign3MCMRinna/main/Global%20YouTube%20Statistics.csv"

# Read the CSV file from the specified path with 'ISO-8859-1' encoding
df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

# Your data transformation code here
df["Youtuber"]=df["Youtuber"].astype("string")
df["category"]=df["category"].astype("string")
df["Country"]=df["Country"].astype("string")
df["video_views_for_the_last_30_days"]=df["video_views_for_the_last_30_days"]/1000000
df["video views"]=df["video views"]/1000000000
df["subscribers_for_last_30_days"]=df["subscribers_for_last_30_days"]/1000000
df["subscribers"]=df["subscribers"]/1000000
df.rename(columns = {'subscribers':'subscribers_per_millon',
                     'subscribers_for_last_30_days':'subscribers_last_30_days_per_millon',
                    'video_views_for_the_last_30_days':'video_views_last_30_days_per_millon',
                    'video views':'video_views_per_thousands_millions'}, inplace = True)

df_views_category=df[["category","video_views_per_thousands_millions"]].groupby(by="category").sum()
df_views_category=df_views_category.sort_values(by=["video_views_per_thousands_millions"],ascending=False)

fig = px.bar(
    df_views_category, 
    x="video_views_per_thousands_millions",
    y=df_views_category.index,
    orientation='h',
    color_discrete_sequence=['red', 'white'],  # You can customize colors here
    labels={"video_views_per_thousands_millions": "Video views", "category": "Category"}
)

fig.update_layout(
    title="Category vs Video views (thousands millions)",
    xaxis_title="Video views",
    yaxis_title="Category",
    xaxis=dict(tickmode='linear', tick0=0, dtick=1000),  # Customize x-axis ticks
    yaxis=dict(tickmode='linear', tick0=0, dtick=1),  # Customize y-axis ticks
    height=600,
    width=1000,
)

# Create a DataFrame for the top 5 countries with the most YouTubers
countriess = df[["Youtuber", "Country"]]
countriess = countriess.groupby("Country").agg("count")
countriess = countriess.reset_index()
countriess = countriess.sort_values(by="Youtuber", ascending=False).head()

# Create a Plotly Express bar chart
fig2 = px.bar(
    df_views30, 
    x="Youtuber",
    y="video_views_last_30_days_per_millon",
    color_discrete_sequence=['red', 'white'],  # You can customize colors here
    labels={"video_views_last_30_days_per_millon": "Video views", "Youtuber": "Youtuber"}
)

fig2.update_layout(
    title="Top 10 YouTuber's Video Views in Last 30 Days",
    xaxis_title="Youtuber",
    yaxis_title="Video views",
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),  # Customize x-axis ticks
    yaxis=dict(tickmode='linear', tick0=0, dtick=1000),  # Customize y-axis ticks
    height=600,
    width=1000,
)

fig2.update_xaxes(tickangle=45) 

# Create a pie chart using Plotly Express
fig3 = px.pie(
    countriess,
    names="Country",
    values="Youtuber",
    title="Top 5 Countries with the Most YouTubers",
)

fig3.update_traces(
    textinfo="percent+label"
)

fig3.update_layout(
    showlegend=False,
    height=600,
    width=1000,
)

app.layout = html.Div(
    [
        html.H1("Data Visualization Rinna Assignment 3"),
        dcc.Graph(id='graph-output', figure=fig),  # First graph with 'graph-output' ID
        dcc.Graph(id='graph-output-2', figure=fig2),
        dcc.Graph(id='pie-chart', figure=fig3)
    
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8057)
