from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import random
import plotly.graph_objects as go

page_number = 1
total_length = 0
longest_quote = ''
shortest_quote = ''
most_quotes_author = most_quotes_num = 0
least_quotes_author = ''
least_quotes_num = 10000
quote_dict = {}
total_tag_count = 0
tag_counts = {}

for i in range(10):
    url = f"https://quotes.toscrape.com/page/{page_number}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    print(soup.title.text)

    quote_data = soup.findAll("div", attrs={"class": "quote"})
    for q in quote_data:
        quote = q.find("span", class_="text").text
        author = q.find("small", class_="author").text
        total_length += len(quote)
        num_quotes = len(quote_data)
        
        if author in quote_dict:
            quote_dict[author] += 1
        else:
            quote_dict[author] = 1
        
        if len(quote) > len(longest_quote):
            longest_quote = quote
        
        if shortest_quote == '' or len(quote) < len(shortest_quote):
            shortest_quote = quote
        
        tags = q.findAll("a", class_="tag")
        total_tag_count += len(tags)
        
        for tag in tags:
            tag_counts[tag.text] = tag_counts.get(tag.text, 0) + 1

    for author, count in quote_dict.items():
        if count == 1:
            print(f"{author}: {count} quote")
        else:
            print(f"{author}: {count} quotes")

        if count > most_quotes_num:
            most_quotes_author = author
            most_quotes_num = count

        if count < least_quotes_num:
            least_quotes_author = author
            least_quotes_num = count

    page_number += 1

most_popular_tag = max(tag_counts, key=tag_counts.get)
print("\n---Author Statistics---")
print(f"Author with the most quotes: {most_quotes_author} with {most_quotes_num} quotes")
print(f"Author with the least quotes: {least_quotes_author} with {least_quotes_num} quotes\n")
print("---Quote Analysis---")
print(f"Average length of a quote: {total_length / num_quotes} characters")
print(f"Longest quote: {longest_quote}")
print(f"Shortest quote: {shortest_quote}\n")
print("---Tag Analysis---")
print(f"Most popular tag: '{most_popular_tag}'")
print(f"Total tags: {total_tag_count}")

# Visualization
print("\nVisualization:")

# Plot for authors with quotes
sorted_authors = sorted(quote_dict.items(), key=lambda x: x[1], reverse=True)
top_authors = [author[0] for author in sorted_authors[:10]]
top_quotes = [author[1] for author in sorted_authors[:10]]
fig = go.Figure(data=[go.Bar(x=top_authors, y=top_quotes)])
fig.update_layout(title="Top 10 Authors by Number of Quotes", xaxis_title="Author", yaxis_title="Number of Quotes")
fig.show()

# Plot for tags
sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
top_tags = [tag[0] for tag in sorted_tags[:10]]
top_tag_counts = [tag[1] for tag in sorted_tags[:10]]
fig = go.Figure(data=[go.Bar(x=top_tags, y=top_tag_counts)])
fig.update_layout(title="Top 10 Tags by Popularity", xaxis_title="Tag", yaxis_title="Popularity")
fig.show()
