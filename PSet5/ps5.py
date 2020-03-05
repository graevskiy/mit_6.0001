# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        try:
            description = translate_html(entry.description)
        except:
            continue
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    """
    Stores RSS item as following set of properties:
        guid - string
        title - string
        description - string
        link - string
        pubdate - datetime
    """
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid 
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        Input: phrase - string
        """
        self.phrase = phrase

    def get_phrase(self):
        return self.phrase

    def get_phrase_lower(self):
        return self.phrase.lower()

    def is_phrase_in(self, text):
        """
        Checks if given text contains phrase (self.phrase)
        Input: text - string
        Output: True if phrase is in text, False otherwise
        """
        text = text.lower()
        text = re.sub(re.compile(f'[{string.punctuation}]'),' ', text)
        text_list = text.split()
        phrase_list = self.get_phrase_lower().split()        

        if len(phrase_list) > len(text_list):
            return False

        # could try to do
        phrase_pointer = 0
        _max_res = 0
        for i in range(len(text_list)):
            if text_list[i] == phrase_list[phrase_pointer]:
                phrase_pointer += 1
            else:
                phrase_pointer = 0
            if phrase_pointer == len(phrase_list):
                return True

        return False


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):

    time_format = "%d %b %Y %H:%M:%S"
    
    def __init__(self, time):
        dt = datetime.strptime(time, self.__class__.time_format)
        self.datetime = self.to_aware_and_ETC(dt)

    def to_aware_and_ETC(self, dt):
        return dt.replace(tzinfo=pytz.timezone("EST"))


    def get_time(self):
        """
        Returns datetime as datetime object
        """
        return self.datetime

    def get_datetime_str(self):
        return self.get_time().strftime(self.__class__.time_format)

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.to_aware_and_ETC(story.get_pubdate()) < self.get_time()

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.to_aware_and_ETC(story.get_pubdate()) > self.get_time()


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):

    def __init__(self, other_trigger):
        self.base_trigger = other_trigger

    def get_base_trigger(self):
        return self.base_trigger

    def evaluate(self, story):
        return not self.get_base_trigger().evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):

    def __init__(self, *triggers):
        self.base_triggers = list(triggers)

    def get_base_triggers(self):
        return self.base_triggers[:]

    def evaluate(self, story):
        return all([t.evaluate(story) for t in self.get_base_triggers()])

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):

    def __init__(self, *triggers):
        self.base_triggers = list(triggers)

    def get_base_triggers(self):
        return self.base_triggers[:]

    def evaluate(self, story):
        return any([t.evaluate(story) for t in self.get_base_triggers()])

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return [story for story in stories if any(t.evaluate(story) for t in triggerlist)]



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    def check_triggers_and_append(triggers_list, list_to_append_to, triggers):
        """
        takes list of triggers from config file (as list), 
        checks if trig name is a valid trigger and updates final list
        """
        res = list_to_append_to[:]
        for t in triggers_list:
            if t in triggers:
                res.append(triggers[t])
        return res

    def class_trig(class_name):
        return {
            'title': TitleTrigger,
            'description': DescriptionTrigger,
            'after': AfterTrigger,
            'before': BeforeTrigger,
            'and': AndTrigger,
            'or': OrTrigger,
            'not': NotTrigger,
        }[class_name]

    def update_triggers(triggers, source):
        assert len(source) >= 3, f"config file - invalid line: '{','.join(source)}'"        

        # assume line looks like below ( or smilar)
        # t2,DESCRIPTION,Trump
        # t6,AND,t1,t4
        trig_name = source[0] #t2
        trig_type = source[1].lower() #DESCRIPTION
        trig_props = source[2:] #Trump

        if trig_type in ('and', 'or', 'not'):
            for i in range(len(trig_props)):
                try:
                    trig_props[i] = triggers[trig_props[i]]
                except KeyError:
                    raise f"line: {','.join(source)}\n{_prop} name of trigger doesn't exist."

        trigger = class_trig(trig_type)(*trig_props)

        triggers.update({trig_name: trigger})


    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    # print(lines) # for now, print it so you see what it contains!
    res = []
    triggers = {}
    for line in lines:
        line = line.split(",")
        if line[0].lower() == "add":
            res = check_triggers_and_append(line[1:], res, triggers)
        else:
            update_triggers(triggers, line)

    return res


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("stocks")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]
        # triggerlist = [t3]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))


            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

