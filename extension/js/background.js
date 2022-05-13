// background.js

var global = {};
global.isMasterSwitchOn = false;
global.port = null;
global.tags = [];

// const URL_CHECK = chrome.runtime.getURL("/resources/check.png");
// const URL_QMARK = chrome.runtime.getURL("/resources/question_mark.png");


function getText(){
	return global.text;
}


function find_all_text_node(node) {
			
	if (node && node.nodeType === 3 && node.length > 1 && !(node.parentNode.offsetParent === null)) {
			global.tags.push(node)
	} else if (node && node.nodeType === 1 && node.childNodes && !NON_TEXT_MEDIA.test(node.tagName)) {
		let child_nodes = node.childNodes;
		for (var i = 0; i < child_nodes.length; i++) {
			if (child_nodes[i]) {
				if (child_nodes[i].tagName != "HIGHLIGHT-101") {
					find_all_text_node(child_nodes[i]);
				}
			}

		}
	}
}

function gen_docs(HTMLbody){
	global.tags = []
	docs = {};
	find_all_text_node(HTMLbody);
	console.log(global.tags);
	global.tags.forEach((tag, index) => docs[index] = tag.data)
	console.log(docs);
}

// On connecting event, store the connection in global variable
chrome.runtime.onConnect.addListener(function(port) {
	
	global.port = port;

  });

async function getScore(data) {
  	const url = "http://127.0.0.1:35678/getScore"
	try {
		return await fetch(url, {
			method: 'POST', // *GET, POST, PUT, DELETE, etc.
			mode: 'cors', // no-cors, *cors, same-origin
			cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
			credentials: 'same-origin', // include, *same-origin, omit
			headers: {
			'Content-Type': 'application/json'
			// // 'Content-Type': 'application/x-www-form-urlencoded',
			},
			redirect: 'follow', // manual, *follow, error
			referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
			body: JSON.stringify(data) // body data type must match "Content-Type" header
		})
		.then( res => res.json() ) // parses JSON response into native JavaScript objects
		// .then( data => { 
		// 	console.log(data);
		// 	return data;
		// 	})
		// If fetch failure, log the Error and return 
		.catch((error) => {
			throw error;
		});
		
	}
	catch(error) {
		console.log(error);
		return { score: 1 - Math.random()/1000 };
	}
	
}

function updateResultImg(score){
	if (score > 0.5) {
		global.port.postMessage({key: "updateResultImg", isPass: 0});
	}
	else {
		global.port.postMessage({key: "updateResultImg", isPass: 1});
	}
}


chrome.runtime.onMessage.addListener( function(request, sender, sendResponse) {
	switch(request.msg) {
		case "test":
			sendResponse("success!");
			break;

		case "setMasterSwitch":
			global.isMasterSwitchOn = request.isOn;
			sendResponse(true);
			break;
		case "getMasterSwitch":
			sendResponse(global.isMasterSwitchOn);
			break;

		case "getURL_CHECK":
			sendResponse(chrome.runtime.getURL("/resources/check.png"));
			return true;

		case "getURL_QMARK":
			sendResponse(chrome.runtime.getURL("/resources/question_mark.png"));
			return true;

		case "query":
			if (typeof request.query !== 'undefined' && request.query !== '')
			// getScore( {'text': request.query} )
			getScore( request.query )
					.then(res => {
						console.log(res.score);
						updateResultImg(res.score);
						sendResponse(res.score);
					});
			
			return true;
		case "docs":
			const docs = request.docs
			var scores = {};
			// console.log(docs);

			Promise.all(docs.map(async (doc, index) => {
				// const res = 
				await 
				// getScore( {'text': doc} )
				getScore( doc )
					.then(res => {
						if (res.hasOwnProperty('score')){
							console.log(res.score); // JSON data parsed by `data.json()` call
							scores[index] = res.score;
						}
						else {
							scores[index] = Math.random();
						}
						
					});
				
			}))
			.then( _ => 
				{
					console.log("ALL DONE!");
					console.log("SORTING THE OBJECT..");
					keysSorted = Object.keys(scores).sort((a,b) => scores[b]-scores[a] );

					console.log("SORTED:: ", keysSorted);
					let NUM_RESULT = 20;
					if (keysSorted.length <= NUM_RESULT*2) 
						NUM_RESULT = Math.floor(keysSorted.length/2);

					const good =  keysSorted.slice(keysSorted.length-NUM_RESULT, keysSorted.length).filter(key => scores[key] < 0.5);
					console.log("<GOOD VALUES>\n");
					good.forEach((key) => console.log(scores[key], "\n"));
					console.log("</GOOD VALUES>\n");
					const bad = keysSorted.slice(0, NUM_RESULT).filter(key => scores[key] > 0.5);
					console.log("<BAD VALUES>\n");
					bad.forEach((key) => console.log(scores[key], "\n"));
					console.log("</BAD VALUES>\n");
					sendResponse({'goodTexts': good, 'badTexts': bad});
					
				});
			return true;
			// let goodDocs = [];
			// let badDocs = [];
			// console.log("ALL DONE!!!!!");
			// console.log(scores);
			// console.log("SORTING THE OBJECT..");
			// keysSorted = Object.keys(scores).sort((a,b) => scores[a]-scores[b] );
			// console.log("SORTED:: ", keysSorted);

			// while(texts.length < 21) {
			// 	let rand = Math.floor(Math.random()*request.docs.length)
			// 	if (texts.includes(rand))
			// 	{}
			// 	else 
			// 		texts.push();
				
			// 	console.log(rand);
			// }
			// let badTexts = [];
			// for(var i = 0; i < 10; i++){
			// 	badTexts.push(Math.floor(Math.random()*request.docs.length));
			// }
			// sendResponse({'goodTexts': keysSorted.slice(keysSorted.length-10, keysSorted.length), 'badTexts': keysSorted.slice(0, 10)});
	}
});

