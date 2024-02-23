import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from myplot import plot_count_mlt,plot_price_mlt,plot_price_met,plot_price_cat
import settings

# config
st.set_page_config(layout="wide")

# settings
list_yoto = settings.list_yoto
list_met = settings.list_met

# headings
title = "土地価格分析アプリ"
st.header(":book:土地取引価格分析ダッシュボード(mock)")
st.markdown("国土交通省土地総合情報システムの土地取引データをstreamlitで可視化")

# data
df = pd.read_parquet(settings.fp)
df_mst = pd.read_parquet(settings.fp_mst)

## 土地取引に絞る
df = df[df['種類']=='宅地(土地)']

## 市区町村名に順番
cat = pd.CategoricalDtype(list(df_mst['市区町村名']),ordered=True)
df['市区町村名'] = df['市区町村名'].astype(cat)

## 件数カウント
df_mst['件数'] = df_mst['市区町村コード'].map(df['市区町村コード'].value_counts()).fillna(0)
df_mst['市区町村名（表示用）'] = [f'{x}({y}件)' for x,y in zip(df_mst['市区町村名'],df_mst['件数'])]

## 単価テーブル
df_tmp = df.loc[df['面積（㎡）']!='2000㎡以上',:]
df_tmp['単価'] = (df_tmp['取引価格（総額）'] / df_tmp['面積（㎡）'].astype(int)).astype(int)
df_tmp['面積（㎡）'] = df_tmp['面積（㎡）'].astype(int)

# user inputs on sidebar
st.sidebar.title("設定")
choices = st.sidebar.multiselect('市区町村',list(df_mst['市区町村名（表示用）']),default=list(df_mst['市区町村名（表示用）'].iloc[8:12]))

## 選択中の市区町村
cities = list(df_mst[df_mst['市区町村名（表示用）'].isin(choices)]['市区町村コード'])
city_names = list(df_mst[df_mst['市区町村名（表示用）'].isin(choices)]['市区町村名'])

## df再作成
df = df[df['市区町村コード'].isin(cities)]
df_tmp = df_tmp[df_tmp['市区町村コード'].isin(cities)]

# main body
with st.container():
    col1, col2 = st.columns(2,gap='medium')
    with col1:
        st.plotly_chart(plot_count_mlt(df),use_container_width=True)
    with col2:
        st.plotly_chart(plot_price_mlt(df_tmp),use_container_width=True)

st.plotly_chart(plot_price_cat(df_tmp,"都市計画",{"都市計画":list_yoto}),use_container_width=True)

with st.container():
    tabs = st.tabs(list_met)
    for met,tab in zip(list_met,tabs):
        with tab:
            st.plotly_chart(plot_price_met(df_tmp,met),use_container_width=True)

st.markdown("**生データ**")
st.dataframe(df)
st.markdown("Powered by [LOGIT group](https://consulting.logit.jp/)")
st.markdown("不動産取引価格情報　国土交通省")