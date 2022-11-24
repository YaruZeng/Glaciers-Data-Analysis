# Glaciers Data Analysis 
The objective of the project is to write a program which enables users to read in and conduct data analysis of a real dataset of glaciers. The project is finished in UCL course 'MPHY0021 Research Software Engineering with Python' where only the Python standard library, matplotlib and pytest can be used. 

## Data sources
### 1. sheet-A.csv (1696 rows)

It has the basic information for each glacier with one row per glacier. The columns are, in order:

• political unit

• name

• identifier (WGMS_ID), made up of 5 digits

• general location (not of interest for this assignment) • specific location (not of interest for this assignment) 

• latitude, in degrees

• longitude, in degrees

• primary classification, encoded as a digit

• form, encoded as a digit

• frontal characteristics, encoded as a digit


The remaining columns are not of interest for this project.

### 2. sheet-E.csv (5306 rows)
It contains the mass-balance measurements taken across the years. It has one row per measurement. Each glacier can have data for multiple years. 

## Deliveries

### 1. glaciers.py
Two classes were built to enable users to 
#### 1) read in data,

#### 2) find the nearest glaciers to a given coordinates,

#### 3) get glaciers whose codes match the given pattern,

#### 4) get the glaciers with the highest area accumulated in the last measurement,

#### 5) plot the mass-balance measurements of a specified glacier against years,

#### 6) plot the mass-balance measurements of two glaciers against years which grew most and shrunk most at the latest measurement, 

#### 7) plot get a summary of the data analysis. 

Users can interact with the 'GlaciersCollection' class to call the functions to conduct data analysis.


### 2. utils.py
As with many real-world scientific datasets, the measurements can be inconsistent and contain errors. The file is constructed to raise errors with appropriate error messages when encountering data that appears to be wrong. 

### 3. test_glaciers.py
Tests were written in Pytest to verify the functions behave as expected in the file.

