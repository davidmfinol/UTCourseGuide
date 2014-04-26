UTCourseGuide
=============
UTCourseGuide crawls the UT Austin electronic Course Instructor Survey (eCIS) database to mine student feeback about UT courses, which it then re-displays to allow UT Students to have an easier time during registration.

Pre-requisites
-------------
UTCourseGuide is written in Python 2.7, which can be found here: 
https://www.python.org/download/releases/2.7

It also requires the Scrapy python module, which can be found here:
http://doc.scrapy.org/en/latest/intro/install.html

The second required module is Selenium, which can be found here:
https://pypi.python.org/pypi/selenium

Usage
-------------
Run the webcrawler with the following command:
scrapy crawl utcourseguide -a username=<youreid> -a password=<yourschoolpassword>

To have the data be stored as json, add the follwing flags: -o items.json -t json
The full command would then be:
scrapy crawl utcourseguide -a username=<youreid> -a password=<yourschoolpassword> -o items.json -t json
