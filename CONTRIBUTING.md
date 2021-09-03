# Contributing to Inscriptis

First off, thank you for considering contributing to inscriptis. 
There are many ways how you can contribute to the project and these guidelines aim at supporting you in doing so.

1. [Reporting bugs and seeking support](#reporting-bugs-and-seeking-support)
2. [Suggesting enhancements](#suggesting-enhancements)
3. [Pull requests](#pull-requests) (contributing code)
4. [Python style guide](#python-style-guide)


## Reporting bugs and seeking support

Bugs and support requests are tracked as GitHub issues.

To create an effective and high quality ticket, please include the following information in your
ticket:

 1. **Use a clear and descriptive title** for the issue to identify the problem. This also helps other users to quickly locate bug reports that affect them.
 2. **Describe the exact steps necessary for reproducing the problem** including at least information on
    - the affected URL
    - the command line parameters or function arguments you used
 3. What would have been the **expected behavior**?
 4. Describe the **observed behavior**.
 5. Provide any additional information which might be helpful in reproducing and/or fixing this issue. 


## Suggesting enhancements

Enhancements are also tracked as GitHub issues and should contain the following information:

 1. **A clear and descriptive title** helps other people to identify enhancements they like, so that they can also add their thoughts and suggestions.
 2. **Provide a step-by-step description** of the suggested enhancement.
 3. **Describe the current behavior** and **explain which behavior you expected to see instead** and why.


## Pull requests

1. Ensure that your code complies with our [Python style guide](#python-style-guide).
2. Write a unit test that covers your new code and put it into the `./tests` directory.
3. Execute `tox .` in the project's root directory to ensure that your code passes the static code analysis, coding style guidelines and security checks.
4. In addition, please document any new API functions in the Inscriptis documentation.


## Python style guide

Inscriptis code should comply to
- the [PEP8 Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/), and
- to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Please also ensure that 
1. functions are properly documented with docstrings that comply to the Google Python Style Guide, and
2. any new code is covered by unit tests.

