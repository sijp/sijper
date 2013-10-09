var url="http://test/srv/"

function sijperResponseHandler(data){
	for (post in data.posts){
		$("#resultbox").append(	data.posts[post]["user"]["uname"]+
					" : "+data.posts[post]["msg"]+
					"<br/>");
	}
}


function sijperPost(obj){
	
	$.post(	url,
		$(obj).serialize(),
		sijperResponseHandler);

	return false;
}
