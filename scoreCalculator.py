import sys
import json
import csv
from pattern.en import lexeme
from collections import OrderedDict
from operator import itemgetter
import re

def main():
	#Book (JSON file)
	book_file = sys.argv[1]

	#Keywords (CSV file)
	keywords_file = sys.argv[2]

	with open(book_file) as json_file:
		books = json.load(json_file)

	#dicts to store keyword values
	genres = {}

	with open(keywords_file) as csv_file:
		keywords = csv.reader(csv_file, delimiter = ',')
		for row in keywords:
			try:
				genre = str(row[0])
				word = str(row[1])
				points = int(row[2]) #if this doesn't work, it means it's an invalid row

				if word[0] == ' ':
					word = word[1:]

				if "u'" in genre[:3]:
					genre = genre[2:]

				if "u'" in word[:3]:
					word = word[2:]			

				# If a keyword appears twice in the same genre, keep the record with maximum points
				if genre in genres.keys():
					repeated = False
					
					for v in genres[genre]:
						if v[0] == word:
							repeated = True

					if repeated is False:
						genres[genre].append([word, points])

					else:
						for v in genres[genre]:
							if v[0] == word:
								if v[1] < points:
									genres[genre].pop(genres[genre].index(v))
									genres[genre].append([word, points])

						
				else:
					genres[genre] = [[word, points]]

			except ValueError:
				continue

	output = {}
	for each in books:
		genre_scores = keywordChecker(each, genres)
		output[each['title']] = outputStorer(each, genre_scores)

	printer(output)

# -- end main --

def keywordChecker(book, genres):

		genre_scores = {}
		for each in genres.keys():
			genre_scores[each] = []

		for genre, words in genres.items():

			found = []
			#words is list of words in each genre

			for wd in words: #for each word in a list
				word =  wd[0]
				
				#wd[1] is the point value of that word

				for a in re.finditer(word, book['description']):
					genre_scores[genre].append(wd[1]) ## WORKING HERE AND THE newL part
					found.append(a.group(0))

				# There can also be other forms of a root word. For example, 'fought' is a form of 'fight'.
				# Use the NLP module pattern.en to call lexeme(word) to get the list of possible forms of that word. Works for 2 word keywords too
				allWords = lexeme(word)
				for each in allWords:
					if word not in each:
						if each in book['description']:
							genre_scores[genre].append(wd[1])
							found.append(each)

		# now, calculate score averages	
		# save score averages as last value in dict for each genre
		for k,v in genre_scores.items():
			if len(v) != 0:
				genre_scores[k].append(len(v) * int(sum(v)/len(v)))

		return genre_scores

# -- end keywordChecker --

def outputStorer(book, genre_scores):

	#print only the 3 records with most points

	genre_avgs = {}

	for genres, vals in genre_scores.items():
		if len(vals) > 0:
			genre_avgs[genres] = vals[len(vals)-1]
		else:
			genre_avgs[genres] = 0

	sorted_ga = OrderedDict( sorted(genre_avgs.items(), key=itemgetter(1), reverse = True) )

	out = []

	for genres, vals in sorted_ga.items():
		out.append((genres.title() + ', ' + str(vals)))

	return out

# -- end outputStorer --

def printer(output):

	# sort output in alphabetical order of movie titles
	output_sorted = OrderedDict(sorted(output.items(), key=itemgetter(0)))

	for k, v in output_sorted.items():
		print k
		
		count = 3
		for genre_record in v:
			if count == 0:
				break
			print genre_record
			count -= 1
		print '\n'

# -- end printer --

if __name__ == "__main__":
	main()
