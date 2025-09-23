## Setup

Create an API key in Kaggle and save in ~/.kaggle/kaggle.json

## Initialize

```
> poetry install
```
```
> poetry run setup.py
```

## Token Costs and Throughput Challenges

In analyzing approximately 500,000 Enron emails, there are roughly 250 million tokens to process as input and perhaps 5-10 million output tokens. Some model providers charge approximately $2-$3 USD per million input tokens and have a throughput of less than 100 tokens per second. Alternative methods involve hosting your own model and renting GPUs for a fixed cost per hour, with potentially higher throughputs depending on the model.
