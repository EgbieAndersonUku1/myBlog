Blog
--------------------------------------------------------------------------------------------


Project: To build a working blog complete with an admin section. The user of the blog will be able to create where mulitple blogs each with its own commenting and reply section.

Project Status: **Complete..**

Project Description

In this section I am going to build a complete blog from the ground up.
 The blog will contain a section where users can comment as well as 
 replying to comments. I will also include an admin interface built using
 bootstrap.
 
 
 I will also be using a combination of testing. This will include  
 automatic testing, unit tests, manual testing, regression testing, exploration testing, 
 black box testing, white box testing, etc. After all an application without any
 tests is not worth writing.
 
 
Technologies that will be used:

1) Python 3.5 does not work using python 2.7x
2) Database MongoDB
3) Flask
4) Pymongo (ORM)
5) Bootstrap, CSS, HTML, JavaScript for the admin panel interface
6) Selenium -> for automatic testing mostly UAT (User Acceptance Testing)
6) Unit tests
 7) Microsoft word and Excel (Manual testing)

 
 Installing and running (Commands to be done on the command line)
 --------------------------------------------------------------------------------
 
 1) To run the blog you can either create a virtual environment on your computer or not. Note this is optional.
 
       To create a virtual environment on **Linux** go to the folder you would like to create the virtual environment in
        and run the command:  **virtualenv 'type what name you like to call your virtual environment here without quotes' -p python3**
        You must already have virtualenv stored on your computer. In the case virtualenv is not installed in your computer
        run the following command on your computer **pip install virtualenv**. This act will install virtualenv on your computer.

 2) If you chosen to install the virtual environment on your computer then activate it by use this command below or **skip to step three**.
 
    **source 'The name of your virtual environment without quotes'/bin/activate**
 
3) Change into myBlog folder by running the command **cd myBlog/src**

4) Next run the command: **pip install -r requirement.txt**.
    This will download all the dependencies needed to run the blog and store it in on your computer or your virtual environment if you have created one.
 
 6) Open a new terminal and run the command sudo mongod. This will start the database.
 7) In the file gmail_credentials.env enter your gmail username and password in the appropriate variables and hit save
 7) Turn **ON** the **less secure app** setting located in your gmail setting account. This allows gmail to use scripts in order
 to send emails. If this is not turned on and error would occur if application tries to send an email.
 7) Run the command **python run.py runserver**. This will start the web server.
 7) Open a new browser and type in the url box: **http://127.0.0.1:5000**.
 
 Should an error occur stop step 8 and by hit CTRl-D and then do step 8 again.
 To access any page just add a slash behind the URL followed by the page name
 
 Should an error occurs stating that there is a missing value <missing blank variable name> delete the mongod database from the shell and then run step 8 again
 
 To Delete the mongod database do the following steps.
 
 Open a terminal
 1) Type in 'mongo' in the shell
 2) Type the commmand 'use blogs'
 3) Type the command drop 'db.blogs.drop()'
 A message should occur stating true.

The database will now be empty


 Things needed to run the blog
 ----------------------------------------------------------------------
 
 1) Any operating system 
 2) A working internet connection 
 
