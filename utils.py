import re
import csv
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from spacy.matcher import Matcher
import pdfplumber


# Load the Spacy English model
nlp = spacy.load('en_core_web_sm')


def extract_text_from_pdf(uploaded_file):

    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    
def _create_matcher():
    # Read skills from CSV file
    file_path='data\skills.csv'
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        skills = [row for row in csv_reader]

    # Create pattern dictionaries from skills
    skill_patterns = [[{'LOWER': skill}] for skill in skills[0]]

    # Create a Matcher object
    matcher = Matcher(nlp.vocab)

    # Add skill patterns to the matcher
    for pattern in skill_patterns:
        matcher.add('Skills', [pattern])
    
    return matcher

# Function to extract skills from text
def extract_skills(text):
    doc = nlp(text)
    matcher = _create_matcher()
    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text
        skills.add(skill)
    return list(skills)




def _ngrams(string, n=3):
    # string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]


    
def recommend_jobs(skills):
    # Loading jobs dataset:
    jd_df=pd.read_csv('data\jobs.csv')

    vectorizer = TfidfVectorizer(min_df=1, analyzer=_ngrams, lowercase=False)
    tfidf = vectorizer.fit_transform(skills)

    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
    jd_test = (jd_df['Processed_JD'].values.astype('U'))

    def getNearestN(query):
        queryTFIDF_ = vectorizer.transform(query)
        distances, indices = nbrs.kneighbors(queryTFIDF_)
        return distances, indices

    distances, indices = getNearestN(jd_test)
    matches = []

    for i,j in enumerate(indices):
        dist=round(distances[i][0],5)
    
        temp = [dist]
        matches.append(temp)
        
    matches = pd.DataFrame(matches, columns=['Match confidence'])

    # Following recommends Top 5 Jobs based on candidate resume:
    jd_df['Match Confidence']=matches['Match confidence']
    return jd_df.sort_values('Match Confidence',ascending=[False]).head(10)