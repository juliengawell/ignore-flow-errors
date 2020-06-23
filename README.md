#Ignore flow errors

##What’s this document about ?

This document talks about:
A short introduction to Flow
Flow installation
The issue we need to solve
The solution used and its implementation
What could be done further


##Introduction

Flow is a static type checker for JavaScript first introduced by Facebook. It was conceived with a goal of finding type errors in JavaScript code. It also adds additional syntax to JavaScript that provides more control to the developers.


Flow installation

First of all, Flow must be installed in our repository.

The easiest way to install it is via npm:

npm install --save-dev flow-bin

The most efficient way to use Flow is to use the Flow server which will check the file incrementally, which means that it only checks the part that has changed.

The Flow server can be started by running on the terminal the command:

npm run flow

which will display maximum 50 errors and the total number of errors detected.

The Flow server can be stopped by running on the terminal the command:

npm run flow stop


##Issue we need to solve

There are too many issues to resolve initially. If we run the command flow in our repository and the output shows 1000+ errors it would be almost impossible to fix all flow errors at once. It would be possible to fix them manually one by one using the $FlowFixMe comment which will ignore the flow error on the following line but it can be very time consuming. Moreover, it would be necessary to correct all the errors manually all at once after adding or modifying the code base.


##Solution

Create a Python script to store the output of the flow --json command in a .json file, group errors by file and add automatically the comment $FlowFixMe to the line before the one with an error.


##Implementation

This script is separated into three steps. 

In the third for each error in the file we add the comment $FlowFixMe to the line before the one containing an error. We also create a counter that we will increment for each error in the file. If we don't do this, when we add a comment to the file, the line with the next error will be on the next line and so the comment will be 2 lines above it and so forth.
(i.e if there is an error on lines 5 and 10 and a comment is added on line 4 to ignore the error on line 5, the error on line 10 is now on line 11 and the comment to ignore this error will be on line 9)


##What could be done further

Currently, errors in jsx code are not handled because the syntax for writing a comment is different from that of pure Javascript code.
We could add a feature that would allow us to adapt the syntax of the comment if the error is in jsx or in pure Javascript code.
