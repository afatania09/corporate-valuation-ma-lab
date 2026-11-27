"""Run: streamlit run dashboard.py"""
import streamlit as st
from examples.hilton_lbo_case import scenario
from valuation_lab.excel_export import lbo_workbook
from valuation_lab.merger_eps import MergerInputs, merger_eps

st.set_page_config(page_title="Corporate Finance Lab", layout="wide")
st.title("Corporate Finance & M&A Lab")
st.caption("Educational underwriting | USD millions for merger; USD billions for LBO")
lbo, merger = st.tabs(["Sponsor LBO", "Merger EPS"])
with lbo:
    st.info("Hilton-inspired hypothetical scenario; not actual sponsor returns.")
    a,b,c = st.columns(3)
    ev=a.number_input("Entry EV", min_value=0.1,value=26.0)
    debt=b.number_input("Entry debt",min_value=0.0,value=20.0)
    years=c.number_input("Holding years",min_value=1,value=6)
    e=a.number_input("Exit EBITDA",min_value=0.0,value=3.0)
    m=b.number_input("Exit multiple",min_value=0.0,value=12.0)
    d=c.number_input("Exit debt",min_value=0.0,value=12.0)
    try:
        r=scenario(ev,debt,e,m,d,years)
        a.metric("MOIC",f"{r['moic']:.2f}x")
        b.metric("Annualised return",f"{r['annualised_return']:.1%}")
        c.metric("Exit equity",f"${r['exit_equity']:.2f}bn")
        st.bar_chart({"Entry equity": [r["entry_equity"]], "Exit equity": [r["exit_equity"]]})
        st.download_button("Export LBO results (CSV)",",".join(r)+"\n"+",".join(str(v) for v in r.values()),"lbo.csv","text/csv")
        st.download_button('Export editable Excel model', lbo_workbook(ev,debt,e,m,d,years), 'lbo.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except ValueError as exc:
        st.error(str(exc))
with merger:
    st.caption("Hypothetical annualised earnings; shares in millions.")
    a,b,c=st.columns(3)
    ni=a.number_input("Buyer net income",value=100.0)
    shares=b.number_input("Buyer shares",min_value=0.01,value=50.0)
    price=c.number_input("Buyer share price",min_value=0.01,value=20.0)
    target=a.number_input("Target net income",value=20.0)
    consideration=b.number_input("Equity consideration",min_value=0.0,value=200.0)
    stock=c.slider("Stock funding %",0,100,50)
    debt_pct=a.slider("Debt funding %",0,100-stock,min(25,100-stock)) if stock<100 else 0
    rate=b.number_input("Debt rate %",min_value=0.0,value=8.0)
    tax=c.slider("Tax rate %",0,100,25)
    synergies=a.number_input("Pre-tax synergies",value=10.0)
    integration=b.number_input("Integration costs",min_value=0.0,value=4.0)
    amort=c.number_input("Incremental amortisation",min_value=0.0,value=2.0)
    cash_yield=st.number_input("Foregone cash yield %",min_value=0.0,value=4.0)
    r=merger_eps(MergerInputs(ni,shares,price,target,consideration,stock/100,debt_pct/100,rate/100,cash_yield/100,tax/100,synergies,integration,amort))
    a.metric("Standalone EPS",f"{r['standalone_eps']:.2f}")
    b.metric("Combined EPS",f"{r['combined_eps']:.2f}")
    c.metric("Accretion",f"{r['accretion_pct']:.2f}%" if r["accretion_pct"] is not None else "N/A")
    st.download_button("Export merger results (CSV)",",".join(r)+"\n"+",".join(str(v) for v in r.values()),"merger.csv","text/csv")
