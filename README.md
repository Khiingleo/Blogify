# Blogify - A Social Blogging Platform
 Blogify is a social blogging platform where users can create, view, update, and delete posts, comment on posts, like posts, manage their accounts, and more. It also includes features like profile pictures, account password reset via email, and password reset functionality.

## Features
- Create Posts: Users can create new blog posts to share their thoughts, ideas, and experiences with others.

- View Posts: Users can view all posts created by themselves and other users.

- View User's Posts: Users can view all posts created by a particular user.

- Update Posts: Users can edit and update their existing posts.

- Delete Posts: Users can delete their own posts if they no longer wish to keep them.

- Comment on Posts: Users can comment on posts to engage in discussions and provide feedback.

- Like Posts: Users can like posts to show appreciation for the content.

- Account Management: Users can create accounts, update their account information, and manage their profile picture.

- Password Reset: Users can request a password reset via email if they forget their password. They can then reset their password using the provided link.

## Technologies Used
- Flask: Flask is used as the web framework for handling HTTP requests and responses.

- Flask_SQLAlchemy: SQLAlchemy is used as the ORM (Object-Relational Mapping) library for interacting with the database.

- SQLite: SQLite is used as the relational database management system to store user data, posts, comments, likes, etc.

- Jinja2: Jinja2 is used as the template engine for rendering HTML templates with dynamic content.

- WTForms: WTForms is used for form validation and rendering HTML forms.

- Flask-Mail: Flask-Mail is used for sending password reset emails to users.

- Bcrypt: Bcrypt is used for password hashing to securely store user passwords.

- 

# Getting Started
Clone the repository:

```bash
Copy code
git clone https://github.com/yourusername/blogify.git
Install dependencies:
```

```bash
Copy code
(install the above technologies)
Set up the database:
```

```bash
Copy code
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Run the application:
```

```bash
Copy code
flask run
Access the application in your web browser at http://localhost:5000.
```

### Author
The author of Blogify is Shalom Ogoziem