# **ALPHA EXPLORER**

A SEC Filing Explorer for Inter IIT Tech Meet High Prep Challenge 2022

<hr>

## Inter IIT Tech Meet 10.0 (2022)

![image](https://www.sec.gov/edgar/search/images/edgar-logo-2x.png)
![image](https://interiit-tech.org/static/media/logo_1.f4d40e83.png)

## Introduction

In this Project, we shall be looking into utilizing the [EDGAR](https://www.sec.gov/edgar/searchedgar/) database of SEC Filings to explore the data and build a model to predict the financial sentiment of a company. The project will be built using Python mostly and its aim is to utilize various financial forms like 10-K and 10-Q to predict the financial performance of a company.

## Objectives

- Scrape Data from the company's History since inception
- Use 10-Q 10-K and 8-K filings to get the company's financial statements
- Use Financial Statements to get the company's balance sheet, income statement, cash flow statement, and ratios
- Use the data to get the company's current assets, liabilities, and equity
- Generate SaaS Metrics
- Generate a Financial Statement Analysis
- Use the metrics with Deep Learning Systems to give Insightful Results

## Description

The scraping component of the app is build using Python modules of `Pandas`, `BeautifulSoup` and `Requests`. The app is designed to scrape data from the company's history since inception. The data is then used to build a model to predict the financial performance of the company. The model is then used to give insightful results.

The **Django API** is used to serve the data to the front end. The front end is built using **React.js**. The API has several endpoints to serve data:

- `/` Landing
- `/bs` Returns company data
- `/comp` To Compare Companies (incomplete)
- `strict` To search for companies by TICKER, returns only if it is a perfect match
- `<str:pk>` Get companies by Id

The **React App** is used to display the data on the front end. 

## Achieved Results

- Able to search for company data by Ticker Name or CIK number
- Able to get the company's financial statements.
- Able to get the company's balance sheet, income statement, cash flow statement, and ratios
- Able to get the company's current assets, liabilities, and equity
- Able to plot these metrics on a graph
- Able to predict the financial sentiment of the company based on these reports
- Able to predict company's future common stock price based on the financial statements.

## Tech Stack

- ***Django*** (Backend)
- ***React*** (Frontend)
- ***Mongo*** (Database)
- ***Tensorflow*** (Model)