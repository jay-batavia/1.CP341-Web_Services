

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
		onNYTQueryResponse(query_response['nyt_recent'] )
	}
	if('twitter' in query_response){
		onTwitterQueryResponse(query_response['twitter'])
	}
	if('nyt_popular' in query_response){
		onNYTPopularResponse(query_response['nyt_popular'])
	}
	if('nyt_wire' in query_response){
		onNYTWireResponse(query_response['nyt_wire'])
	}
	
}


function onNYTWireResponse(wire_list){
	var search_display = document.getElementById('nyt_wire')
	search_display.innerHTML = ""


	var h1 = document.createElement('h1')
	var heading_text = document.createTextNode('NYT Newswire: ')
	h1.appendChild(heading_text)
	search_display.appendChild(h1)


	for(var count in wire_list){
		var article = wire_list[count]
		var url = article['web_url']
		var headline = article['headline']
		var snippet = article['snippet']
		var pub_date = article['pub_date']
		var section = JSON.stringify(article['section_tag'])

		var snippet_string = JSON.stringify(snippet)
		var headline_string = JSON.stringify(headline)
		var date_string = JSON.stringify(pub_date)

		var br = document.createElement('br')
		var pnode = document.createElement('p');
		var a = document.createElement('a');

		var linkText = document.createTextNode('['+section+']'+headline_string)

		a.appendChild(linkText)
		a.href = url
		a.appendChild(br)
		pnode.appendChild(a)
		var text_node = document.createTextNode(snippet_string +' at: '+date_string)
		pnode.appendChild(text_node)
		search_display.appendChild(pnode);
	}
}


function onTwitterQueryResponse(tweet_list){
	var tweets = "";
	var search_display = document.getElementById('twitter_search')
	search_display.innerHTML = ""

	var h1 = document.createElement('h1')
	var heading_text = document.createTextNode('Twitter Search: ')
	h1.appendChild(heading_text)
	search_display.appendChild(h1)

	for(var count in tweet_list){
		var tweet = tweet_list[count]

		var text = tweet['tweet_text']
		var rt_count = tweet['retweet_count']
		var text_string = JSON.stringify(text)
		var rt_string = JSON.stringify(rt_count)

		var br = document.createElement('br')
		var pnode = document.createElement('p');
		var a = document.createElement('a');


		var tweet = document.createTextNode(text_string);
		var rt_string = document.createTextNode('Retweet Count: '+rt_count);
		pnode.appendChild(tweet)
		pnode.appendChild(br)
		pnode.appendChild(rt_string)

		search_display.appendChild(pnode)
	}

}

function onNYTPopularResponse(article_list){
	var search_display = document.getElementById('nyt_popular')
	search_display.innerHTML = ""
	var heading_text = document.createTextNode('NYT Popular:')
	var h1 = document.createElement('h1')
	h1.appendChild(heading_text)
	search_display.appendChild(h1)

	for(var count in article_list){
		var article = article_list[count]
		var url = article['web_url']
		var headline = article['headline']
		var snippet = article['snippet']
		var pub_date = article['pub_date']

		var snippet_string = JSON.stringify(snippet)
		var headline_string = JSON.stringify(headline)
		var date_string = JSON.stringify(pub_date)

		var br = document.createElement('br')
		var pnode = document.createElement('p');
		var a = document.createElement('a');

		var linkText = document.createTextNode(headline_string)	

		a.appendChild(linkText)
		a.href = url
		a.appendChild(br)
		pnode.appendChild(a)
		var text_node = document.createTextNode(snippet_string +' at: '+date_string)
		pnode.appendChild(text_node)
		search_display.appendChild(pnode);
	}

}


function onNYTQueryResponse(article_list){
	var search_display = document.getElementById('nyt_search')
	search_display.innerHTML = ""

	var headlines = "";
	var h1 = document.createElement('h1')
	var heading_text = document.createTextNode('NYT Search: ')
	h1.appendChild(heading_text)
	search_display.appendChild(h1)


	for(var count in article_list){
		var article = article_list[count]
		var url = article['web_url']
		var headline = article['headline']
		var snippet = article['snippet']
		var pub_date = article['pub_date']
		var section = JSON.stringify(article['section_tag'])

		var snippet_string = JSON.stringify(snippet)
		var headline_string = JSON.stringify(headline)
		var date_string = JSON.stringify(pub_date)

		var br = document.createElement('br')
		var pnode = document.createElement('p');
		var a = document.createElement('a');

		var linkText = document.createTextNode('['+section+']'+headline_string)

		a.appendChild(linkText)
		a.href = url
		a.appendChild(br)
		pnode.appendChild(a)
		var text_node = document.createTextNode(snippet_string +' at: '+date_string)
		pnode.appendChild(text_node)
		search_display.appendChild(pnode);
	}
	// document.getElementById('nyt_search').innerHTML = headlines
}



