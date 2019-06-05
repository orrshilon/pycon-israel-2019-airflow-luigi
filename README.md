# Data Pipelines - Comparing Airflow and Luigi by people who have made mistakes in both
This repository contains the code examples from the talk.

### Abstract
Data is Twiggle's bread and butter, so choosing the right data pipelining framework was critical for us. After comparing Luigi and Airflow pipelines we ended up selecting both! We’ll explain why, present our unique challenges and chosen solutions.

### Description
Organizing and scaling data pipelines is a common challenge many organizations face. Luigi and Airflow are the two most popular open source frameworks to help solve this task. We will present a quick overview and comparison of the two. Then we will take a deep dive, including code examples, into the special cases for which we used the frameworks at Twiggle.

Among the examples we will discuss: 
* Airflow as a highly available web server, and extending it with APIs for customers. 
* Data processing using Dask and Spark in Luigi. 
* Code reuse in Luigi vs Airflow.
