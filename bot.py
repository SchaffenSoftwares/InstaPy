from flask import Flask,request as rq,jsonify
import os
from time import sleep
from distutils.util import strtobool as sb
from selenium.webdriver import Firefox
from instapy import InstaPy as ip
from bs4 import BeautifulSoup as bs
from requests import get as ge
import re

class insta:
    def __init__(self):
        self.wb,self.url=None,None
        self.user = input("Enter Username:")
        self.pwd = input("Enter Password:")
        if os.path.exists(r"C:\Users\user\InstaPy\assets\extension.xpi"):
            try:
               os.system("taskkill /f /im firefox.exe")
            except:
                pass
        self.se = ip(username=self.user, password=self.pwd, headless_browser=True)
        self.se.login()
        self.se.set_dont_like(["naked", "nsfw"])
        self.pro()

    def see_more(self):
        while True:
            try:
                self.wb.find_element_by_xpath("//a[@class='PJ4k2']").click()
            except:
                break

    def pro(self):
        a=Flask(__name__)

        @a.route("/personal")
        def per():
            r=ge("https://www.instagram.com/{}/".format(self.user))
            b=bs(r.content,"html5lib")
            m = list(map(int, re.findall(r"\d+",b.find("meta", attrs={"name": "description"}).get("content").replace(",","").split("-")[0])))
            d = {"Post": m[2], "Img": b.find("meta", attrs={"property": "og:image"}).get("content"),"Total Followers": m[0], "Total Following": m[1], "Followers List": {}, "Following List": {}}
            f=self.se.grab_followers(username=self.user,amount="full",live_match=False,store_locally=False)
            fg=self.se.grab_following(username=self.user,amount="full",live_match=False,store_locally=False)
            for j,i in enumerate(f):
                print(j+1)
                r=ge("https://www.instagram.com/{}/".format(i))
                b=bs(r.content,"html5lib")
                try:
                   d["Followers List"].update({i: b.find("meta", attrs={"property": "og:image"}).get("content")})
                except:
                    d["Followers List"].update({i:"-"})
            for j,i in enumerate(fg):
                print(j+1)
                r=ge("https://www.instagram.com/{}/".format(i))
                b=bs(r.content,"html5lib")
                try:
                    d["Following List"].update({i: b.find("meta", attrs={"property": "og:image"}).get("content")})
                except:
                    d["Following List"].update({i:"-"})
            return jsonify(d)

        @a.route("/location")
        def lo():
            con = rq.args.get("con")
            cit = rq.args.get("cit")
            loc = rq.args.get("loc")
            self.wb = Firefox(executable_path=os.getcwd() + "/geckodriver.exe")
            self.wb.get("https://www.instagram.com/explore/locations/")
            sleep(1)
            self.see_more()
            for i in self.wb.find_elements_by_xpath("//a[@class='aMwHK']"):
                if con == i.text:
                    i.click()
                    sleep(1)
                    self.see_more()
                    for j in self.wb.find_elements_by_xpath("//a[@class='aMwHK']"):
                        if cit == j.text:
                            j.click()
                            sleep(1)
                            self.see_more()
                            for k in self.wb.find_elements_by_xpath("//a[@class='aMwHK']"):
                                if loc == k.text:
                                    k.click()
                                    sleep(3)
                                    self.url = self.wb.current_url
                                    self.wb.close()
                                    break
                            break
                    break
            return "abc"

        @a.route("/like/<op>")
        def like(op):
            am = int(rq.args.get("am"))
            if op=="Tags":
                val = rq.args.get("val")
                if "," in val:
                       self.se.like_by_tags(val.split(","), amount=am)
                else:
                       self.se.like_by_tags([val], amount=am)
            elif op=="Location":
                self.se.like_by_locations([re.search(r'\d+', self.url).group()],amount=am,skip_top_posts=bool(sb(rq.args.get("stp"))))
            return "abc"

        @a.route("/cmnt/<op>")
        def cmnt(op):
            val=rq.args.get("val")
            me=rq.args.get("me")
            if me=="Both":
                me=None
            self.se.set_do_comment(enabled=True, percentage=rq.args.get("per"))
            if op=="random":
                   if "," in val:
                      self.se.set_comments(val.split(","),media=me)
                   else:
                       self.se.set_comments([val],media=me)
            elif op=="mamdatory":
                    mw=rq.args.get("mw")
                    k = [i.strip(" ") for i in mw.split("OR")]
                    for i, j in enumerate(k):
                        if "AND" in j:
                          k[i] = [y.strip(" ") for y in k[i].split("AND")]
                    if "," in val:
                        cm=[{'mandatory_words':k,'comments':val.split(",")}]
                    else:
                        cm=[{'mandatory_words':k, 'comments':[val]}]
                    self.se.set_comments(cm,media=me)
            if rq.args.get("po")=="loc":
                self.se.comment_by_locations([re.search(r'\d+', self.url).group()],amount=int(rq.args.get("am")),skip_top_posts=bool(sb(rq.args.get("stp"))))
            return "abc"

        @a.route("/follow/<op>")
        def follow(op):
           am=int(rq.args.get("am"))
           if op=="Tags":
               val=rq.args.get("val")
               try:
                   if "," in val:
                     self.se.follow_by_tags(val.split(","),amount=am)
                   else:
                     self.se.follow_by_tags([val],amount=am)
               except:
                   pass
           elif op=="Location":
               self.se.follow_by_locations([re.search(r'\d+', self.url).group()], amount=am,skip_top_posts=bool(sb(rq.args.get("stp"))))

        #@a.route("/interact")
        #def interact():


        a.run()

if __name__=="__main__":
    d=insta()