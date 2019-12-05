import json
import requests
from bs4 import BeautifulSoup
import sys
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
  
# function to print sentiments 
# of the sentence. 
def sentiment_scores(sentence): 
  
    # Create a SentimentIntensityAnalyzer object. 
    sid_obj = SentimentIntensityAnalyzer() 
  
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    sentiment_dict = sid_obj.polarity_scores(sentence) 
      
    print("Overall sentiment dictionary is : ", sentiment_dict) 
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative") 
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral") 
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive") 
  
    print("Sentence Overall Rated As", end = " ") 
  
    # decide sentiment as positive, negative and neutral 
    if sentiment_dict['compound'] >= 0.05 : 
        print("Positive\n")
        return 1
  
    elif sentiment_dict['compound'] <= - 0.05 : 
        print("Negative\n")
        return 0
  
    else : 
        print("Neutral\n")
  
if __name__=="__main__":

	try:
		print("Enter the users instagram username(should be public)")
		s=str(input())
		input1='https://www.instagram.com/' + s + '/'
		r = requests.get(input1)
		soup = BeautifulSoup(r.text, 'html.parser')
		t=[]
		p=[]
		caption=[]
		script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
		page_json = script.text.split(' = ', 1)[1].rstrip(';')
		data = json.loads(page_json)


		for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
			image_src = post['node']['edge_media_to_caption']
			for k,val in image_src.items():
				val=str(val)
				t=val.split(":")
				x=str(t[2])
				cap=str(x[2:-4])
				cap=cap.replace("\\n"," ")
				nestr = re.sub(r'[^a-zA-Z0-9 ]',r'',cap)
				p.append(nestr)
			
		b=[]
		for i in range(len(p)):
			print(p[i])
			b.append(sentiment_scores(p[i]))
		#print(b)

		if not b:
			print("Account private")
		else:	
			if(b.count(1)>b.count(0)):
				print("User is on the positive side")
			else:
				print("User is on the negative side")
	except:
		print("Account doesn't exist or is not reachable at the moment")