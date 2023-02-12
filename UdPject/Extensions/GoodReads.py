from lxml import html
import requests
def Gquote(search,number):
    search.replace(" ","+")
    quotes_page = requests.get('https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q='+search)
    data = []
    tree = html.fromstring(quotes_page.content)
    

    for quote_div in tree.xpath('//div[@class="quoteText"]'):
        if(number != None):
            if(len(data)>number-1):
                return data
        quote_text = quote_div.xpath('text()')[0].strip()
        author = quote_div.xpath('a/text()')[0].strip()
        data.append((quote_text,author))
    return data
