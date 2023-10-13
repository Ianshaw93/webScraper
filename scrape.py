import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kneesovertoesguy.medium.com/"

def get_article_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all <article> tags
    articles = soup.find_all('article')
    
    # Extract the href attribute from the nested <a> tags within each <article>
    article_links = [article.find('a', href=True)['href'].split('?')[0] for article in articles if article.find('a', href=True)]
    
    return article_links

def get_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Navigate through <article>, <section>, and <div> tags
    article_tag = soup.find('article')
    if article_tag:
        section_tag = article_tag.find('section')
        if section_tag:
            paragraphs = section_tag.find_all('p')
            return ' '.join(p.text for p in paragraphs)
    return ""

# TODO: create object with each article content, link and title
def main():
    article_links = get_article_links()
    article_objects = []
    for link in article_links:
        if link == article_links[0]:
            title = link[1:-13]
            full_link = BASE_URL + link
            text = get_article_text(full_link)
            article_objects.append({
                                    "title": title, 
                                    "link": full_link, 
                                    "text": text
                                    })
            print(text)
    import json
    # write to data.txt
    with open('single_blog.txt', 'w') as f:
        json.dump(article_objects, f)
    return article_objects

if __name__ == "__main__":
    articles = main()   
