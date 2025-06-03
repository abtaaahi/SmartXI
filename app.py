import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
from trainTeam import team

st.title("SmartXI")
d=pd.read_csv("data.csv")

with open("market_value_model.pkl","rb") as f:
    marketmodel, marketfeatures=pickle.load(f)
with open("label_encoders.pkl","rb") as f:
    encoders=pickle.load(f)

def lineup(team):
    group={"GK":[],"DEF":[],"MID":[],"FWD":[]}
    for _, p in team.iterrows():
        pos=p['Position'].lower()
        plname=p['Name']
        if"goalkeeper"in pos:
            group["GK"].append(plname)
        elif"defender"in pos:
            group["DEF"].append(plname)
        elif"midfielder"in pos:
            group["MID"].append(plname)
        elif"forward"in pos:
            group["FWD"].append(plname)

    y={"FWD":0.9,"MID":0.65,"DEF":0.4,"GK":0.15}
    field="#007A33"
    tc="#ffffff"
    marker="#FAB634"

    fig=go.Figure()

    for role,y in y.items():
        players=group[role]
        if not players:
            continue
        x_coords=[i/(len(players)+1) for i in range(1,len(players)+1)]
        for x,name in zip(x_coords, players):
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=40, color=marker, line=dict(width=2, color="white")),
                text=[name],
                textposition="bottom center",
                textfont=dict(size=12, color=tc),
                hoverinfo="text"
            ))

    fig.add_shape(type="rect",x0=0,y0=0,x1=1,y1=1,line=dict(color="white",width=3))
    fig.update_layout(
        title=dict(text="Team Lineup", x=0.5, font=dict(color="white")),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        plot_bgcolor=field,
        paper_bgcolor=field,
        height=600,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
    )
    return fig

option=st.sidebar.selectbox("Choose Option",["Recommend a Team","Predict Player Market Value"])

if option=="Recommend a Team":
    budget=st.number_input("", min_value=1)
    formation=st.selectbox("",["4-3-3","4-4-2","3-4-3"])
    style=st.selectbox("",["Attacking","Balanced","Defensive"])

    if st.button("Generate Team"):
        message=st.empty()
        message.info("")
        team=team(budget, formation, style)
        message.empty()
        st.success("")
        team.index=range(1, len(team) + 1)
        st.dataframe(team)
        fig=lineup(team)
        st.plotly_chart(fig)

elif option=="Predict Player Market Value":
    plp=d["Name"].dropna().unique().tolist()
    sl=st.selectbox("", sorted(plp))
    if sl and st.button("Predict"):
        pl=d[d["Name"]==sl]
        if pl.empty:
            st.error("not")
        else:
            input_features=pl.drop(columns=["Name","Nationality","Position","Club"], errors="ignore")
            value=marketmodel.predict(input_features)[0]
            st.success(f"Estimated Market Value: ${value/1_000_000:.2f} Million")
            st.dataframe(pl.drop(columns=["Nationality", "Position"]))
            stats_labels=["Pace","Shooting","Passing","Dribbling","Defending","Physical"]
            stats_values=pl[stats_labels].values.flatten().tolist()
            fig=go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=stats_values,
                theta=stats_labels,
                fill='toself',
                name=sl,
                line=dict(color='gold')
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                showlegend=False,
            )

            st.plotly_chart(fig)