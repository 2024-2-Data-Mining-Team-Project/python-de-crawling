# python-de-insight

# Seoul Business Location Data Crawler

This repository contains the scripts and processes for web crawling and collecting business location data in Seoul. The primary goal is to gather detailed information on stores across various categories to support market analysis and recommendation system development.

---

## Features

- **Automated Data Collection**: Gathers store information from Naver Maps using predefined search queries.
- **Customizable Categories**: Allows searches for specific business types (e.g., cafes, Korean food, Chinese food).
- **API Integration**: Incorporates Naver and Google APIs for geocoding and transportation data retrieval.
- **Data Structuring**: Outputs cleaned and structured data in CSV format for further analysis.

---

## Data Collected

The crawling process gathers the following information for each store:

| Field       | Description                              |
|-------------|------------------------------------------|
| `매장명`    | Store name                              |
| `카테고리`  | Business category (e.g., cafe, Korean food) |
| `평점`      | Average rating                          |
| `리뷰`      | Number of reviews                       |

The data is separated into categories and saved in individual CSV files, such as `카페.csv`, `한식.csv`, etc.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/seoul-business-crawler.git
   cd seoul-business-crawler
