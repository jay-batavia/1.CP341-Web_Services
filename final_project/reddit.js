var CLIENT_SECRET = 'G1icv8SulRpnnq0IEyMDC9GqnXA';
var CLIENT_ID = 'ftdmUlIROTiAGw:'
var REDDIT_HOST = 'https://www.reddit.com'

window.onload = handleRedditConnect;
document.getElementById('reddit').onclick = getTopAll;
var access_token;

function handleRedditConnect(e){
	xmlhttp = new XMLHttpRequest();
	var auth_string = CLIENT_ID+CLIENT_SECRET;
	var encoded_auth = btoa(auth_string)
	var post_data = "grant_type=client_credentials"
	xmlhttp.addEventListener('load', onRedditTokenRx, false);
	xmlhttp.open('POST','https://www.reddit.com/api/v1/access_token', true);
	xmlhttp.setRequestHeader('Authorization', 'Basic '+encoded_auth);
	xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xmlhttp.send(post_data)
}


function onRedditTokenRx(){
	var resp = JSON.parse(this.responseText)
	access_token = resp['access_token']
}

function getTopAll(e){
	xmlhttp = new XMLHttpRequest;

	xmlhttp.addEventListener('load', onTopAllRx, false);
	xmlhttp.open('GET', REDDIT_HOST+'/r/DestinyTheGame/new.json', true)
	xmlhttp.setRequestHeader('Authorization', ' Bearer '+access_token)
	xmlhttp.send(null)
}

function onTopAllRx(){
	var resp = this.responseText
	console.log(resp)
}