#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Cards Against Humanity CLI
A command line tool that completes sentences matching answer and question "cards" from the famous game

@author:     Simone Scarduzio
@copyright:  2014 Simone Scarduzio. 
@license:    Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) -  http://creativecommons.org/licenses/by-nc/3.0/
@contact:    scarduzio@gmail.com

CREDITS
 * The actual card game (http://cardsagainsthumanity.com/)
 * Somebody who put all the questions and answers in JSON format (nodanaonlyzuul@github)
 
'''
import urllib2
import json
import random
from HTMLParser import HTMLParser

CACHE_FILE = '/tmp/cau_cache.txt'
JSON_URL = 'https://raw.githubusercontent.com/nodanaonlyzuul/against-humanity/master/source/cards.json'

open(CACHE_FILE, "a").close()
cacheFile = open(CACHE_FILE, "r+")
jsonString = cacheFile.read()

if(len(jsonString) == 0):
  jsonString = urllib2.build_opener().open(urllib2.Request(JSON_URL)).read()
  cacheFile.write(jsonString)

cacheFile.close()
cards = json.loads(jsonString)

# Separate questions from answers and format them right
answers, questions = [],[]

for item in cards:
  text = HTMLParser().unescape(item['text'])
  if item['cardType'] == 'A':
    answers.append("[" +text[:-1] + "]")
  elif item['cardType'] == 'Q':
    questions.append(text)

# Recursively replace underscores with answers
def fillPlaceHolder(question):
  for idx, char in enumerate(question):
    if char == '_':
      return question[:idx] + random.choice(answers) + fillPlaceHolder(question[idx+1:])
    
  # Sometimes we have an interrogative sentence, then we have to placeholder and we have to put an answer at the end.
  if len(question) > 0 and question[-1] == '?':
    question += " " + random.choice(answers)

  return question

for i in range(150):
  print fillPlaceHolder(random.choice(questions))
