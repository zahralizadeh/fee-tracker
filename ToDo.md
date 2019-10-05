# webapp
- [x] login web service
- [ ] forget password
- [x] api list
- [ ] send email to user
- [ ] make configs hidden
- [x] password hasher

# userquery
- [x] handle user request (price)
- [ ] handle user request (area)
- [x] save user request
- [x] webservice  user request
- [ ] autentication is complosory for sending request
- [ ] pridict more consistently - hidden BUG

# web scrape
- [x] webscrape model documentation
- [ ] fix bug: scrape age (new/none) is not detected
- [x] search prediction history before start prediction
- [ ] fix warning of ssl sneding request to ihome

# clean database
- [ ] in cleaning database consider that for each location there should be at least 50 records left
- [ ] extra data (more that 150 for each  location will be deleted)
- [ ] if last update was not successfull try again some minutes later

# poll
- [ ] ask user if prediction was accurate or not (receive and store poll)

# Server Side
- [ ] https://stackoverflow.com/questions/46385350/django-cron-task-not-executing-automatically
- [ ] how to upload website on server


# logic
- [x] automatic scheduling 
- [x] change logic to read all of the sites
- [x] https://www.geeksforgeeks.org/python-schedule-library/
- [x] https://django-cron.readthedocs.io/en/latest/installation.html
- [x] check data and collect data since last update automatically
- [x] if database is clean first data collecting will run
- [x] delete old files from database
- [x] save price/meter instead of price, check if the result is more consisitent or not
- [x] save property type! it was ignored!!!!



