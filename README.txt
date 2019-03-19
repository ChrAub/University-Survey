The files in this directory provide a survey about classes at university. 

It starts with some personal information:r
current semester
bachelor already finished? (either yes or no)
hours worked (part time jobs) in each semester

For each course the participant is asked for 
attendence (a mark in one of the four columns)
hours learned for the course
weather the course was passed passed? (either yes or no)
which semester the course was finished (it is possible to take a course up to 5 times)
If the course is not started, the line should be left empty. 
 
The question sheet was provided in Excel, so it is possible to make sure certain cells only contain specified values.
A simplified version of the question sheet is also provided in the directory. 

Data are then stored in a JSON-like structure (non persistent, but with about 100 participants reading time is small). 
Also ects.csv is read that contains a list with credit hours.
With the available data a bunch of analysis can be performed. Some useful functions are also included in the code.

