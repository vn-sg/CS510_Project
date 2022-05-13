// ***INITIALIZING VARIABLES***
const search = document.getElementById("inputText");
const searchResult = document.getElementById("outputText");
const masterSwitch = document.getElementById("masterSwitch");
const outputBox = document.getElementById("outputBox");
const passCheck = document.getElementById("passCheck");
const failCheck = document.getElementById("failCheck");
const passText = document.getElementById("passText");
const failText = document.getElementById("failText");
outputBox.style.display = 'none';
passCheck.style.display = 'none';
failCheck.style.display = 'none';
passCheck.src = chrome.runtime.getURL("/resources/successLogo.png");
failCheck.src = chrome.runtime.getURL("/resources/errorLogo.png");
// URL_passCheck = chrome.runtime.getURL("/resources/successLogo.png");
// URL_failCheck = chrome.runtime.getURL("/resources/errorLogo.png");
const dark_background_color = '#282c35';
// ***/INITIALIZING VARIABLES***


// ***SETTING PARAMETERS***
search.style.backgroundColor = dark_background_color;
search.style.color = '#fff';
search.focus();
// ***SETTING PARAMETERS***


// // ***ON PAGE LOAD***


// Initialize doc and collection
var port = chrome.runtime.connect({name: "connection_background"});

// Initialize masterSwitch state 
chrome.runtime.sendMessage( 
	{ msg: "getMasterSwitch" },
	isChecked => { 
		masterSwitch.checked = isChecked;
});


port.onMessage.addListener(function(msg) {
	switch(msg.key) {
		case "totalUpdate": 
			break;
		case "updateResultImg": 
			passCheck.style.display = 'none';
			failCheck.style.display = 'none';
			passText.style.display = 'none';
			failText.style.display = 'none';
			outputBox.style.display = 'block';
			outputBox.style.visibility = 'visible';
			if (msg.isPass) {
				passCheck.style.display = 'block';
				passText.style.display = 'block';
			}
			else {
				failCheck.style.display = 'block';
				failText.style.display = 'block';
			}
			break;

	}
});

chrome.tabs.query({
	active: true,
	currentWindow: true
})
.then( ([tab]) => {
		chrome.scripting.executeScript(
			{
				target: {
					tabId: tab.id
				},
				func: getSelectedText,
				args:[]
			}
		)
		.then( (selectedText) => {
			const input = selectedText[0].result;
			if (typeof input !== 'undefined' && input !== '')
				console.log(input);
				search.value = input;
				chrome.runtime.sendMessage(
					{ msg: "query", query: input },
					async res => { 
						try {
							console.log(res);
							searchResult.innerHTML = res;
						}
						catch (error) {
							console.log('Error:', error);
						}
						
					}
				);
		} );
	
} );

function getSelectedText() {
	return window.getSelection().toString();
}

// When User puts input to searchBox
search.addEventListener('input', async () => {
	// outputBox.style.display = 'none';
	outputBox.style.visibility = 'hidden';
	passCheck.style.display = 'none';
	failCheck.style.display = 'none';
	if (typeof search.value !== 'undefined' && search.value !== '')
	{
		const input = search.value;

		chrome.runtime.sendMessage(
			{ msg: "query", query: input },
			res => { 
				try {
					console.log(res);
					searchResult.innerHTML = res;
				}
				catch (error) {
					console.log('Error:', error);
				}
				
			}
		);
	}

});


// Perform action whenever user hit Enter
search.addEventListener('keyup', async function(event) {
	if (event.keyCode === 13) {
		let [tab] = await chrome.tabs.query({
			active: true,
			currentWindow: true
		});

		
		chrome.scripting.executeScript({
			target: {
				tabId: tab.id
			},
			function: process_texts,
		});

	}
});


masterSwitch.addEventListener('change', e => { 
	// Pass on current masterSwitch button state to the background to keep track of
		chrome.runtime.sendMessage(
			{ msg: "setMasterSwitch", isOn: e.target.checked},
			res => { 
				res ? console.log("SUCCESS updating masterSwitch") : console.error("FAIL updating masterSwitch");
		});

	chrome.tabs.query({
		active: true,
		currentWindow: true
	})
	.then( ([tab]) => {
		if (e.target.checked) {
			chrome.scripting.executeScript(
				{
					target: {
						tabId: tab.id
					},
					func: process_texts
				}
			);
		}
		else {
			chrome.scripting.executeScript(
				{
					target: {
						tabId: tab.id
					},
					func: del_highlight
				}
			);
		}
	} );

});

