# PhoneBook Assessment
## Task Instructions

* **Main objective**: Create a phone book - Web Server API


### General Instructions:
* The app should be a simple phone book (contacts) like any contacts book on your personal phone
* It should be a clear and simple API service
* There is no need for a UI, we'll mainly focus on the backend implementation.
* The server can be written on any preferred framework but we'll be happy to get it in **GoLang**.
* Consider *scale*, *error* *handling*, *logs*, **tests**, etc...
* Please use docker

### Expected features:
* Contact should include - first name, last name, phone, and address
* The service API should include:
  * **Get** contacts - with a maximum of 10 with a pagination feature
  * **Search** contact
  * **Add** contact
  * **Edit** contact
  * **Delete** contact
  
* **README**: Please add proper run instructions and API documentation to your code.

### Bonus features:
* Add any feature you'd like!!

### Handover:
* Next Tuesday 20/6
* Please use Github
---

## Functional requirements
1. API should consist of CRUD ops.
   1. app should be able to store contacts. (**which DB should I use??**)
2. the search should be optimize search engine.
3. app should use pagination when it return contacts will 10 contacts per page.
4. additional Bonus: contact can be add to favorites.

## NFRs
1. the app should scale.
2. test should to be written.
3. app should print logs.

## Open Issues:
1. by which filter the search should find contacts?
2. the search could find more than one contact? 
for example if I search for the first name "tomer" and I got 20 "tomer"s, should I need to return all of them, or we assume that I search only unique property that the contact has?
3. 