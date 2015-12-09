# identify-book-genres
####Tool to help go through a list of books and identify the correct genre for each book. 

**Approach:**
* The program analyzes the description of each book and calculates a score based on the presence of certain genre-specific keywords.
* A point value is given to each expected key words (keywords are in a CSV file)
* The genre-fit score is calculated as: total num keyword matches * avg point value of the unique matching keywords
* Book titles are printed alphabetically, with their three highest scoring genres and their respective scores.

**Inputs:**
* JSON representation of books is: [{'title': ...., 'description':....}, {'title': ...., 'description':....},...]
* In CSV file, use the representation: genre, keyword, point-value

**Output Format:**  
Movie title  
genre1, score  
genre2, score  
genre3, score  
