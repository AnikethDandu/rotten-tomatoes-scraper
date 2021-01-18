# Rotten Tomatoes Scraper
[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)

A Python CLI tool that returns a list of top rated movies from the [Rotten Tomatoes Website](https://www.rottentomatoes.com).

## Installation
Make sure you have installed git. Run the following command in your desired project directory to get the scripts on your computer.
```bash
git clone https://github.com/AnikethDandu/rotten-tomatoes-scraper.git
```

## Usage
Inside your project directory, navigate inside the RottenTomatoesScraper directory. Once inside, run the following command:
```bash
Python3 main.py [-l] [-g] [-h]
```

## Features
### Command-line arguments
* --length, -l
  * Specify number of Top 100 movies to get. Can only choose from 0 - 100
* --genre, -g
  * Specify genre of movies to get
* --year, -y
  * Specify year to get movies from. <b>Cannot specify both year and genre. Only specify one or the other</b>
