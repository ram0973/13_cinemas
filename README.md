# Task [№13](https://devman.org/challenges/13/) from [devman](https://devman.org)
## Desription
The script displays the most popular movies going at the moment,
sorted by rating.
Additionally you can drop a movies screeining in a small number of cinemas, 
by choosing the cinemas count. 
And you can choose the movies count, default is 20 movies.
Script parses information from the mobile site and XML API, 
because this method is fast and stable.
## Requirements
```
Python 3.5.2+
beautifulsoup4
lxml
requests
tqdm
```
## Setup
```    
git clone https://github.com/ram0973/13_cinemas.git
cd 13_cinemas
pip3 install -r requirements.txt
```
## Usage
```
python3 cinemas.py --movies 15 --cinemas 5
```
## License
[MIT](http://opensource.org/licenses/MIT)