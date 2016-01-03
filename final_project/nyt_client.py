import http.client, urllib.parse
import json
import base64
from pprint import pprint
from collections import Counter

NYTSEARCH_KEY = 'c3a712f9587a97bc584a76df1fef5664:9:72962549'
NYTTAGS_KEY = '66e62094aa65abba8e843ecd98ede1b1:7:72962549'
NYTPOPULAR_KEY = 'd058a36f897d68b2167470dc46767279:15:72962549'
NYTTIMESWIRE = 'f15b3e6e4cb273fae2ca6c97f2f650c2:8:72962549'
NYT_HOST = 'api.nytimes.com'
TAGS_PATH = '/svc/suggest/v1/timestags'
SEARCH_PATH = '/svc/search/v2/articlesearch.json'
POPULAR_PATH = '/svc/mostpopular/v2/mostshared/all-sections/1.json'
TIMESWIRE_PATH = '/svc/news/v3/content/all'

sections_list = [{"section":"admin","display_name":"Admin"},{"section":"arts","display_name":"Arts"},{"section":"automobiles","display_name":"Automobiles"},{"section":"blogs","display_name":"Blogs"},{"section":"books","display_name":"Books"},{"section":"booming","display_name":"Booming"},{"section":"business day","display_name":"Business Day"},{"section":"corrections","display_name":"Corrections"},{"section":"crosswords & games","display_name":"Crosswords & Games"},{"section":"crosswords\/games","display_name":"Crosswords\/Games"},{"section":"education","display_name":"Education"},{"section":"fashion & style","display_name":"Fashion & Style"},{"section":"feeds","display_name":"Feeds"},{"section":"food","display_name":"Food"},{"section":"giving","display_name":"Giving"},{"section":"global home","display_name":"Global Home"},{"section":"great homes & destinations","display_name":"Great Homes & Destinations"},{"section":"health","display_name":"Health"},{"section":"home & garden","display_name":"Home & Garden"},{"section":"homepage","display_name":"Homepage"},{"section":"international home","display_name":"International Home"},{"section":"job market","display_name":"Job Market"},{"section":"learning","display_name":"Learning"},{"section":"magazine","display_name":"Magazine"},{"section":"membercenter","display_name":"membercenter"},{"section":"movies","display_name":"Movies"},{"section":"multimedia","display_name":"Multimedia"},{"section":"multimedia\/photos","display_name":"Multimedia\/Photos"},{"section":"n.y. \/ region","display_name":"N.Y. \/ Region"},{"section":"none","display_name":"none"},{"section":"nyt now","display_name":"NYT Now"},{"section":"nytfrontpage","display_name":"nytfrontpage"},{"section":"obituaries","display_name":"Obituaries"},{"section":"open","display_name":"Open"},{"section":"opinion","display_name":"Opinion"},{"section":"public editor","display_name":"Public Editor"},{"section":"real estate","display_name":"Real Estate"},{"section":"science","display_name":"Science"},{"section":"sports","display_name":"Sports"},{"section":"style","display_name":"Style"},{"section":"sunday review","display_name":"Sunday Review"},{"section":"t magazine","display_name":"T Magazine"},{"section":"t:style","display_name":"T:Style"},{"section":"technology","display_name":"Technology"},{"section":"the upshot","display_name":"The Upshot"},{"section":"theater","display_name":"Theater"},{"section":"times insider","display_name":"Times Insider"},{"section":"times topics","display_name":"Times Topics"},{"section":"timesselect","display_name":"timesselect"},{"section":"topics","display_name":"Topics"},{"section":"travel","display_name":"Travel"},{"section":"u.s.","display_name":"U.S."},{"section":"urbaneye","display_name":"UrbanEye"},{"section":"washington","display_name":"Washington"},{"section":"week in review","display_name":"Week in Review"},{"section":"world","display_name":"World"},{"section":"your money","display_name":"Your Money"}]
search_section = []

encoding = 'utf-8'





def getQueryRecent( query_term ):
	connection = http.client.HTTPConnection( NYT_HOST )
	query = {'q': query_term, 'sort': 'newest', 'hl': 'true','facet_field': 'section_name', 'api-key': '%s' %NYTSEARCH_KEY}
	
	connection.request( 'GET', SEARCH_PATH+'?'+urllib.parse.urlencode(query))
	try:
		response = connection.getresponse()
		decoded_response = response.read().decode(encoding)
		result_dict = json.loads(decoded_response)['response']
		article_dict = filterResult(result_dict)
		# json_response = json.dumps(response_dict)
	except:
		return []

	return article_dict

def getTimesWire():
	global search_section
	connection = http.client.HTTPConnection( NYT_HOST )
	newswire_list = []
	c = Counter()
	for section in search_section:
		c[section] +=1
	section_search = c.most_common()[0]

	search_section = []


	query = {'limit': 10, 'api-key': '%s'%NYTTIMESWIRE}
	connection.request( 'GET', TIMESWIRE_PATH+'/'+section_search[0]+'/5.json?'+urllib.parse.urlencode(query))

	response = connection.getresponse()
	decoded_response = response.read().decode(encoding)
	result = json.loads(decoded_response)['results']
	search_section

	for key in result:
		temp = {}
		temp['web_url'] = key['url']
		temp['headline'] = key['title']
		temp['snippet'] = key['abstract']
		temp['pub_date'] = key['published_date']
		temp['section_tag'] = key['section']
		newswire_list.append(temp)
	return newswire_list



def filterResult(result_dict):
	news_stories = []
	result_hits = result_dict['docs']

	#{stories: [{url:, headline:, snippet:,}]}
	for hit in result_hits:
		temp = {}
		temp['headline'] = hit['headline']['main']
		temp['snippet'] = hit['snippet']
		temp['web_url'] = hit['web_url']
		temp['pub_date'] = hit['pub_date']
		temp['section_tag'] = hit['section_name']
		search_section.append(hit['section_name'])
		news_stories.append(temp)

	return news_stories

def getTags( query_term ):
	connection = http.client.HTTPConnection( NYT_HOST )
	query = {'query': query_term, 'api-key': '%s'%NYTTAGS_KEY}

	connection.request('GET', TAGS_PATH+'?'+urllib.parse.urlencode(query))
	response = connection.getresponse()
	decoded_response = response.read().decode(encoding)
	json_response = json.loads(decoded_response)

	tags_list = json_response[1]	
	return tags_list

def getQueryPopular( ):
	connection = http.client.HTTPConnection( NYT_HOST )
	query = {'api-key': '%s'%NYTPOPULAR_KEY}
	popular_list = []
	# tags_list = getTags( query_term )
	# main_tag = tags_list[0]
	connection.request( 'GET', POPULAR_PATH+'?'+urllib.parse.urlencode(query))

	response = connection.getresponse()
	decoded_response = response.read().decode(encoding)
	result = json.loads(decoded_response)['results']


	for key in result:
		
		temp = {}
		temp['web_url'] = key['url']
		temp['headline'] = key['title']
		temp['snippet'] = key['abstract']
		temp['pub_date'] = key['published_date']

		popular_list.append(temp)

	return popular_list





