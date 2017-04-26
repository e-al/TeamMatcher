from __future__ import print_function
import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
import numpy as np
import pandas as pd
import nltk
import re


from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from sklearn import mixture


#projdesc = open('group1/group1.dat').read().splitlines()
numclusters = 12
vocabs = np.genfromtxt('TeamMatcher/recommender/vocab.nips.txt',dtype='str')
stopwords = nltk.corpus.stopwords.words('english')

def preprocess(descriptions):
    
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    
    for i in descriptions:
        allwords_stemmed = tokenize_and_stem(i.decode('utf-8')) #for each item in 'synopses', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list

        allwords_tokenized = tokenize_only(i.decode('utf-8'))
        totalvocab_tokenized.extend(allwords_tokenized)

    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
    print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
    return vocab_frame 
    
    

def getMeClusters(descriptions): 

    projid = list(range(len(descriptions)))
    
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                             min_df=0.2, stop_words=stopwords,
                             use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,1),vocabulary=vocabs)
                             
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions) #fit the vectorizer to synopses

    terms = tfidf_vectorizer.get_feature_names()

    em = mixture.GaussianMixture(n_components=numclusters)
    
    em.fit(tfidf_matrix.toarray())
    
    clusters = em.predict(tfidf_matrix.toarray()).tolist()

    projects = { 'project id': projid, 'project description': descriptions, 'cluster': clusters }

    frame = pd.DataFrame(projects , columns = [ 'project id', 'cluster','project description'])

    frame['cluster'].value_counts()
    
    
    vocab_frame = preprocess(descriptions)
    
    order_centroids = em.means_.argsort()[:, ::-1] 


    for i in range(numclusters):
        
        for ind in order_centroids[i, :10]: #replace 6 with n words per cluster
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
        print() #add whitespace
        print() #add whitespace
       

        print("Cluster %d project id:" % i, end='')
        for teams in frame.loc[frame['cluster']==i]['project id']:
            print(' %s,' % teams, end='')
        print() #add whitespace
        print() #add whitespace
    
    frame.to_csv(path_or_buf='clusters.csv')
    return frame



def searchMeTeams(pastprojects=None,skills=None,interests=None):
    
    if(pastprojects == None and skills == None and interests == None):
        return []
    
    clusters = pd.read_csv('TeamMatcher/recommender/clusters.csv')
    
    if(pastprojects is None):
        pastprojects =['']
    else:
        pastprojects = [pastprojects]
    
    if(skills is None):
        skills =['']
    else:
        skills = [skills]
        
    if(interests is None):
        interests =['']
    else:
        interests = [interests]
        
    ret_id = []
    
    vocabs = np.genfromtxt('TeamMatcher/recommender/vocab.nips.txt',dtype='str')
    allscores = []
    tfidf_vectorizer = TfidfVectorizer(max_df=1, max_features=200000,
                    min_df=0, stop_words=stopwords,
                    use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,1),vocabulary=vocabs)
    
    tfidf_pastprojects = tfidf_vectorizer.fit_transform(pastprojects) #fit the vectorizer to synopses
    tfidf_skills = tfidf_vectorizer.fit_transform(skills) #fit the vectorizer to synopses
    tfidf_interests = tfidf_vectorizer.fit_transform(interests) #fit the vectorizer to synopses

    for i in range(numclusters):
        tfidf_Documents = tfidf_vectorizer.fit_transform(clusters.loc[clusters['cluster']==i]['project description']) #fit the vectorizer to synopses
        score_pastprojects = np.dot(tfidf_Documents.toarray(),np.transpose(tfidf_pastprojects.toarray()))
        score_skills = np.dot(tfidf_Documents.toarray(),np.transpose(tfidf_skills.toarray()))
        score_interests = np.dot(tfidf_Documents.toarray(),np.transpose(tfidf_interests.toarray()))
        
        score = score_pastprojects + 1.2*score_skills + score_interests
        
        allscores.append(np.mean(score))
    
    bestclusters = np.argsort(allscores)[::-1][0:3] #np.argmax(allscores)
    print()
    print(bestclusters)
    print()
    for i in bestclusters: 
        ret_id = ret_id+list(clusters.loc[clusters['cluster']==i]['project id'])
    return ret_id[0:10  ]
        
def searchMeStudents(query,interests):
    query = [query]
    vocabs = np.genfromtxt('vocab.nips.txt',dtype='str')
    allscores = []
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                    min_df=0.2, stop_words=stopwords,
                    use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,1),vocabulary=vocabs)

    tfidf_Documents = tfidf_vectorizer.fit_transform(interests) #fit the vectorizer to synopses
    tfidf_Queries = tfidf_vectorizer.fit_transform(query) #fit the vectorizer to synopses

    scores = np.dot(tfidf_Documents.toarray(),np.transpose(tfidf_Queries.toarray()))
    return np.argsort(scores[:,0])[::-1] #np.argmax(allscores)  

    
def tokenize_and_stem(text):
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

