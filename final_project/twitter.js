

document.getElementById('search_button').onclick = querySearch;
var host = 'http://localhost:8100'


function querySearch(evt){
	var search_term = document.getElementById('query_search').value
	var xmlhttp = new XMLHttpRequest();

	xmlhttp.addEventListener('load', onQueryResponse, false);
	xmlhttp.open('GET', host+'/search/'+search_term, true);
	xmlhttp.send(null)
}

function onQueryResponse(){
	var query_response = JSON.parse(this.responseText);
	if ('nyt_recent' in query_response){
		onNYTQueryResponse(query_response['nyt_recent'])
	}
	if('twitter' in query_response){
		onTwitterQueryResponse(query_response['twitter'])
	}
	
}



function onTwitterQueryResponse(tweet_list){
	var tweets = "";

	for(var count in tweet_list){
		var tweet = tweet_list[count]
		var text = tweet['tweet_text']
		var text_string = JSON.stringify(text)
		tweets += '<p id=p'+count+'>'+text_string+'<br/>'
	}
	document.getElementById('twitter_search').innerHTML = tweets
}

function onNYTQueryResponse(article_list){

	var headlines = "";

	for(var count in article_list){
		var article = article_list[count]
		var url = article['web_url']
		var headline = article['headline']
		var snippet = article['snippet']
		var snippet_string = JSON.stringify(snippet)
		var headline_string = JSON.stringify(headline)
		headlines += '<p id=p'+count+'><a href='+url+'>'+headline_string+'</a> <br/>'+snippet_string +'<br/>';
	}
	document.getElementById('nyt_search').innerHTML = headlines
}



