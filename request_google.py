import requests
import json


## This is a usage for crawling Google CSE search engine for CNN news
# ref = 'https://programmablesearchengine.google.com/about/'
# ref = 'https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python'

cse_id = 'your own search engine id'
api_key = 'your own key'

query = "entertainment"
page = 1

start = (page-1)*10+1
url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&start={start}"

# use request library
data = requests.get(url).json()
#print(data)

news = []

search_items = data.get("items")
for i, search_item in enumerate(search_items, start = 1):
	
	# get data
	title = search_item.get("title")
	snippet = search_item.get("snippet")
	html_snippet = search_item.get("htmlSnippet")
	link = search_item.get("link")

	# store data for dumping to JSON
	temp = {'Title': title, 'Description': snippet, 'Url': link}
	news.append(temp)
	print("="*10, f"Result #{i+start-1}", "="*10)
	print("Title:", title)
	print("Description:", snippet)
	print("URL:", link, "\n")

# store file
with open('./cnn.json', 'w') as cnn_data:
	json.dump(news, cnn_data)

