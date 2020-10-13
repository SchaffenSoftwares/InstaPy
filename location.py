from selenium.webdriver import Firefox
import os
import json
from time import sleep

def see_more():
    while True:
        try:
            wb.find_element_by_xpath("//a[@class='PJ4k2']").click()
        except:
            break

wb = Firefox(executable_path=os.getcwd() + "/geckodriver.exe")
wb.get("https://www.instagram.com/explore/locations/")
data={}
see_more()
for i in wb.find_elements_by_xpath("//a[@class='aMwHK']"):
        txt1=i.text
        wb.execute_script('''window.open("{}","_blank");'''.format(i.get_attribute("href")))
        sleep(1)
        wb.switch_to.window(wb.window_handles[1])
        see_more()
        data[txt1]={}
        for j in wb.find_elements_by_xpath("//a[@class='aMwHK']"):
                txt2=j.text
                wb.execute_script('''window.open("{}","_blank");'''.format(j.get_attribute("href")))
                sleep(1)
                wb.switch_to.window(wb.window_handles[2])
                see_more()
                data[txt1][txt2]=[k.text for k in wb.find_elements_by_xpath("//a[@class='aMwHK']")]
                wb.close()
                wb.switch_to.window(wb.window_handles[1])
        wb.close()
        wb.switch_to.window(wb.window_handles[0])
with open("database.json","w") as f:
    f.write(json.dumps(data,indent=4))