function sendLog(logText) {
	console.log(logText);
}

function process_texts() {
	var global = {tags: [], docs: {}, docList: []};
	
	NON_TEXT_MEDIA = /(script|style|svg|audio|canvas|figure|video|select|input|textarea)/i
	function find_all_text_node(node) {
			
		if (typeof node !== 'undefined' && node.nodeType === 3 && node.data.split(' ').filter(w => w !== '').length > 8 && !(node.parentNode.offsetParent === null)) {
				global.tags.push(node)
		} else if (node && node.nodeType === 1 && node.childNodes && !NON_TEXT_MEDIA.test(node.tagName)) {
			let child_nodes = node.childNodes;
			for (var i = 0; i < child_nodes.length; i++) {
				if (child_nodes[i]) {
					if (child_nodes[i].tagName != "HIGHLIGHT-1024") {
						find_all_text_node(child_nodes[i]);
					}
				}
	
			}
		}
	}
	function highlight_node(isGood, indexes){
		// const CHECK = "&#9989;";
		if (isGood) {
			chrome.runtime.sendMessage(
				{ msg: "getURL_CHECK" },
				URL => { 
					for (var i = 0; i < indexes.length; i++) {
						let tag = global.tags[indexes[i]];
						if (typeof tag.parentNode !== 'undefined') {
							var high_tag = document.createElement("highlight-1024");
							var img_tag = document.createElement("img");
							img_tag.style.display = 'inline-block';
							img_tag.style.height = '1.4em';
							img_tag.style.width = 'auto';
							img_tag.style.verticalAlign = 'middle';
							img_tag.src = URL;

							high_tag.style.backgroundColor = '#B6FF00';
							high_tag.style.color = '#000';
							// high_tag.style.textShadow = '1px 1px 0 #444';
							
							high_tag.appendChild(img_tag);
							high_tag.appendChild(tag.cloneNode(false));
							tag.parentNode.replaceChild(high_tag, tag);
						}
					}
			});
		}
		else {
			chrome.runtime.sendMessage(
				{ msg: "getURL_QMARK" },
					URL => { 
						for (var i = 0; i < indexes.length; i++) {
							let tag = global.tags[indexes[i]];
							if (typeof tag.parentNode !== 'undefined') {
								var high_tag = document.createElement("highlight-1024");
								
								var img_tag = document.createElement("img");
								img_tag.style.display = 'inline-block';
								img_tag.style.height = '1.4em';
								img_tag.style.width = 'auto';
								img_tag.style.verticalAlign = 'middle';
								img_tag.src = URL;

								high_tag.style.backgroundColor = '#B1B1B1';
								// high_tag.style.backgroundColor = '#CFCFCF';
								high_tag.style.color = '#FFFFFF';
								high_tag.appendChild(img_tag);
								high_tag.appendChild(tag.cloneNode(false));
								tag.parentNode.replaceChild(high_tag, tag);
						}
					}
				}	
				);
				
			
		}
		
	}


	find_all_text_node(document.getElementsByTagName("body")[0]);

	global.tags.forEach((tag, _) => global.docList.push(tag.data))
	
	// console.log(global.docList);

	chrome.runtime.sendMessage(
		{ msg: "docs", docs: global.docList },
		res => { 
			try {
				// console.log(res);
				// Label results that passed our checker
				highlight_node(1, res.goodTexts);

				// Label results that failed to pass
				highlight_node(0, res.badTexts);
			}
			catch (error) {
				console.log('Error:', error);
			}
			
		}
	);
}

// 
// To Remove previously generated highlight results
// 
function del_highlight() {
	let node = null;
	let child = null;
	while (node = document.querySelector("highlight-1024")) {
		if (child = node.firstChild){
			child.outerHTML = "";
		}
		node.outerHTML = node.innerHTML;
	}
	while (node = document.querySelector("highlight-1024-selected")) {
		if (child = node.firstChild){
			child.outerHTML = "";
		}
		node.outerHTML = node.innerHTML;
	}

}