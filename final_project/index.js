var NYTSEARCH_KEY = 'c3a712f9587a97bc584a76df1fef5664:9:72962549'
var NYTTAGS_KEY = '66e62094aa65abba8e843ecd98ede1b1:7:72962549'
var NYTPOPULAR_KEY = 'd058a36f897d68b2167470dc46767279:15:72962549'
var NYT_URI = 'http://api.nytimes.com/svc/'
var TAGS_PATH = 'suggest/v1/timestags'
var SEARCH_PATH = 'search/v2/articlesearch.json'
var POPULAR_PATH = 'mostpopular/v2/mostshared/1.json'


document.getElementById('nyt_search').onclick = handleNYTQuery;
document.getElementById('nyt_popular').onclick = getNYTPopular;


function handleNYTPopular(e){
	var search_query = document.getElementById('nyt_query').value;
	searchNYTTags(search_query, getNYTPopular)
}

function searchNYTTags(search_query, callback){
	xmlhttp = new XMLHttpRequest();

	xmlhttp.addEventListener('load', callback, false);
	xmlhttp.open('GET', NYT_URI+TAGS_PATH+'?query='+search_query+'&api-key='+NYTTAGS_KEY)
	xmlhttp.send(null)
}

function getNYTPopular(){
	// var tags_response = JSON.parse(this.responseText)
	// var main_tag = tags_response[1][0]

	xmlhttp = new XMLHttpRequest();

	xmlhttp.addEventListener('load', onNYTPopularRx, false);
	xmlhttp.open('GET', NYT_URI+'mostpopular/v2/mostshared/all-sections/1.json?api-key=d058a36f897d68b2167470dc46767279%3A15%3A72962549')
	xmlhttp.send(null)

}

function onNYTPopularRx(){
	var NYTPopular_response = JSON.parse(this.responseText);
	console.log(this.responseText)

}


function handleNYTQuery(e){
	var search_query = document.getElementById('nyt_query').value;
	var xmlhttp = new XMLHttpRequest();

	xmlhttp.addEventListener('load', onNYTQueryResponse, false);

	xmlhttp.open('GET', NYT_URI+SEARCH_PATH+'?q='+search_query+'&sort=newest&hl=true&api-key='+NYTSEARCH_KEY);
	xmlhttp.send(null);
}

function onNYTQueryResponse(){
	var paragraph = document.getElementById('contents');
	var response = JSON.parse(this.responseText)['response'];
	var NYTSearch_hits = response['docs']
	var headlines = ""

	for(var number in NYTSearch_hits){
		var item = NYTSearch_hits[number]
		var url = item['web_url']
		var headline = item['headline']['main']
		var snippet = item['snippet']
		var snippet_string = JSON.stringify(snippet)
		var headline_string = JSON.stringify(headline)
		headlines += '<p id=p'+number+'><a href='+url+'>'+headline_string+'</a> <br/>'+snippet_string ;
	}
	
	document.getElementById('NYTSearch').innerHTML = headlines
}