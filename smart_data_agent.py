# Smart Data Analysis & Decision Support Agent

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import openai  # pip install openai

# 1. Configure OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key

# 2. Load data (replace with CSV/API as needed)
sales_data = pd.DataFrame({
    "date": pd.date_range(start="2026-05-01", periods=10),
    "product": ["A","B","C","D","E","A","B","C","D","E"],
    "sales": np.random.randint(50, 200, size=10)
})

inventory_data = pd.DataFrame({
    "product": ["A","B","C","D","E"],
    "stock": np.random.randint(20, 100, size=5)
})

user_behavior_data = pd.DataFrame({
    "date": pd.date_range(start="2026-05-01", periods=10),
    "active_users": np.random.randint(100, 500, size=10)
})

# 3. Data cleaning and merging
sales_summary = sales_data.groupby("product").agg({"sales":"sum"}).reset_index()
business_data = pd.merge(sales_summary, inventory_data, on="product")
business_data["reorder_needed"] = business_data["stock"] < (0.5 * business_data["sales"])

# 4. Visualization
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.barplot(x="product", y="sales", data=business_data, color="skyblue", label="Total Sales")
sns.lineplot(x="product", y="stock", data=business_data, marker='o', color='red', label="Stock")
plt.title("Sales vs Stock")
plt.ylabel("Quantity")
plt.legend()
plt.tight_layout()
plt.savefig("sales_vs_stock.png")
plt.show()

# 5. AI analysis and recommendations
ai_prompt = f"""You are a business data analysis assistant. Analyze the following business data, including sales trends, inventory status, and provide optimization suggestions:
{business_data.to_dict(orient='records')}

Generate a report in English or Chinese, including:
1. Sales trend analysis
2. Inventory health
3. Recommendations for reordering or optimization
The report should be concise and usable for management decision-making."""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": ai_prompt}],
    temperature=0.5,
    max_tokens=500
)

ai_report = response['choices'][0]['message']['content']

# 6. Save report
report_file = "ai_business_report.txt"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"Data Analysis Report - {datetime.now().strftime('%Y-%m-%d')}\n")
    f.write("="*40 + "\n\n")
    f.write(ai_report)

print(f"Report generated: {report_file}")
print("\nReport preview:\n")
print(ai_report)
