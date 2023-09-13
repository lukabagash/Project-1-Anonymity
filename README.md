# Project-1-Anonymity



# Flight Data Anonymization

This repository contains code for anonymizing flight data using k-anonymity and measuring the utility of the anonymized data. This README provides instructions on how to reproduce the results of the project using the provided code.

## Getting Started

### Installation

1. Clone this repository:

```bash
git clone https://github.com/lukabagash/Project-1-Anonymity.git
cd Project-1-Anonymity
```

2. Install the required Python libraries:

```bash 
pip install pandas
```

## Usage

### 1. Data Preparation

Before you can start anonymizing the flight data, you need to obtain the dataset. You can download the dataset from [here](https://github.com/lukabagash/Project-1-Anonymity/blob/main/data/Flight_DataSet.csv). Place the dataset in the `data`/ directory. 

### 2. Running the Anonymization Code

To anonymize the flight data for different k-values (e.g., 2, 5, 50), follow these steps:

1. Open the `k_anonymity_test.py` script.
2. Set the `data_path` variable to the path of your flight dataset:

```python
data_path = "data/Flight_DataSet.csv"
```

Run the `k_anonymity_test.py` script:
```bash
python k_anonymity_test.py
```

The script will perform k-anonymization for the specified k-values and save the anonymized datasets in the `data`/ directory with filenames like `anonymized_data_k_2.csv`, `anonymized_data_k_5.csv`, etc.

### 3. Measuring Utility

To measure the utility of the anonymized datasets, you can run the following command:
```bash
python k_anonymity.py
```

The utility scores for different k-values will be printed to the console.

## Results

The anonymized datasets can be found in the `data`/ directory. You can use these datasets for further analysis while considering the trade-off between privacy (k-anonymity) and utility.

## Acknowledgments
Luka Bagash

Haris Iqbal




