from newspaper import Article
import random 
import string 
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')



def preprocess_data():
	# Download punkt package
	nltk.download('punkt', quiet=True) # sentence tokenizer

	# get an article to scrape
	article = Article("https://devskiller.com/history-of-programming-languages/")
	article.download()
	article.parse()
	article.nlp()
	corpus = article.text

	# print articles text
	# print(corpus)

	#tokenization
	text = corpus
	sentence_list = nltk.sent_tokenize(text) # this will give us a list of sentences
	# print(sentence_list)
	return text, sentence_list


def greet(text):
	text = text.lower()

	bot_greetings = ["Hello", "howdy", "hi", "hey", "wassup", "hola"]
	user_greetings = ["hi", "hey", "hello", "hola"]

	for word in text.split(): #might not need to make this a loop
		if word in user_greetings:
			return random.choice(bot_greetings)

def index_sort(myList):
	length = len(myList)
	list_idx = list(range(0, length))

	x = myList
	for i in range(length):
		for j in range(length):
			if x[list_idx[i]] > x[list_idx[j]]:
				list_idx[i], list_idx[j] = list_idx[j], list_idx[i]

	return list_idx


def bot_response(user_input, sentence_list):
	user_input = user_input.lower()
	sentence_list.append(user_input)
	bot_response = ''
	cm = CountVectorizer().fit_transform(sentence_list)
	similarity_scores = cosine_similarity(cm[-1], cm) # get last sentence (this is why we append) and then we compare it to the entire matrix
	similarity_scores_list = similarity_scores.flatten() # reduces dimensionality to a list
	index = index_sort(similarity_scores_list)
	index = index[1:] # this ensures we don't include the users input because we would get a 100% match
	response_flag = 0

	count = 0
	for i in range(len(index)):
		if similarity_scores_list[index[i]] > 0.0: 
			bot_response = bot_response + " " + str(sentence_list[index[i]])
			response_flag = 1
			count += 1

		if count > 2: 
			break
		
	if response_flag == 0:
		bot_response = bot_response + " " + "I apologize, I don't understand  :("

	sentence_list.remove(user_input)
	return bot_response 

def update_transcipt(time, user_input=""):

	with open("transcript.txt", "a") as convo: 
		convo.write(time + " " + str(user_input) + "\n")


	convo.close()
def main():

	text, sentence_list = preprocess_data()
	exit_list = ['bye', 'seeyalater', "quit", 'break', 'exit']
	current_date = datetime.now().strftime("%d/%m/%Y")

	update_transcipt("\t"*8 + "[" + current_date + "]" + "\n-------------------------------------------------------------------\n")
	print("I am bot version 0.1! I will answer your queries about Programming!")
	while True: 
		time = datetime.now().strftime("%H:%M:%S")
		user_input = input("> ")
		update_transcipt(time, user_input)
		if user_input.lower() in exit_list: 
			print("> BOT shutting down...")
			update_transcipt(time, "> bot shutting down...\n-------------------------------------------------------------------\n\n")
			break
		else: 
			if greet(user_input) != None: 
				print("BOT: " + greet(user_input))
				update_transcipt(time, "BOT: " + greet(user_input))
				
			else:
				print("BOT: " + bot_response(user_input, sentence_list))
				update_transcipt(time, "BOT: " + bot_response(user_input, sentence_list))

	

main()




