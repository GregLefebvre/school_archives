from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import time
import chromedriver_binary
import json

class DriverBot():

    def __init__(self):
        self.introduce()

    def introduce(self):
        print(self.text_in_a_box('hello '))

    def text_in_a_box(self, message, separator='o', padding=3):
        message = str(message)
        top = separator * (len(message) + padding*2 + 2)
        empty_line = separator + (len(message) + padding*2)*" " + separator + '\n'

        message = top + '\n' + empty_line*padding + separator + " "*padding + message + " "*padding + separator + '\n'+ empty_line*padding + top+ '\n'
        return message

    def initiate_driver(self):
        driver = webdriver.Chrome()
        return driver

    def query_schools_and_cities(self):
        self.driver.get('https://en.wikipedia.org/wiki/List_of_schools_in_France')
        time.sleep(1)
        school_list = list()
        schools_full = self.driver.find_elements_by_xpath('/html[1]/body[1]/div[3]/div[3]/div[4]/div[1]/ul[1]/li')
        for school_full in schools_full:
            school_name = school_full.find_element_by_xpath('./a[1]').text
            try:
                school_city = school_full.find_element_by_xpath('./a[2]').get_attribute('title')
            except:
                school_city = False
            school_data = [school_name, school_city]
            # print(school_data)
            school_list.append(school_data)
        return school_list


    def main_action(self):
        start_time = time.time()
        self.driver = self.initiate_driver()
        school_list = self.query_schools_and_cities()

        # with open('schools1.txt', 'w+') as outfile:
        #     # json.dump(school_list, outfile, indent=4)
        #     outfile.write('from files_exchange.models import *'+'\n')
        #     outfile.write('lycee = TypeSchool.objects.filter(slug_title="lycee")[0]'+'\n')
        #     for school in school_list:
        #         if school[1]:
        #             city = 'school="'+school[1]+'", '
        #         else:
        #             city = ''
        #         str = 'school = School(title="'+school[0]+'", '+city+'type=lycee)'+'\n'
        #         outfile.write(str.encode('utf-8'))
        #         outfile.write('school.save()'+'\n')

        print('from files_exchange.models import *')
        print('lycee = TypeSchool.objects.filter(slug_title="lycee")[0]')
        for school in school_list:
            if school[1]:
                city = 'city="'+school[1]+'", '
            else:
                city = ''
            str = 'school = School(title="'+school[0]+'", '+city+'type=lycee)'
            print(str)
            print('school.save()')

        end_time = time.time()
        duration = end_time-start_time
        return duration

    def end_driver(self):
        self.driver.quit()

if __name__ == '__main__':
    bot = DriverBot()
    duration = bot.main_action()
    print(bot.text_in_a_box(duration))
    bot.end_driver()
