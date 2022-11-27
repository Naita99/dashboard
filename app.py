
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_excel(
    "assets/dashboard.xlsx",
)

states = df.State.unique().tolist()
outcomes = df.Outcome.unique().tolist()
outcomes.insert(0, "all")
mind = df.Date.min()
maxd = df.Date.max()

def part_a():

    figure = px.line(x=totac.index, y=totac.values)
    figure.add_scatter(x=totsuc.index,y=totsuc.values,name="Success")
    figure.add_scatter(x=totnsuc.index,y=totnsuc.values,name= "Failure")
    figure.add_scatter(x=totsuc.index,y=totsuc.values*100/totac[totsuc.index],name = "Ratio")
    
    return figure

def part_b():
    figure=px.bar(x=totacs.index, y=totacs.values)
    figure.add_bar(x=totsucs.index,y=totsucs.values,name="Success")
    figure.add_bar(x=totnsucs.index,y=totnsucs.values,name= "Failure")
    
    return figure

def part_c():
    data1=df.groupby("Outcome")["Outcome"].count()
    figure = px.pie( values= data1.values, names = data1.index)
    
    return figure

def part_d():
    figure = go.Figure()

    totac = df.groupby("State")["Outcome"].count()
    totsuc = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()

    state_success = (totsuc / totac * 100).sort_values(ascending=False)

    figure.add_trace(
        go.Bar(
            x=state_success.index,
            y=state_success.values,
            name="State success",
        )
    )

    return figure

def part_e():
   
    totac = df.groupby('State')['Outcome'].count()

    labels = totac.index
    vals = totac.values.flatten()

    figure = go.Figure(data=[go.Pie(labels=labels, values=vals, hole=.3)])
    figure.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return figure
    
def part_f():
    try:
        figure = px.bar(df_changed, x=df_changed.Time_Period,
                      y=df_changed.Outcome)
        return figure
    except Exception as e:
        pass



def filter_date(outcome, state, dateStart, dateEnd):
    global df, totac, totacs, totnsuc, totsucs, tottime, totnsucs, totsuc, df_changed

    df = pd.read_excel(
        "assets/dashboard.xlsx",
    )

    if outcome == "all" and state == "all":
        df = df[(df.Date >= dateStart) & (df.Date <= dateEnd)]
    elif outcome == "all":
        df = df[(df.Date >= dateStart) & (df.Date <= dateEnd)]
        df = df[df.State.isin(state)]
    elif state == "all":
        df = df[(df.Date >= dateStart) & (df.Date <= dateEnd)]
        df = df[df.Outcome == outcome]
    else:
        df = df[(df.Date >= dateStart) & (df.Date <= dateEnd)]
        df = df[df.State.isin(state)]
        df = df[df.Outcome == outcome]
    
    totac = df.groupby('Date')['Outcome'].count()
    totsuc = df[df['Outcome'] == 'Success'].groupby('Date')['Outcome'].count()
    totnsuc = df[df['Outcome'] == 'Failure'].groupby('Date')['Outcome'].count()
    tottime = df[df['Outcome'] == 'Time out'].groupby('Date')['Outcome'].count()
    totacs = df.groupby('State')['Outcome'].count()
    totsucs = df[df['Outcome'] == 'Success'].groupby('State')['Outcome'].count()
    totnsucs = df[df['Outcome'] == 'Failure'].groupby('State')['Outcome'].count()

    df_changed = (
        df[df["Outcome"] == "Success"]
        .groupby("Time_Period")["Outcome"]
        .count()
        .reset_index()
    )


app.layout = html.Div([

    html.Div(
        children = [ 
            html.H1(children = "Course Work 2", className="title"),
            html.P(children="Visualization of the data in a global way", className="description",),
            html.P(children="Work done by Abdrakhmanova Naita", className="description1",),], className="header",),
            
            

        html.Div(children=[
            dcc.Dropdown(
                options=["Success", "Failure"],
                value='all',
                placeholder="Select",
                id="outcome",
           
            ),
            dcc.Dropdown(states,
                         value='all',
                         multi = True,
                         placeholder="All states",
                         id="states",
                       
                         ),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="datePicker",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            )],
            className="dropdown1"),


        html.P(children = "a-We want to see this data in a graph with a time series legend. Then we want to see in the same graph the ratio of success /total calls as a function of date.", className="sub-title",),
        dcc.Graph(id="image1"),
        html.P(children = "b-We want to see another graph that presents the success and failure by State in the form of a bargraph.", className="sub-title",),
        dcc.Graph(id="image2"),
        html.P(children = "c-We want to see a piechart that displays failure-success-timeout as a percentage", className="sub-title",),
        dcc.Graph(id="image3"),
        html.P(children = "d-We want to see at the end which state was the most ' successful ' in share ratios.", className="sub-title",),
        dcc.Graph(id="image4"),
        html.P(children = "e-We also want to see a double piechart that displays the total number of actions/ State and number of success / state .", className="sub-title",),
        dcc.Graph(id="image5"),
        html.P(children = "f-We want to know the number of succes by Time_Period", className="sub-title",),
        dcc.Graph(id="image6"),



    ], className="mainDiv")

@app.callback(
    [
    Output("image1", "figure"),
    Output("image2", "figure"),
    Output("image3", "figure"),
    Output("image4", "figure"),
    Output("image5", "figure"),
    Output("image6", "figure"),
    ],
    [
    Input("outcome", "value"),
    Input("states", "value"),
    Input("datePicker", "start_date"),
    Input("datePicker", "end_date"),
    ]
)

def update_output(outcome, state, dateStart, dateEnd):

    if state == None or len(state) == 0:
        state = "all"

    if outcome == None or len(outcome) == 0:
        outcome = "all"

    filter_date(outcome, state, dateStart, dateEnd)

    return part_a(), part_b(), part_c(), part_d(), part_e(), part_f()

    


if __name__=="__main__":
    app.run_server(debug=True)