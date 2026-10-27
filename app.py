import streamlit as st
import os
import requests

st.set_page_config(page_title="SmartPenny AI", page_icon="💰", layout="wide")

st.title("💰 SmartPenny AI")
st.caption("Autonomous Multi-Agent Expense & Savings Optimizer")

api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not api_key:
    st.info("Please enter your Groq API key in the sidebar to proceed.")
    st.stop()

st.subheader("📋 Enter Monthly Financial Details")

col1, col2 = st.columns(2)
with col1:
    monthly_income = st.number_input("Total Monthly Income (₹):", min_value=1000, value=25000)
with col2:
    expenses_text = st.text_area(
        "Enter Raw Expenses (Item: Amount):",
        value="Rent: 8000\nGroceries: 4500\nZomato/Eating out: 3500\nNetflix & Prime: 800\nShopping & Clothes: 4000\nSIP/Investments: 2000\nUtilities & Recharge: 1500",
        height=150
    )

def call_groq_agent(system_prompt, user_prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Active production models on Groq
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-20b"]
    
    last_error = ""
    for model_name in models_to_try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            last_error = response.text

    st.error(f"Groq API Error: {last_error}")
    st.stop()

if st.button("🚀 Run SmartPenny Multi-Agents"):
    with st.spinner("🤖 Agent 1: Categorizing Raw Transactions..."):
        categorizer_system = "You are an expert Expense Categorizer Specialist. Categorize raw input into Needs, Wants, and Savings with total sums."
        categorizer_user = f"Income: ₹{monthly_income}\nExpenses:\n{expenses_text}"
        step1_out = call_groq_agent(categorizer_system, categorizer_user)
        
    with st.spinner("🤖 Agent 2: Analyzing 50/30/20 Budget Overruns..."):
        optimizer_system = "You are a Budget Optimization Specialist. Compare categorized spending against the standard 50/30/20 budget rule."
        optimizer_user = f"Total Income: ₹{monthly_income}\nCategorized Data:\n{step1_out}"
        step2_out = call_groq_agent(optimizer_system, optimizer_user)

    with st.spinner("🤖 Agent 3: Generating Actionable Financial Plan..."):
        advisor_system = "You are a Personal Financial Advisor. Provide 4 clear actionable advice to cut down 'Wants' and boost 'Savings'."
        advisor_user = f"Budget Analysis:\n{step2_out}"
        step3_out = call_groq_agent(advisor_system, advisor_user)

    st.success("✅ Multi-Agent Workflow Executed Successfully!")
    
    st.markdown("### 📊 Agent 1: Expense Categorization")
    st.markdown(step1_out)
    
    st.markdown("---")
    st.markdown("### 📈 Agent 2: 50/30/20 Budget Optimization")
    st.markdown(step2_out)
    
    st.markdown("---")
    st.markdown("### 💡 Agent 3: Actionable Advisory & Savings Plan")
    st.markdown(step3_out)