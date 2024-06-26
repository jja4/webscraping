## Web Scraping Tool for Creating Contact Lists

This project is a web scraping tool designed to extract contact information, such as names, phone numbers, and email addresses, from various websites. The tool utilizes the Scrapy framework and can be used to create comprehensive contact lists or databases for various purposes, such as lead generation, market research, or data analysis.

The tool is designed to be user-friendly and can be easily configured to scrape specific websites or search for specific keywords. It leverages the power of Google search to identify relevant websites and then crawls those websites to extract the desired contact information.

The extracted data is saved in a CSV file, which can be easily imported into spreadsheet software or databases for further analysis or processing.


## Getting Started
### Prerequisites
Things required to get started:
1. Download Miniconda3
(https://docs.conda.io/en/latest/miniconda.html#windows-installers)
2. Download Git Bash (https://gitforwindows.org/)
3. Clone repository by opening Git Bash, change directories (cd) to the desired install
location/path (perhaps your Documents folder), then:
  ```python
  git clone https://github.com/jja4/webscraping.git
  ```
4. Change directories (cd) to Scrapy_Emails_Phone_Numbers folder
  ```python
  cd Scrapy_Emails_Phone_Numbers
  ```
5. Install all required packages, open Anaconda Prompt, then:
  ```python
  conda env create -n webscraping --file environment.yml
  ```
6. Activate the webscraping environment
  ```python
  conda activate webscraping
  ```
7. Run the following command to install a language processing AI model
  ```python
  python -m spacy download en_core_web_sm --user
  ```
### Basic Usage
1. If not already open, open Anaconda prompt, then:
```python
conda activate webscraping
```
2. cd to the location/path where the repository was installed (don’t copy exactly below)
```python
cd path/to/webscraping/Scrapy_Emails_Phone_Numbers
```
3. Start the scrapy crawler script:
```python
scrapy crawl emailspider -o output.csv
```
Alternative commands
To overwrite an existing output.csv file
```python
scrapy crawl emailspider -O output.csv
```
To save to a new file with a different name
```python
scrapy crawl emailspider -o new_name.csv
```
4. Start the search with your google search query. For example:
```python
machine learning companies germany
```

### Advanced Usage
To change the number of Google search results pages to scrape:
On Line ~43 of emailspider.py, change “results_pages_to_scrape = 1” to
“results_pages_to_scrape = 5“ or another number other than 5
To update the code to the latest version:
1. Open Git Bash, change directory to the Scrapy Tool project:
```python
cd ‘/path/to/webscraping/Scrapy_Emails_Phone_Numbers’
```
2. Download the new code
```python
git pull
```
3. Open Anaconda Prompt, update the environment by:
```python
conda activate webscraping
conda env update -f environment.yml --prune
```
### Keywords to use:
To search for phone numbers, use these keywords:

  Phone number, contact, telephone, +49 or other relevant country codes

For emails:

  Email, contact

For prices:

  Price, product code, cost

To search for company revenues, use these keywords:

  Revenue, financials, annual report, investments or income statement

![](Scrapy_Emails_Phone_Numbers/input.png)

The search and crawling process will take quite a while as it retrieves maximum results from Google & try to crawl all of them.
After the process finished, you can see output in specified file

![](Scrapy_Emails_Phone_Numbers/output.png)


## Troubleshooting
If you run into the problem where the scrapy code executes, but you do not get any results,
with output similar to this:

![](Scrapy_Emails_Phone_Numbers/blocked_ouput.PNG)


Here is the solution:

Open the settings.py file in
“webscraping\Scrapy_Emails_Phone_Numbers\emailcrawler\settings.py”

On line 20 or so, change:

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
like Gecko) Chrome/61.0.3163.100 Safari/537.36'

to

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
like Gecko) Chrome/89.0.4389.82 Safari/537.36'

Save the file, and try again.

If still having trouble try a higher number like 91.0.4389.82 until it works again. The first
number should be between 61 and 113, these are the versions of Chrome.

## Built With

* [Scrapy](https://scrapy.org/) - The main framework for this crawler

## Contributing

Feel free to submit pull requests to me.


## Authors

* **Joel Aftreth**   *Initial work* - [Muhammad Haseeb]


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
