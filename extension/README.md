# Intelligent Find Chrome Extension    
> **CS410 CourseProject**  
 
## Group Name: **Debuff**
## Members:
- Luhao Wang  
- Shih-Chiang Lee
- Jiaxin Ying  

# Overview
## Take a look at our [**Tutorial Presentation**](https://drive.google.com/file/d/1LMwCwm6UX8T4WJORoJW8L162K1FJjlE8/view?usp=sharing) before you begin :)  
<br/>

This is a chrome extension to improve people’s searching efficiency on the current tab. The default search function that Chrome provides can only do one-to-one matching of keywords. In our project, the extension can perfectly replace the old search function, while allowing users to accomplish more matching than just basic exact keyword matching capabilities. More specifically, users are able to match entire sentences or search-engine inputs like questions to most relevant components we call “documents” by the meaning and occurrences of words.

## Main Functions:
1.	Dividing the webpage into documents to form a collection of properly set documents based on topics and distribution of text contents.
2.	Match the most relevant sentences to the search keywords in meaning, if the match result is empty, will further match by keyword
3.	Highlight results with different colors. The current result will be orange, and others will be yellow.
4.	Able to jump to the location of the current result. The first result will be the most relevant.
5.	Able to jump to the location of previous result or next result by clicking upward and downward buttons.
6.	supports shortcut key [Ctrl+Shift+f]

## Software Implementation

### Main Components

Our implementation consists of mainly two parts: The Front-End User Interface and the Back-End javascript functions to support fundamental functionalities. Through exploring, we found that the most efficient way to communicate between front and back end is through sending messages in Manifest V3. To be more specific, our content script handles the interaction between the “popup” which we call the user interface and the scripts injected into the webpage. Meanwhile, the content scripts sent chrome runtime messages to backend scripts, namely the background.js, to fulfill users’ requests.
	
### A Simple Walkthrough

As a walkthrough of the process of a user-input-lookup-up cycle, we begin by initializing the setup of collections and documents for each tab when users visit a new webpage. We tuned this process to make the efficiency pretty good, which takes milliseconds to finish generating indexed docs, collections, and computes potentially useful stats, such as average document length and vocabulary, for future usage. Upon completion, the extension constantly monitors the user’s input and parses it into processable data structures such as arrays and objects in order to compute scores and rank the results. We have spent quite some time optimizing this process to make it very responsive, by providing immediate results for each character that users type in. Upon retrieving ranked search results associated with scores, we took advantage of the DOM object structure of HTML elements to highlight the result for users according to the score of each document. And we also keep track of the ranks of the results and store them so that users will be able to see labeled rank and jump across results in the order of their ranks.

We implement the BM25 model from scratch in javascript. The first step is to construct the data structure to store the inverted index, document length and average document length. For each webpage, we treat the whole document as a collection and treat every topic as a document.
 
Then we use the shown equation to calculate the score for each document given a query, and rank all documents given their scores. If there are more documents with a score greater than 0, we take the top 10 documents. After reference search and fine tuning, we choose to set k as 1.2 and b as 0.2.

## Software Usage
	
Before the start: 
	This is a Google Chrome Extension. Therefore, before using, please make sure that the browser you are using is chrome, or a browser that supports Google Chrome Extension.

### Installation:
 1.	Open your browser.
 2.	Go to “**Setting**”, and click “**Extension**”.
<p align="center"><img src="https://user-images.githubusercontent.com/77092749/145667215-dd1ca215-5691-43b9-949d-48f6c2ce2f45.png"></p>

 3. Open “**Developer Mode**”, Click "**Load unpacked**", and select the folder where you downloaded our extension source code
 
<p align="center"><img src="https://user-images.githubusercontent.com/77092749/145668048-7096dbac-8948-4221-bccc-9e2dbe9cfb63.png"></p>
 
 4. Make sure the extension is turned on
 
<p align="center"><img src="https://user-images.githubusercontent.com/77092749/145668049-7c59ff46-b52e-4198-8f2a-d3b709c898b0.png"></p>


### Instructions for use:

1. The shortcut keys to quickly call our search box is: **Ctrl+Shift+F**. Or you can simply click on the button of the extension on the top right corner

<p align="center"><img src="https://user-images.githubusercontent.com/77092749/145668052-efff3190-7938-41da-b352-8890324b261d.png"></p>
<p align="center"><img src="https://user-images.githubusercontent.com/77092749/145668055-62294757-ff44-48c7-8f15-63ac9889e35b.png"></p>

2. In the black input box, type in the keywords, phrases or sentences you want to search on the current tab. Then, tap “Enter” on your keyboard. The page will move to the results, and they will be highlighted. Here is an 	example for search "When will my social security card arrive?" in [this webpage](https://www.thebalancecareers.com/how-to-get-a-social-security-number-for-non-us-citizens-2064264).


![image](https://user-images.githubusercontent.com/77092749/145668058-57217138-d04e-4db6-a4a5-2a221f4bc62f.png)





 
 	

 

 
The top result will be highlighted with orange. And the rest results 
will be highlighted with yellow. The yellow result may not be relevant to your research

If you don’t think the result highlighted with orange is relevant to 
your research, click ![image](https://user-images.githubusercontent.com/77092749/145668059-fa893c84-a418-4563-a2a4-1bfba3deb5c3.png) to move to the next relevant result. Or click ![image](https://user-images.githubusercontent.com/77092749/145668061-8760b71a-edd1-4a56-977d-629d2bf64f47.png) to move to the previous result. The new current result will be highlighted with 	orange, and the old result will be highlighted with yellow.


