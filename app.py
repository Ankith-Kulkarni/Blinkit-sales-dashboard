
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Blinkit Sales Dashboard", layout="wide")

st.sidebar.title(" 🛒 Blinkit Sales Dashboard")
st.sidebar.caption("India’s Last Minute Delivery App 🚀")

df=pd.read_csv("Blinkit_sales.csv")
    
st.sidebar.subheader("🔍 Filter Panel")

Outlet_Location_Type=st.sidebar.selectbox("Outlet_Location_Type",["ALL"]+sorted(df["Outlet_Location_Type"].dropna().unique()))

Outlet_Size=st.sidebar.selectbox("Outlet_Size",["ALL"]+sorted(df["Outlet_Size"].dropna().unique()))

Item_Type=st.sidebar.selectbox("Item_Type",["ALL"]+sorted(df["Item_Type"].dropna().unique()))

filtered_df = df.copy()

if Outlet_Location_Type !="ALL":
    filtered_df=filtered_df[filtered_df["Outlet_Location_Type"] == Outlet_Location_Type]

if Outlet_Size !="ALL":
    filtered_df=filtered_df[filtered_df["Outlet_Size"] == Outlet_Size]

if Item_Type !="ALL":
   filtered_df=filtered_df[filtered_df["Item_Type"] == Item_Type]

if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

total_sales=filtered_df["Item_Outlet_Sales"].sum()
avg_sales=filtered_df["Item_Outlet_Sales"].mean()
no_of_items=filtered_df["Item_Type"].nunique()

st.markdown("""
<style>
            .card{
            background: orange;
            padding: 20px;
            border-radius: 12px;
            color: black;
            font-weight: bold;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15)}

            .card2{
                     background: white;
                     padding: 20px;
                     border-radius: 12px;
                     border-left: 6px solid #00c853;
                     font-weight: bold;
                     box-shadow: 0px 4px 12px rgba(0,0,0,0.15);}
            .value {
                   font-size: 28px;
                                  }
            .label {
                    font-size: 14px;
                    opacity: 0.7;}
            .icon {
                  float: right;
                  font-size: 25px;
                  margin-top: -5px;
                   }
            </style>
            """,unsafe_allow_html=True)

c1,c2,c3=st.columns(3)

with c1:
   st.markdown(f"""
               <div class="card">
               <div class="value">${total_sales/1e6:.2f} M<span class="icon">📈</span></div>
               <div class="label">Total Sales</div>
               </div>

               """,unsafe_allow_html=True)
   
with c2:
    st.markdown(f"""
                <div class="card2">
                <div class="value">{avg_sales:.2f}<span class="icon">💲</span></div>
                <div class="label">Avg Sales</div>

""",unsafe_allow_html=True)

with c3:
    st.markdown(f"""
                <div class="card2">
                <div class="value">{no_of_items}<span class="icon">📦</span></div>
                <div class="label">Items</div>
                
""",unsafe_allow_html=True)
    
st.markdown("""
            <br></br>""", unsafe_allow_html=True)


fat_sales=(
    filtered_df.groupby("Item_Fat_Content")["Item_Outlet_Sales"].sum()
)

fig1,ax1=plt.subplots(figsize=(4,4))

ax1.pie(
    fat_sales,
    labels=fat_sales.index,
    autopct=lambda p: f"${p*fat_sales.sum()/100/1e6:.2f}M",
    startangle=90,
    wedgeprops={"width": 0.4},
    labeldistance=1,
    pctdistance=0.7,
    textprops={"fontsize": 9}  
)

ax1.text(0, 0, f"${fat_sales.sum()/1e6:.2f}M\nTotal Sales",
         ha="center", va="center", fontsize=9,fontweight="bold")

ax1.set_title("FAT CONTENT")

item_sales = (
    filtered_df
    .groupby("Item_Type")["Item_Outlet_Sales"]
    .sum()
    .sort_values(ascending=True)
)

fig2, ax2 = plt.subplots(figsize=(6, 6))

ax2.barh(item_sales.index, item_sales.values / 1e6,color="orange")

ax2.set_xlabel("Sales (in Millions)")
ax2.set_title("ITEM TYPE")

for i, v in enumerate(item_sales.values):
    ax2.text(v/1e6, i, f" ${v/1e6:.2f}M", va="center")

outlet_fat = (
    filtered_df
    .groupby(["Outlet_Location_Type", "Item_Fat_Content"])
    ["Item_Outlet_Sales"]
    .sum()
    .unstack()
)

x = np.arange(len(outlet_fat.index))
width = 0.35

fig3, ax3 = plt.subplots()

ax3.barh(x - width/2, outlet_fat["Low Fat"]/1e6, width, label="Low Fat")
ax3.barh(x + width/2, outlet_fat["Regular"]/1e6, width, label="Regular")

ax3.set_xticks(x)
ax3.set_xticklabels(outlet_fat.index)
ax3.set_ylabel("Sales (in Millions)")
ax3.set_title("FAT BY OUTLET")
ax3.legend()

year_sales = (
    filtered_df.groupby("Outlet_Establishment_Year")["Item_Outlet_Sales"]
      .sum()
      .sort_index()
)

fig4, ax4 = plt.subplots(figsize=(5, 3))
ax4.plot(year_sales.index, year_sales.values, color="black", marker="o")
ax4.fill_between(year_sales.index, year_sales.values, color="green")
ax4.set_title("Outlet Establishment")
ax4.set_xlabel("Year")
ax4.set_ylabel("Total Sales")

left, right = st.columns([1, 2])

with left:
    st.pyplot(fig1)
    st.pyplot(fig3)
    plt.close()
    
with right:
    st.pyplot(fig2)
    st.pyplot(fig4)
    plt.close()


 