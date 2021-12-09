# Jackpot

Jackpot is an online purchasing platform where users can join communities and exchange products and services from members known to them safely. Jackpot is all about security, community and ease!

This README will guide through the steps required to set up this application, and some information about the challenges and achievements of Jackpot.

You can access the Jackpot website here [here](https://jackpot-communities.herokuapp.com/).

## Installation and Usage

### Installation
- Clone or download this repo.
- In the terminal, navigate to the `django-ecommerce-final-project` folder.
- In the terminal, enter the pipenv environment using `pipenv shell`. Then run `pipenv install` to install the required packages.

### Usage
- In the terminal, use the command `python manage.py runserver` to launch the app.

## Technologies Used
* Heroku for deploying the site.
* HTML and CSS.
* Django for our backend framework.
* Postresql for our database.
* Bootstrap for styling.
* Pytest to test our app.
* VS code was our code editor.
* Github for version control.
* Zoom and Slack for collaboration and communication between team members.

## Process
1. Started by writing a brief for our project. This can be found [here](https://gist.github.com/ZNBrown/08f7627f2c83cc7f6ccf836c284e4ed3).
2. Planned the structure of our database and used Figma to design the styling of our app.
3. Created a repo on GitHub.
4. Created our initial file structure and set Django boilerplate.
5. Create a Kanban board and filled it with tasks that needed completing.
6. We set up our models, views and urls in Django.
7. Started testing our models, views and urls
8. Created our html templates.
9. Implemented functionality for all of our different forms.
10. Started implementing paypal to allow users to pay.
11. Added styling to our site using Bootstrap.
12. Finished any testing and removed any unnecessary code.


## Bugs


## Wins & Challenges

### Wins
* Worked really well as a team, with constant communication throughout.
* Achieved our Minimum Viable Product.
* Implemented paypal so that users can pay for products and sellers receive those payments.
* App is successfully styled with a mobile first design.
* Website successfully deployed on Heroku.

### Challenges
* Issues when trying to deploy our database on Heroku. To resolve these issues, we moved from SQLite to Postresql.
* We wanted users to be able to log in to their account using their email address rather than a username. To achieve this, we created a custom Member class.

### Future Features
* Give users the option of posting their products to social media. We plan to implement this using Django social share.
* Implement domain verifications so that communities for specific workplaces or universities include automatic verification for anyone requesting to join with a verified email address.
* Allow admins to change the colour theme for their community for extra personalisation.
