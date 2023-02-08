# Lil' Bank
The bank that cares about you, not the world, nor the 
policies of the other banks.

## Project Requirements

Lil' Bank is a project that is based on a simulation
of real world requirements.

A Bank requires a B2C Web Portal to collect the data 
about its customers through full-stack based web portal.

For this purpose, the data needs to be collected from 
various resources. The data needs to be maintained at 
a centralized location so that it is available to various 
sections including the Accounts and the Sales sections of 
various branches, regardless of the hardware and software 
platforms being used at the branches. 
It also needs to verify that the valid data is stored in 
a MySQL database.

The details of the customer are as follows,
- Customer ID
- Account No
- First Name
- Last Name
- Address
- Phone

A customer may specify residential or official contact information.
Bank wants to display the details of all its customers. 

The customer details must be available in MySQL & registered 
user details should be displayed in the tabular structure. 
Bank needs to display a summarized report about customers. 

## Features
- [X] Web Portal should have multiple menu items to perform tasks after login
- [X] Some menu option should have sub menu 
- [ ] Web portal should be with JavaScript based slider 
- [X] Web portal should have registration and login form
- [ ] Web portal should have search module 
- [X] Only authorized user should access the portal’s features.
- [X] Validate the Web form to get the required data 
- [X] Write methods for declaring fields to be used for storing structured data 
- [X] Validate the structure of data.  
- [ ] Display summarized data. 
- [ ] Can have caching management for improved performance 
- [X] State Management using sessions
- [X] User profiles 
- [X] Web portal should be compatible with all browsers 

## Other Challenges/Features

- [X] Use bootstrap for design pages
- [ ] Provide authentication, authorization using oauth or similar package
- [X] Create restful apis for app features
- [X] Provide swagger UI for rest api usage
- [ ] If possible or it’s optional, create micro-services for the app components using docker