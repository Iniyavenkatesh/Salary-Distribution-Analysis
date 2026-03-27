from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import os

# Disable debug
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

app = Flask(__name__)

# -------- LOAD DATA --------
df = pd.read_csv("jobs_in_data.csv")

# -------- CLEAN DATA --------
def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna()
    return df

cleaned_df = clean_data(df)

# -------- CREATE CHARTS --------
def create_charts():
    if not os.path.exists("static"):
        os.makedirs("static")

    # 1. Salary Histogram
    if "salary_in_usd" in cleaned_df.columns:
        plt.figure()
        cleaned_df["salary_in_usd"].hist()
        plt.title("Salary Distribution")
        plt.savefig("static/salary_hist.png")
        plt.close()

    # 2. Top Locations
    if "company_location" in cleaned_df.columns:
        plt.figure()
        cleaned_df["company_location"].value_counts().head(10).plot(kind='bar')
        plt.title("Top Company Locations")
        plt.savefig("static/location_bar.png")
        plt.close()

    # 3. Job Titles
    if "job_title" in cleaned_df.columns:
        plt.figure()
        cleaned_df["job_title"].value_counts().head(10).plot(kind='bar')
        plt.title("Top Job Roles")
        plt.savefig("static/job_bar.png")
        plt.close()

    # 4. Experience Level Pie
    if "experience_level" in cleaned_df.columns:
        plt.figure()
        cleaned_df["experience_level"].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Experience Level Distribution")
        plt.ylabel("")
        plt.savefig("static/exp_pie.png")
        plt.close()

create_charts()

# -------- HTML DASHBOARD --------
html = """
<!DOCTYPE html>
<html>
<head>
<title>Data Dashboard</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { background: #f0f2f5; }
.card { margin-top: 20px; border-radius: 15px; }
h1 { text-align: center; margin-top: 20px; }
img { border-radius: 10px; }
</style>
</head>

<body class="container">

<h1>📊 Data Analysis Dashboard</h1>

<div class="row">

<div class="col-md-6">
<div class="card p-3">
<h4>Salary Distribution</h4>
<img src="/static/salary_hist.png" width="100%">
</div>
</div>

<div class="col-md-6">
<div class="card p-3">
<h4>Top Locations</h4>
<img src="/static/location_bar.png" width="100%">
</div>
</div>

<div class="col-md-6">
<div class="card p-3">
<h4>Top Job Roles</h4>
<img src="/static/job_bar.png" width="100%">
</div>
</div>

<div class="col-md-6">
<div class="card p-3">
<h4>Experience Level</h4>
<img src="/static/exp_pie.png" width="100%">
</div>
</div>

</div>

<div class="card p-3">
<h3>🔴 Raw Dataset</h3>
{{ raw|safe }}
</div>

<div class="card p-3">
<h3>🟢 Cleaned Dataset</h3>
{{ clean|safe }}
</div>

</body>
</html>
"""

# -------- ROUTE --------
@app.route('/')
def home():
    return render_template_string(
        html,
        raw=df.head(10).to_html(classes="table table-striped"),
        clean=cleaned_df.head(10).to_html(classes="table table-striped")
    )

# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)