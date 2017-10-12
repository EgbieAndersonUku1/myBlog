Project: Blog with a commenting and reply section. Also includes an admin section.

Project: Pending

Technologies that will be used:

1) Python 3.5
2) Database MongoDB
3) Flask
4) Pymongo (ORM)
5) Bootstrap, CSS, HTML, JavaScript for the admin panel interface
6) Selenium -> for automatic testing
 7) Microsoft word (Manual testing)
 8) Excel (Manual testing)
 
 In this section I am going to build a complete blog from the ground up.
 The blog will contain a section where users can comment as well as 
 replying to comments. I will also include an admin interface built using
 bootstrap.
 
 
 I will also be using a combination of testing. This will include  
 automatic testing, unit tests, manual testing, regression testing, exploration testing, 
 black box testing, white box testing, etc. After all an application without any
 tests is not worth writing.
  
 
 Installing and running
 --------------------------------------------------------------------------------
 
 1) To run the blog you can either create a virtual environment on your computer or not. Note this is optional.
 
       To create a virtual environment on **Linux** go to folder you like to create the virtual environment in
        and run the command:  **virtualenv 'type what name you like to call your virtual environment here without quotes' -p python3**
 
    This will create a virtual environment.
 
 2) If you have installed virtual environment activate it by use this command below or skip to step 3:
 
    **source 'The name of your virtual environment'/bin/activate**
 
3) Change into myBlog folder by running the command **cd myBlog**

4) Next run the command on the command line: **pip install -r requirement.txt**.
    This will download all the depencides needed to run the blog and store it in on your computer. 
 
 4) Change into the src folder by typing the command: **cd src**
 5) Run the command **python run.py runserver**. This will start the web server.
 6) Open a new browser and type in the url box: **http://127.0.0.1:5000**.
 To access any page just add a slash behind the link followed by the page.
 