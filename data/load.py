


#https://www.reddit.com/r/learnpython/comments/bg644l/learning_to_webscrape_reddit_using_beautiful_soup/

### solution 1: scraping 

### get all threads of a specific topic: topic -> thread -> comments

import re 
from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent




def lovely_soup(u):
    ua = UserAgent()
    r = get(u, headers={'User-Agent': ua.chrome})
    return BeautifulSoup(r.text, 'lxml')




def extract_thread_url(topic):
    url = "https://old.reddit.com/r/"+topic+"?sort=top&t=week"
    print("root url: ", url)
    soup = lovely_soup(url)

    url_list = [] #list of threads underneath the r/topic
    for a in soup.find_all('a', href=True):
        url_string = a['href']
        if (re.match("^https.+comments",url_string)):  #valid url containing comments must start with https, with the text '/comment/comment' in the middle 
            print("url appended: ",url_string)
            url_list.append(url_string)
    print("url list: ",url_list)
    
extract_thread_url("Showerthoughts") #problem: if the thread updates too fast, the old thread will be sitting all the way back




### extract comments from each threads      
def extract_comments(thread_url,comment_number): 
    # return(comments)   #to do: 1) expand all comments using Selenium
        
    post_url = thread_url + "/?limit=500"
    print("post url: ", post_url,'\n')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    page = get(post_url, headers=headers) #insert the above header to not be recognized as a bot
    soup = BeautifulSoup(page.content, 'html.parser') #load html page content 
    
    some_comment = soup.find_all("div",{"class":"entry unvoted"})[comment_number]
    comment_body = some_comment.find_all("div",{"class":"md"})[0].get_text()
    timestamps = some_comment.find_all("p",{"class":"tagline"})[0].find_all("time")
    live_timestamp = timestamps[0].attrs['datetime']
    
    try:
        edited_timestamp = timestamps[1].attrs['datetime']
    except IndexError as e:  
        print("An exception occurred:", e)
        edited_timestamp = ''
        
    try:
        count_upvote = some_comment.find_all("span",{"class":"score unvoted"})[0].get_text() #we are one vote short always... WHY?
    except IndexError as e: 
        print("An exception occurred:", e)
        count_upvote = ''
    
    #print("times", timestamps,'\n')
    print("live timestamp: ", live_timestamp,'\n')
    print("edited timestamp: ", edited_timestamp,'\n')
    print("comment_body:\n\n", comment_body ,'\n')
    print("count_upvote:",count_upvote,'\n')


    # write comments into a table... to think about: how do we extract user info as well, user karma, group memberships, on top of the comments?
    # how to we capture the hirechical structure of the data? comment -> re-comment -> re-re-comments? 
    # get all commments

shower_thoughts = extract_comments("https://old.reddit.com/r/Showerthoughts/comments/fjtbye/important_psa_no_you_did_not_win_a_gift_card/",
                                   3)
shower_thoughts

# convert paragraphs of o

#f= open("shower_thoughts_comments_example.txt","w+")
#f.write(shower_thoughts)


### create a classs caled RedditComments
class RedditThread:
    # Class attribute

    def __init__(self, comments, commenters):
        self.comments = comments
        self.commenters = commenters
        
    def description(self):
        return f"Commenter '{self.commenters}' said '{self.comments}'"
        
        
### solution 2: use the praw API
        