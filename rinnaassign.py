from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

app.title = "MCM7003 Data Visualization Interactive Demo"

df_views_category = pd.read_csv("https://raw.githubusercontent.com/RinnaEberaj/assign3MCMRinna/main/Global%20YouTube%20Statistics.csv")

# Your data transformation code here

# Create a Plotly figure using Plotly Express
fig = px.bar(
    df_views_category, 
    x="video_views_per_thousands_millions", 
    y="category",
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

app.layout = html.Div(
    [html.H1("Data Visualization"),
     dcc.Graph(id='graph-output', figure=fig)]
)

if __name__ == '__main__':
    app.run_server(debug=True)