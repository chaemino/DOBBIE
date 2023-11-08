import json
import logging
import datetime
import random

from agent import Agent
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello World!'

@app.route('/citations/mainpage', methods=['POST']) ## POST로 
def search():

    result = dict()
    query = dict() ## paper search information

    data = request.get_json() ## from frontend
    print(data)

    ## keywords
    keywords = data['keywords']
    query['keywords'] = keywords.replace(' ', '+')
    print(query['keywords'])
    if not keywords:
        return "At Least 2 Keywords", 400

    ## date range
    date = dict()
    currentDateTime = datetime.datetime.now()
    date_ = currentDateTime.date()
    date_dict = {
            'This year': 1,
            'Last 5 years': 5,
            'Last 10 years': 10
            }
    past = date_dict[data['dateRange'].strip()]
    query['year'] = f"{date_.year-past}-{date_.year}" 
    print(query['year'])

    ## sort option
    sort = data['sortingmethod'] ## Latest, Numbers of Citation
    #if sort == 'Latest':
    #    sort = 'pub-date'
    #else:
    #    sort = 'total-citations'
    query['sort'] = sort
    print(query['sort'])

    ## field 
    field = data['fieldsOfStudy']
    query['field'] = field
    print(query['field'])

    #print('from client: ', query, field, date, sort, flush=True)
    print('from client: ', keywords, field, date, flush=True)

    api = Agent()
    papers = list()
    #TODO: recover for using pai
    result = api.get_papers(query)

    print(result, flush=True)
 
    return jsonify(request='success', result=result) ## return what?

@app.route('/citations/mainpage/citation', methods=['POST'])
def citations():

    result = list()
    data = request.get_json()

    paper_id = data['paperId']
    print(paper_id)
    api = Agent()
    result = api.get_citations(paper_id)

    print(result, flush=True)

    return jsonify(request='success', result=result) ## return what?


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
