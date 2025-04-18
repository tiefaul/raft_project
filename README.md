This project is a fully serverless data pipeline and dashboard for processing and displaying transponder (flight) data. It leverages AWS services to ingest CSV files, transform and store the data, expose metrics via a REST API, and display it on a simple frontend hosted in S3.

---

## 🧠 Project Summary

The goal of this project was to:
- Ingest raw CSV data into Amazon S3 with best practices enabled.
- Transform and load the data into a cloud-based database. I used AWS RDS Postgresql.
- Expose a REST API with endpoints to load data and return key metrics. Endpoint being \load and \metrics.
- Build a static frontend that displays the metrics using the API and a AWS S3 static website.

> Note: This is not a rundown of everything I did. I simply want to provide examples of what I did. You will still have to configure all permissions and networking yourself.

---

## ⚙️ Tech Stack

| Layer       | Service       | Purpose |
|-------------|---------------|---------|
| Storage     | S3 (x2)       | Raw CSV upload + Static frontend hosting |
| API         | API Gateway   | Expose REST endpoints `/load` and `/metrics` |
| Compute     | Lambda (Python 3.13) | Run ETL logic and database queries |
| Database    | PostgreSQL on RDS | Store cleaned flight data |
| Frontend    | HTML + JS + CSS (hosted on S3) | Fetch and display metrics |

---

# 🛰️ Architecture
## Endpoints
### \load (POST)
- Triggers a Lambda function that:
  - Downloads the latest CSV from the S3 Bucket
  - Extracts and transforms the data and loads it into the Postresql database
### \metrics (GET)
- Instructions were to extract 4 data points:
  - max_row_count - Number of rows in the data.
  - last_transponder_seen_at - The time the last transponder was seen at.
  - most_popular_destination - What was the most seen destination in the dataset.
  - count_of_unique_transponders - List out all the unique transponders. (the transponders are in the icao24 field)
- Json output example:
```json
{
  "row_count": 1234,
  "last_transponder_seen_at": "2025-04-09T14:52:30Z",
  "most_popular_destination": "JFK",
  "count_of_unique_transponders": 567
}
```

---

# Key Decisions and Trade-Offs
| Decision | Why |
|----------|-----|
Serverless Architecture | Scalable, cost-effective, no server maintanence
S3 for static frontend | Simple hosting, integrates well with other AWS services
Javascript frontend | required for the API call from a static site (using Fetch())
CORS configuration | Needed to allow frontend to call the API Gateway from a different domain
Lambda packaging | Used zip to bundle and deploy my lambda functions to provide dependencies for Python

---

# What is provided in this repo:

