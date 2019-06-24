from plotly.offline import plot
import plotly.graph_objs as go

scores = []


def show(instance):
    scatter = go.Scatter(
        x=list(range(1, len(scores) + 1)),
        y=scores,
        mode='lines+markers'
    )
    layout = go.Layout(
        title='Evolution graph',
        xaxis=dict(
            title='Generations'
        ),
        yaxis=dict(
            title='Best scores'
        )
    )
    fig = go.Figure(data=[scatter], layout=layout)
    plot(fig)
