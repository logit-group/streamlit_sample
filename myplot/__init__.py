from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

def plot_count(df):
    p = df.pivot_table(index=['取引時点（四半期初日）'],values='No',aggfunc='count')
    plot = [go.Bar(x=p.index, y=p['No'])]
    layout = {"title": {"text": "取引件数"},"height": 300,"width": 600}
    fig = go.Figure(data=plot,layout=layout)
    return fig

def plot_price(df_tmp):
    p = df_tmp.pivot_table(index=['取引時点（四半期初日）'],values='単価',aggfunc='mean')
    plot = [go.Scatter(x=p.index, y=p['単価'])]
    layout = {"title": {"text": "平均単価"},"height": 300,"width": 600}
    fig = go.Figure(data=plot,layout=layout)
    return fig

def plot_count_mlt(df):
    p = df.pivot_table(index=['市区町村名','取引時点（四半期初日）'],values='No',aggfunc='count').reset_index()
    p = p[p['No']>0]
    fig = px.bar(p,x='取引時点（四半期初日）', y='No',color='市区町村名',barmode='relative',title='取引件数',height=400,width=400)
    return fig

def plot_price_mlt(df_tmp):
    p = df_tmp.pivot_table(index=['市区町村名','取引時点（四半期初日）'],values='単価',aggfunc='mean').reset_index()
    fig = px.line(p,x='取引時点（四半期初日）', y='単価',color='市区町村名',title='平均単価',height=300,width=400)
    return fig

def plot_price_met(df_tmp,x):
    fig = px.scatter(
        df_tmp,
        x=x,
        y="単価",
        # marginal_x="histogram",
        marginal_y="histogram",
        title=f"単価分析 - {x}",
        color="市区町村名",
        size="面積（㎡）",
        height=800,
        width=800,
        opacity=0.5,
        # trendline="ols"
    )
    return fig

def plot_price_cat(df_tmp,x,category_orders):
    fig = px.box(
        df_tmp,
        x=x,
        y="単価",
        title=f"単価分析 - {x}",
        color="市区町村名",
        height=400,
        width=800,
        category_orders=category_orders
    )
    return fig