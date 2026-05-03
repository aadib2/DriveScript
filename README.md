# DriveScript
Source Code for DriveScript Esoteric Programming Language. Created as part of SDSU CS 420: Advanced Programming Languages

Final Project Submission
1. Complete the implementation of your language. Demonstrate five examples.

(a) Write two (3) simple programs using your programming language. Save the files as the proper extension. For instance, if your language is called star, write a program called hello_world.star.

b) Implement a simple interpreter that i) parses your language, and b) interprets the language and gives an output  

c) Write at least one (1) complex additional programs using your programming language.

d) Write one (1) program for your language that runs FizzBuzz.

e) Run your interpreter against these more complex programs.

 

BONUS: Bonus points for creativity.

 

2. Create a Simple Website for your Language and make sure the Interpreter is uploaded to GitHub

See: https://lhartikk.github.io/ArnoldCLinks to an external site.


Help with Web Dev / Git: https://www.theodinproject.com/Links to an external site. 

Submit the following links...

Live Website Link: ___

Git Source Code Link: 

 

3. Slides Presentation

Create a Slideshow presentation of your work. Your work should include your entire report, as well as all of your examples. Be sure to include:

Programming Language Name
Programming Language Purpose & Philosophy
Programming Language Style
Go over your Language philosophy and why you created it
Explain your Three (3) programs and explain how they work
Demonstrate your interpreter running the Six (6) programs



Claude do the following:
right now we want to focus on finalizing the interpreter implementation and the sample programs. 

Firstly let's add support for the LISTEN command which allows for user input and reading bytes into cells

Next,  to get entire fizzbuzz working (1 through 100)  - the code would be hundreds of lines long, we want to shorten it by creating some sort of standard library of reusable patterns that could be implemented as "include" files (in CPP). These could include support for multipication, division, modulo and others.
