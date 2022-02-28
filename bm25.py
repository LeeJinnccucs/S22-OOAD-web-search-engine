import nltk
import pandas as pd

# use BM25 for indexing
from rank_bm25 import *

import json
import re

# init nltk tools

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
ps = PorterStemmer()

#download punkt when first time usage
#nltk.download('punkt')

stop_words = set(stopwords.words('english'))

# preprocessing, could be put to utils.py afterwards
class Preprocessing:
	
	# tokenization
	def tokenize(self,text):
		return word_tokenize(text)

	# re removing none alphanumeric characters
	def spl_chars_removal(self,text):
		result = ''
		result = re.sub("[^0-9a-zA-Z ]+"," ",text)
		return result 

	# tokenization + remove special char + lower + stopword + stemming
	def preprocess(self,text):
		clean_text = self.spl_chars_removal(text)
		tok_text = self.tokenize(clean_text)
		pre_text = [ps.stem(word.lower()) for word in tok_text if word.lower() not in stop_words]
		return pre_text

# corpus class, store data
class corpus:

	def __init__(self, file_dir):
		self.file_dir = file_dir
		self.utils = Preprocessing()	
		self.index_movie, self.processed_corpus = self.get_processed_data(self.file_dir)
		self.bm_25 = None

	# get processed text, index-movie dictionary
	def get_processed_data(self, file_dir):
		with open(file_dir) as movies_file:
			movies = json.load(movies_file)
		index_dic = {}
		processed = []
		for index,movie in enumerate(movies):
			index_dic[index] = movie['name']
			pre_text = self.utils.preprocess(movie['plot'])
			movie['plot'] = pre_text
			processed.append(movie['plot'])
		return index_dic, processed

	# create BM25 Object
	def create_bm25(self, processed_data):
		return BM25Okapi(processed_data)

	# print query result
	def query_result(self, Query):
		query = self.utils.preprocess(Query)
		score = self.bm_25.get_scores(query)
		max_indexs = np.argpartition(score, -5)[-5:]
		top5_index = max_indexs[np.argsort(score[max_indexs])]
		print("="*10, f"Query: {Query}", "="*10)
		for i in top5_index:
			print("index:{}, movie_name:{}".format(i, self.index_movie[i]))

def main():
	file_dir = 'movie.json'
	movies = corpus(file_dir)
	movies.bm_25 = movies.create_bm25(movies.processed_corpus)
	query = 'hero'
	movies.query_result(query)
	
if __name__ == "__main__":
	main()
