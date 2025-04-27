# **Personal Blog**
This is a simple personal blog web application built using Flask.
It allows you to view articles and provides an admin dashboard where authenticated users can add, edit, and delete articles.

## Features
📰 View a list of published articles (stored as .json files).

🔒 Admin authentication with username and password.

🛠️ Admin Dashboard to manage articles:

Add a new article

Edit an existing article

Delete articles

🖥️ Simple and responsive UI (no JavaScript required).

🚪 Session-based login/logout system.

## **Project Structure**
blog_app/  
│
├── app.py              # Flask application logic  
├── templates/          # HTML templates for the web pages  
│   ├── add_article.html  # Add article page      
│   ├── article.html      # Single article page     
│   ├── dashboard.html    # Admin dashboard page   
│   └── edit_article.html # Edit article page  
│   ├── home.html      # Home page displaying articles   
│   └── login.html # Admin login page   
└── README.md        

## How to Add Articles
1. Go to /admin/login
2. Log in with admin credentials
3. Use the "Add Article" button on the dashboard
4. Fill in the title and content → Save

Each article is saved as a .json file inside the articles/ folder automatically.
