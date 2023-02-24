---
hide:
  - toc
---
# TB-ML-Containers

Welcome to the tb-ml-community page which serves as a centralised repository list of containers that can be used with [tb-ml](https://github.com/jodyphelan/tb-ml). Click on an individual container to find out more. For information on how to build containers and how to add them to this page, click on the [contribute](contribute.md) section.

## Prediction containers

Name | Architecture | Drugs | Input | Docker 
------------ | ------------- | ------------ | ------------ | ------------
{%- for c in get_prediction_containers() %}
{{ c.url }} | {{ c.architecture }}  | {{ c.drugs }} | {{ c.input }} | {{ c.docker }}
{%- endfor %}

## Preprocessing containers

Name | Input | Features | Docker 
------------ | ------------- | ------------ | ------------
{%- for c in get_preprocessing_containers() %}
{{ c.url }} | {{ c.input }}  | {{ c.features }} | {{ c.docker }}
{%- endfor %}


<!-- 100% privacy friendly analytics to report back to funding agency -->
<!-- Learn more at https://docs.simpleanalytics.com/what-we-collect -->
<script async defer src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<noscript><img src="https://queue.simpleanalyticscdn.com/noscript.gif" alt="" referrerpolicy="no-referrer-when-downgrade" /></noscript>
