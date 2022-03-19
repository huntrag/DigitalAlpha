# **ALPHA EXPLORER**

A SEC Filing Explorer for Inter IIT Tech Meet High Prep Challenge 2022
<hr>

## Inter IIT Tech Meet 10.0 (2022)

- Initially install all the requirements using the following script
- pip install -r requirements.txt
- If you are using virtual environment, activate and do the following
- manage.py will start the django server. Thus, enter the sec directory and run
- python manage.py runserver

## Introduction

This is a team project by:

In this Project, we shall be looking into utilizing the [EDGAR](https://www.sec.gov/edgar/searchedgar/) database of SEC Filings to explore the data and build a model to predict the financial sentiment of a company. The project will be built using Python mostly and its aim is to utilize various financial forms like 10-K and 10-Q to predict the financial performance of a company.

## How to run

- In one terminal, run the following command
  - go to sec subfolder `cd /sec`
  - run `pip install -r requirements.txt` to install all the requirements
  - run `python manage.py runserver` to run the backend.
  - the backend must be now up and running at **127.0.0.1:8000**
- In another terminal, run the following command
  - go to Frontend/interiit `cd /FrontEnd/interiit`
  - run `npm install` (for the first time)
  - run `npm start` to run the frontend
  - the frontend must be now up and running at **127.0.0.1:3000**
  - fire up the browser and go to `127:0.0.1:3000/search` to now search for companies and see the results for yourselves

## Website Structure

The site has a la

## Shipped Features

Features that are shipped and ready to use are

- **Seach:** Search for companies and see the results
  - ![img1](https://raw.githubusercontent.com/Inter-IIT/DigitalAlpha/Backend/docs/img/s1.jpg?token=GHSAT0AAAAAABQ5PJ4YR3K3AJJVK3WZSONMYRV7SCA)
- **Company Details:** See the details of a company
  - ![img1](https://raw.githubusercontent.com/Inter-IIT/DigitalAlpha/Backend/docs/img/s5.jpg?token=GHSAT0AAAAAABQ5PJ4Y2PI4CV7CN3BKV7MIYRV7MEQ)
- **Charts:** See the financial charts of a company
  - ![img1](https://raw.githubusercontent.com/Inter-IIT/DigitalAlpha/Backend/docs/img/s7.jpg?token=GHSAT0AAAAAABQ5PJ4Z5UMQNEFMVBHYSKWAYRV7M6A)
- **Stock:** Common Stock Price of the company of last 5 years.
  - ![img1](https://raw.githubusercontent.com/Inter-IIT/DigitalAlpha/Backend/docs/img/s6.jpg?token=GHSAT0AAAAAABQ5PJ4Z3RCXLMNNYRCKB6NAYRV7N2A)

## Beta Features

Some features currently in beta are:

- **Document Sentiment Analysis:** Sentiment Analysis of the documents. Ref to `scripts/sentiment-analysis.ipynb`
- **Deep Learning Model for Stock Prediction:** Sentiment Analysis of the company. Ref to `scripts/stockPred.ipynb`.

## Total Objectives

- Scrape Data from the company's History since inception
- Use 10-Q 10-K and 8-K filings to get the company's financial sentiments
- Use Financial Statements to get the company's balance sheet, income statement, cash flow statement, and ratios
- Use the data to get the company's current assets, liabilities, and equity
- Generate SaaS Metrics
- Generate a Financial Statement Analysis
- Use the metrics with Deep Learning Systems to give Insightful Results

## Completed Objectives

- Scrape Data from the company's History since inception
- Use Financial Statements to get the company's balance sheet, income statement, cash flow statement, and ratios
- Use the data to get the company's current assets, liabilities, and equity
- Generate a Financial Statement Analysis
- Use the metrics with Deep Learning Systems to give Insightful Results

## Future Goals

- Generate SaaS Metrics
- Use 10-Q 10-K and 8-K filings to get the company's financial sentiments
