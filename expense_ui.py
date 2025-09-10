import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

CSV_FILE = "expenses.csv"

# Load existing data or create a new DataFrame
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
else:
    df = pd.DataFrame(columns=["desc", "amount", "category", "date"])

st.set_page_config(page_title="💸 Expense Tracker", page_icon="📊", layout="centered")
st.title("💸 Personal Expense Tracker")

# --- Add Expense Form ---
with st.form("expense_form"):
    desc = st.text_input("📝 Description")
    amount = st.number_input("💰 Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("📂 Category", ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Other"])
    date = st.date_input("📅 Date", datetime.today().date())
    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        new_expense = pd.DataFrame(
            [[desc, amount, category, date]],
            columns=["desc", "amount", "category", "date"]
        )
        df = pd.concat([df, new_expense], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ Expense Added!")


# --- Expense Filters ---
st.subheader("🔍 View Expenses")
view_option = st.radio("📊 View by", ["All", "Day", "Week", "Month"])

today = datetime.today().date()
if view_option == "Day":
    filtered_df = df[df["date"] == today]
elif view_option == "Week":
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    filtered_df = df[(df["date"] >= start_week) & (df["date"] <= end_week)]
elif view_option == "Month":
    filtered_df = df[(df["date"].apply(lambda x: x.month) == today.month) &
                     (df["date"].apply(lambda x: x.year) == today.year)]
else:
    filtered_df = df.copy()

# Sort by date (latest first)
if not filtered_df.empty:
    filtered_df = filtered_df.sort_values(by="date", ascending=False)

# --- Show Table ---
st.dataframe(filtered_df, use_container_width=True)

# --- Delete Option ---
if not filtered_df.empty:
    st.subheader("🗑️ Delete Expense")
    row_to_delete = st.selectbox("Select an expense to delete", filtered_df.index)

    if st.button("❌ Delete Selected Expense"):
        df = df.drop(row_to_delete).reset_index(drop=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("Expense deleted successfully! Refresh to see updates.")

# --- Show Total ---
if not filtered_df.empty:
    total = filtered_df["amount"].sum()
    st.metric("💵 Total", f"{total:.2f}")
else:
    st.info("No expenses found for this filter.")
