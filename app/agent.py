import time
import json
import datetime
import re

from apiRequester import ApiRequester

class Agent:
    '''
    Main class to retrieve data from Semantic Scholar Graph API
    '''

    def __init__(self, offset=0, limit=50):
        self._offset = offset ## 목록의 시작 위치
        self._limit = limit ## 반환할 최대 결과 수

        self._requester = ApiRequester()

    def get_papers(self, query) -> list:

        results = dict()
        papers = list()
        refers = dict()

        param = f'search?limit={self._limit}&query={query["keywords"]}&year={query["year"]}&fieldsOfStudy={query["field"]}'\
                '&fields=title,publicationDate,authors,abstract,citationCount,year,citationStyles,references.title,references.year,references.referenceCount'
#        param = f'search?limit={self._limit}&query={query["keywords"]}&year={query["year"]}&fieldsOfStudy={query["field"]}&fields=year,publicationDate,citationStyles,references.title,references.year,references.referenceCount'
       
        papers = self._requester.get_data(param, "search")

        if 'data' not in papers:
            papers = list()
            return papers ## Error Message

        papers = papers['data']

        ## references processing
        refers = self.get_reference(papers)
        results['refer'] = refers
        
        ## delete useless key-value
        for items in papers:
            if 'references' in items:
                del items['references']

        pattern = r'\[[^()]*\]|None'
        ## change bibtex type entries
        for items in papers:
            bibtex = items["citationStyles"]["bibtex"]
            bibtex = re.sub(pattern, 'article', bibtex)
            items["citationStyles"]["bibtex"] = bibtex

        papers = self.sorting(papers, query['sort'])
        results['data'] = papers

        return results

    def get_citations(self, paper_id):
        '''
        citation paper id
        contents only intents = 'background'
        '''
        #TODO: case1: No CitatingPaper Found

        results = list()

        #url = self.api_url
        param = f'{paper_id}/citations?offset=0&limit=40&fields=paperId,contexts'
        citations = self._requester.get_data(param, "citations")

        print(json.dumps(citations, indent=4))

        if 'is_error' in citations:
            return results

        for data in citations['data']: 
            if data['contexts']:
                results.append(data)

        return results

    def get_reference(self, papers):
        results = list()
        refers = dict()

        for paper in papers:
            for refer_paper in paper['references']:
                if refer_paper['paperId'] is None: #TODO: None
                    continue
                if refer_paper['paperId'] not in refers:
                    refers[refer_paper['paperId']] = dict()
                    refers[refer_paper['paperId']]["paperId"] = refer_paper['paperId']
                    refers[refer_paper['paperId']]["title"] = refer_paper['title']
                    refers[refer_paper['paperId']]["year"] = refer_paper['year']
#                    refers[refer_paper['paperId']]["referenceCount"] = refer_paper['referenceCount']
                    refers[refer_paper['paperId']]['referenceCount'] = 0
                refers[refer_paper['paperId']]['referenceCount'] += 1
        
        results = sorted(refers.items(), key=lambda x:x[1]['referenceCount'] or 0, reverse=True)
        results = dict(results[:3])

        results = list(results.values())
       
#        results = list()
#        refers = dict()
#
#        for paper in papers:
#            for refer_paper in paper['references']:
#                if refer_paper['paperId'] is None:
#                    continue
#                if refer_paper['paperId'] not in refers:
#                    refers[refer_paper['paperId']] = 0
#                refers[refer_paper['paperId']] += 1
#
#        results = sorted(refers.items(), key=lambda x:x[1], reverse=True)
#        results = dict(results[:3])
        print(json.dumps(results, indent=4))
        return results

    def sorting(self, papers, sort) -> list:

        if sort == "Latest":
            with_year = dict()
            for item in papers:
                temp = list()
                temp = [item["year"], item["publicationDate"], item]
                if item["year"] not in with_year:
                    with_year[item["year"]] = list()
                with_year[item['year']].append(temp)

            for year in with_year:
                year_list = list()
                null_list = list()
        
                for item in with_year[year]:
                    if item[1] is None:
                        null_list.append(item)
                        continue
                    year_list.append(item)
                year_list = sorted(year_list, key=lambda x:x[1] or "null",  reverse=True)
                
                for item in null_list:
                    item[2]["publicationDate"] = item[0]

                new_list = year_list+null_list
                with_year[year] = new_list

            with_year = sorted(with_year.items(), reverse=True)
            with_year = dict(with_year)

            papers = list()
            for year in with_year:
                for i in with_year[year]:
                    papers.append(i[2])
        else: 
#        if sort == "Latest":
#            papers = sorted(sorted(papers, key=lambda d:d['publicationDate'] or "null", reverse=True), key=lambda d:d['year'] or "null", reverse=True)

#        elif sort == "Number of citationsi":
            print(sort)
            papers = sorted(papers, key=lambda d:d['citationCount'], reverse=True)

        return papers


def main():
    count = 0

    query = {
            'keywords': 'chatGPT',
            'field': 'Computer Science',
            'year': '2020-2023',
            'sort': 'Latest'
            }

    paper_id = 'd6ecce76d7f72269bc78a8b29ad322623b8aa7c1'
    paper_id = 'df2b0e26d0599ce3e70df8a9da02e51594e0e992'

    api = Agent()

    start = time.time()
    papers = api.get_papers(query)
    #citations = api.get_citations(paper_id)
    #print(json.dumps(papers, indent=4))
    for paper in papers['data']:
        print(paper['publicationDate'])
    print(time.time()-start)   

if __name__ == '__main__':
    main()



