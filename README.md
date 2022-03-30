CMPUT291 - Winter 2022\
Mini Project II
=======================================

(group project)
---------------

Due: Mar 30th at 5pm

### Clarifications:

You are responsible for monitoring the course discussion forum in eclass and this section of the project specification for more details or clarifications. No clarification will be posted after *5pm on March 28th*.

-   March 27. In "Search for cast/crew members," we want to see all professions of the member and for each title the member had a job or played a character in, we want to see the primary title, the job and character (if any).
-   March 26. [Here](https://eclass.srv.ualberta.ca/pluginfile.php/7954786/mod_page/content/111/prj2-rubric.txt?time=1648336670626) is a marking rubric for the project.
-   March 24. The "year" field in search for titles refers to the start year of movies. 
-   March 21. It is generally a good practice to do "one line at a time" processing" and not load a large chunk of data to memory if possible. That said, you can ignore the constraint if it makes your job easier for the first phase of the project.

### Introduction

The goal of this project is to teach the concept of working with data stored in files and NoSQL databases. This is done by building and operating on a document store, using MongoDB. Your job in this project is to write programs that store data in MongoDB and provide basic functions for searches and updates. 80% of the project mark would be assigned to your implementation, which would be assessed in a demo session, and is further broken down to two phases with 10% of the mark allocated for Phase 1 and 70% for Phase 2. Another 15% of the mark will be assigned for the documentation and quality of your source code and for your design document. 5% of the mark is assigned for your project task break-down and your group coordination.

### Group work policy

You will be doing this project with one or two other partner from the 291 class. Register your group at the [group registration page for mini-project 2](https://eclass.srv.ualberta.ca/mod/data/view.php?id=5846916). It is assumed that all group members contribute somewhat equally to the project, hence they would receive the same mark. In case of difficulties within a group and when a partner is not lifting his/her weight, make sure to document all your contributions. If there is a break-up, each group member will get credit only for his/her portion of the work completed (losing the mark for any work either not completed or completed by the partner). For the same reason, a break-up should be your last resort.

### Task

You are given four tab-separated files named as name.basics.tsv, title.basics.tsv, title.principals.tsv and title.ratings.tsv, which you will convert to json before loading them into MongoDB. Samples of these files are available at [google drive](https://drive.google.com/drive/folders/1byzefxDV-XUzt1HBq05jEWiZZs4XRaAd?usp=sharing) (use your ualberta account to access the files). The data is obtained from IMDb and includes information about movies, principal cast/crew members, and ratings. More information about these files, their fields as well as larger files is available at imdb.com/interfaces. Your job is to create MongoDB collections, following Phase 1, and support searches and updates in Phases 2.

### Phase 1: Building a document store

For this part, you will write two programs. One program, named *tsv-2-json* with a proper extension (e.g. *tsv-2-json.py* if using Python), will read the four tsv files in the current directory and convert them to [json](https://en.wikipedia.org/wiki/JSON) files. The file names should remain the same except the extension which will change to json. The columns *primaryProfession, knownForTitles, genres* and *characters* are of type array and should be represented as nested arrays in json. You can use the resources on the Web with a proper citation (e.g. [here](https://www.geeksforgeeks.org/python-tsv-conversion-to-json/) is a sample program but does not do nesting).

Another program, named *load-json* with a proper extension (e.g. *load-json.py* if using Python), will take those four json files in the current directory and constructs a MongoDB collection for each. Your program will take as input a port number under which the MongoDB server is running, will connect to the server and will create a database named 291db (if it does not exist). Your program then will create four collections named *name_basics, title_basics, title_principals* and *title_ratings* respectively for name.basics.json, title.basics.json, title.principals.json and title.ratings.json. If those collections exist, your program should drop them and create new collections. Your program for this phase ends after building these collections.

Important Note: None of the files can be fully loaded into memory. The input files are expected to be too large to fit in memory and you can only process them as one-row-at-a time.

### Phase 2: Operating on the document store

Write a program that supports the following operations on the MongoDB database created in Phase 1. Your program will take as input a port number under which the MongoDB server is running, and will connect to a database named 291db on the server.

Next, users should be able to perform the following tasks.

1.  Search for titles The user should be able to provide one or more keywords, and the system should retrieve all titles that match all those keywords (AND semantics). A keyword matches if it appears in the primaryTitle field (the matches should be case-insensitive). A keyword also matches if it has the same value as the year field. For each matching title, display all the fields in title_basics. The user should be able to select a title to see the rating, the number of votes, the names of cast/crew members and their characters (if any).

2.  Search for genres The user should be able to provide a genre and a minimum vote count and see all titles under the provided genre (again case-insensitive match) that have the given number of votes or more. The result should be sorted based on the average rating with the highest rating on top.

3.  Search for cast/crew members The user should be able to provide a cast/crew member name and see all professions of the member and for each title the member had a job, the primary title, the job and character (if any). Matching of the member name should be case-insensitive.

4.  Add a movie The user should be able to add a row to title_basics by providing a unique id, a title, a start year, a running time and a list of genres. Both the primary title and the original title will be set to the provided title, the title type is set to movie and isAdult and endYear are set to Null (denoted as \N).

5.  Add a cast/crew member The user should be able to add a row to title_principals by providing a cast/crew member id, a title id, and a category. The provided title and person ids should exist in name_basics and title_basics respectively (otherwise, proper messages should be given), the ordering should be set to the largest ordering listed for the title plus one (or 1 if the title is not listed in title_principals) and any other field that is not provided (including job and characters) set to Null.

After each action, the user should be able to return to the main menu for further operations. There should be also an option to end the program.

### Testing

At development time, you will be testing your programs with your own data sets but conforming to the project specification.

At demo time, we will be testing your programs with our test data files that have the same names as given above on lab machines. Using your submitted code, we will (1) build a MongoDB database in Phase 1, and (2) perform search and update operations in Phase 2. We typically follow a 5 minutes rule for Phase 1, meaning your database should be built in less than 5min. If not, we may have to use our own database, in which case you would lose the whole mark for Phase 1.

Every group will book a time slot convenient to all group members to demo their projects. At demo time, all group members must be present. Our TAs will be asking you for instruction to perform various tasks and to test how your application is handling each task. A mark will be assigned to your demo on the spot after the testing.

Here are some important details about our testing process and your choices (same as in Project 1):

1.  The demo will be run using the source code submitted and nothing else. Don't hard-code the port number in your application since the port number is not known in advance, and you don't want to change your code at demo time. The test files will follow the same formatting as the samples (in terms of field names and types) but will be larger. Your application will be tested under a TA account.
2.  We must be able to compile and run your code under our account on undergrad machines and using our own database. You are not allowed to make any changes to the code without a hefty penalty.
3.  Our test data and our test cases will be published after the project due date but before our demo times. This means, you have a chance to test your application and learn about possible issues (if any) before your demo time.
4.  Your code cannot be demoed on a laptop (yours or ours) or any machine other than the lab machine with only one exception. The exception is if you are developing your application using a less traditional programming language or tool that is not available on lab machines, you MAY be allowed to demo your application on a laptop. Those cases should be discussed with the instructor well before the project due date and an approval must be obtained. Otherwise, you cannot demo your project on any machine other than the lab machines.

### Instructions for Submissions

Your submission includes (1) the application source code for phases 1 and 2, (2) README.txt, and (3) a short report named *Report.pdf*. Your source code must include at least two programs, i.e. one for each phase. Your program for Phase 2 would implement a simple query interface in your favourite programming language (e.g. Python, C or C++, Java).

-   Create a single gzipped tar file with (1) all your source code, (2) README.txt, and (3) your project report. Name the file *prj2code.tgz*.
-   Submit your project tarfile in [the project submission site](https://eclass.srv.ualberta.ca/mod/assign/view.php?id=5846924) by the due date at the top of this page.
-   All partners in a group must submit their own copies (even though the copies may be identical)!

The file README.txt is a text file that lists the names and ccids of all group members. This file must also include the names of anyone you collaborated with (as much as it is allowed within the course policy) or a line saying that you did not collaborate with anyone else. This is also the place to acknowledge the use of any source of information besides the course textbook and/or class notes. Your report must be type-written, saved as PDF and be included in your submission. Your report cannot exceed 3 pages.

The report should include (a) a general overview of your system with a small user guide, (b) a detailed design of your software with a focus on the components required to deliver the major functions of your application, (c) your testing strategy, and (d) your group work break-down strategy. The general overview of the system gives a high level introduction and may include a diagram showing the flow of data between different components; this can be useful for both users and developers of your application. The detailed design of your software should describe the responsibility and interface of each primary function or class (not secondary utility functions/classes) and the structure and relationships among them. Depending on the programming language being used, you may have methods, functions or classes. The testing strategy discusses your general strategy for testing, with the scenarios being tested and the coverage of your test cases. The group work strategy must list the break-down of the work items among partners, both the time spent (an estimate) and the progress made by each partner, and your method of coordination to keep the project on track. The report should also include any assumption you have made or any possible limitations your code may have.