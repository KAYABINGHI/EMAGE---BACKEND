
# 🌿 EMAGE — People-First Wellness Platform

A modern wellness and self-care platform built with a React frontend and Flask backend, designed to help users discover trusted wellness resources, supportive services, and curated programs for better mental and emotional wellbeing.

## 📑 Table of Contents

- ✨ Features

- ⚡ Quick Start

- 🔑 Authentication Setup

- 📡 API Endpoints

- 🌱 Usage

- 🛠️ Technologies Used

- 🔒 Privacy & Security

- 👥 Authors

- 🤝 Contributing
## ✨ Features

🧘 Wellness & Self-Care

- Curated catalog of self-care and wellness programs

- Transparent pricing for paid and free offerings

- Short, actionable guidance and wellbeing tips

- Testimonials and social proof for credibility

- Newsletter for regular mental health prompts and updates

🔐 Authentication

- JWT-based authentication (access & refresh tokens)

- Email/password registration & login

- Protected routes and secure logout with token revocation

- Personalized user dashboard for saved services and preferences

🌍 Accessibility & Human-Centered Design

- Clean, readable typography

- Semantic HTML for screen-reader compatibility

- Minimal data collection with explicit opt-ins

- Inclusive, compassionate language
## ⚡ Quick Start

🔧 Backend Setup

```
export PIPENV_VENV_IN_PROJECT=1
pipenv install
pipenv shell
python main.py 
```
💻 Frontend Setup

```
npm install
npm run dev
```
## 🔑 Authentication Setup

### Register

Provide the following:

  1. Username

  2. Email
 
  3. Phonenumber
  4. Password
  

### Login

- Use your email, Phonenumber and password
## 📡 API Endpoints

🔐 Authentication

- ```POST / register``` -> register
- ```POST /login``` -> login
- ```POST /forgot``` -> forgot password

🌱 Services & Resources
- ```GET / community``` -> list_communities
- ```POST / community``` -> create community

💬 Contact & Newsletter
- ```POST / post_message``` -> send a message
- ```POST /message``` -> connect_users
## 🌱 Usage
- Register/Login to your account

- Explore self-care tips and curated wellness services

- Compare pricing and read testimonials

- Book or save your preferred service

- Subscribe to the newsletter for regular wellbeing prompts

- Log out securely when done
## 🛠️ Technologies Used
- Backend: flask-jwt-extended. flask-cors. flask-bcrypt. flask. flask-sqlalchemy. flask-migrate. psycopg. python-dotenv. flask-softdelete 
- Frontend: tailwindcss/vite, axios, boring-avatars, lucide-react, react, react-dom, react-router-dom, sweetalert2,tailwindcss
- Database: PostgreSQL/Supabase
## 🔒 Privacy & Security
- JWT tokens (access = 60sec, refresh = 60sec)

- Token revocation on logout

- Password hashing with bcrypt

- CORS configuration for frontend-backend communication

- Minimal personal data collection — explicit user consent for contact/newsletter
## 👥 Authors
- [@KAYABINGHI](https://www.github.com/KAYABINGHI)
- [@BKiptoo](https://github.com/BKiptoo)
- [@moen-roy](https://github.com/moen-roy)
- [@Angellucy460](https://github.com/Angellucy460)