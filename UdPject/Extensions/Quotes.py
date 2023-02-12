def links(search):
    search=str(search)
    import requests
    from bs4 import BeautifulSoup as bs

    links=[]
    if(search == None):
        login_url ="https://www.brainyquote.com/search_results.html?q=albert+einstein"
    else:
        search.replace(" ","+")
        login_url ="https://www.brainyquote.com/search_results.html?q="+search
    first="https://www.brainyquote.com"
    result = requests.get(login_url)
    soup=bs(result.text,"html.parser")
    
    for quote in soup.find_all('a', {'title': 'view image'}):
        for img in (quote("img")):
            links.append(first+img.get("src"))
    return links
