# Raw-Data-Testing-Framework
This is a framework for testing raw data that was being developed at Stellar Health. This code is non proprietary and Stellar health has allowed me to take my code fore demonstrative purposes with me

LOG_________________________________________________________________________________________________________________________________________________________________

10/27

Handled for different seperator types for txt files using regex.

Repo for TI to share and develop scripts and tooling for internal usage

* * * * * * * Functions created and their parameters are listed at the bottom of this document * * * * * * *


10/24 V2.1 

Increased user ease of use:
    -Files will be stored in a folder seperate from any other files and outside of the ti-playyground folder to avoid PHI breaches
    -Script addresses you as a person
    -Outputs clear
Formatted the output for the template
Mapping file v2 with horizontal layout for consolodation of all business entities and LOBs
 

10/18 added funcion 'import_or_install' so that a new user will have their packages installed automatically if the package requirements are not satisfied

10/16

-Added all functions to test_functions.py
-Created new function for accepting all file types located in utility_functions.py


v2.0 End to end dynamic column calls testing for member file and outputs to worksheet


v1.2 Dynamic capabilities

insider your repo you will find a few new files

test_mapping - this will the structure which we will use to create the dynamic ingest. The stellar values should be agreed upon by the team and then for each customer we create a mapping. 

Q. Will we create a mapping per tab or in some other way?
A. Not sure yet


utility_functs.py has been updated with a new function client_constructor - this function is called against a dataframe and that creates a dictionary mapping that customer's columns to the standard columns

test_functs.py has been updated. The column references have been replaced by variables in {curly braces}. What we do is we create a variable in curly braces and then at the end of the string use the .format method to set the inputs for the test function.

Raw_data v1.0 is updated to work with dynamic capabilities
_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

v1.1 -  Multi Table functionality framework

This is NOT the most elegant solution for calling multiple files to join together. 
However in the interest of time we need to have some sort of process to set up a table made out of two or more files from which a test is run

eg:

We have an eligibility file and a demographic file

for Eligibiltity we can run tests on that file alone such as

    Select member_id, max(eligibility_end_date) from table where max(eligibility_end_date) > TODAY()
    #to get a list of patients who have lost eligibility and we should expect them to show up in the "dropped" numbers

for Demographic we can run tests such as 

    Select member_id, (count distinct member_id) from table group by member_id
    #to generate a list of duplicate member_ids that should be a flag for escalation. 

For certain tests, we are going to need to join two files together first to conduct a test.

A more elegant solution could be had but we need to get moving on dynamic capabilities. So in the interst of time, I have created a v1.1 process which requires some attention from the user

WHAT YOU WILL DO TO RUN

1. Hit run
2. You will be prompted three times for inputs. 
3. The program will display a list of files which should be all the files you have dropped in the folder. 
4. Each file has a number next to it. 
5. Enter the number into the box and hit enter. 
6. After the last input is recorded, the script will THEN run and give you an output based on those files

Again, not the most elegant because you still need to interact. But I am trying to build this with minimal human input to minimize human error.\

