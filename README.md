# NeuroDataResource
NeuroDataResource is a python wrapper for [Intern](https://github.com/jhuapl-boss/intern) for interfacing with BOSS. 

## Contents
- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Usage](#usage)

## Overview
**NeuroDataResource** is a tool for interfacing with BOSS, primarily for downloading data from it. It is powered by [Inter](https://github.com/jhuapl-boss/intern).

## System Requirements
  - **NeuroDataResource** was developed in Python 3.6. Currently, there is no plan to support Python 2.
  - Requires no non-standard hardware to run.

The following lists the dependencies for **NeuroDataResource**. It is very robust, and only requires two packages

```
numpy>=1.13.1
intern>=0.9.4
```

## Usage Guide
**NeuroDataResource** can be installed via Github as shown below. 

### Clone the repository from Github

    git clone https://github.com/neurodata-nomads/neurodataresource
    

### Demo
It is **_highly_** recommended that you use **PyMEDA** inside Jupyter notebook, which allows **PyMEDA** visualizations to be easily embedded. However, **PyMEDA** also supports embedding in static HTML pages. 

Please see [demo](https://github.com/neurodata-nomads/pymeda/blob/master/notebooks/Demo.ipynb "PyMEDA demo using iris dataset")
 here to view the usages using the iris dataset.