
# 🛡️ ComLTD Web Application - Secure vs Vulnerable Full-Stack Project

## 📖 Overview
**ComLTD** is a fictional communication company offering internet data packages, serving as the backdrop for this **full-stack web application project**.  
The project’s unique purpose is to demonstrate **secure development practices** alongside **common web vulnerabilities**, including **SQL Injection** and **XSS (Cross-Site Scripting)**.

This dual-backend architecture provides both:
- ✅ **Protected Backend:** Secure implementation with input sanitization, parameterized queries, and validation.
- ❌ **Vulnerable Backend:** An intentionally flawed implementation to demonstrate how common attacks can exploit insecure code.

This project reflects **secure coding principles**, **vulnerability exploitation scenarios**, and **full-stack development skills**, combining **ReactJS, FastAPI, MySQL, and Docker**.

---

## 🎯 Key Learning Objectives
- ✅ Understanding and implementing **secure coding best practices**.
- ✅ Simulating and demonstrating **real-world web attacks**.
- ✅ Applying **full-stack development principles** in a real environment.
- ✅ Building containerized applications for **consistent deployment**.

---

## 🏗️ Project Architecture

| Layer        | Technology      | Description |
|--------------|----------------|-------------|
| **Frontend** | ReactJS         | Interactive UI with dynamic forms, package browsing, and customer management |
| **Backend**  | FastAPI (Python) | Two versions: Secure & Vulnerable |
| **Database** | MySQL            | Persistent relational data storage |
| **Containerization** | Docker & Docker Compose | Environment consistency and simplified deployment |

---

## 🛠️ Core Features

### 🔐 Secure Features (Protected Backend)
- **User Registration & Login:** With **hashed passwords** and input sanitization.
- **Password Recovery:** Email-based token system for secure resets.
- **Customer Management:** Add, edit, delete customers safely.
- **Data Packages Display:** Browse company offerings.
- **Contact Form:** Secure user feedback with email notification.

### 🚨 Vulnerability Demonstrations (Vulnerable Backend)
- **SQL Injection:** Direct string concatenation allowing injection in:
    - Registration
    - Login
    - Customer Search
- **Stored & Reflected XSS:** Malicious scripts stored in:
    - Customer Details
    - User Registration Form

---

## 🔎 Security Demonstration Scenarios

| Attack Type | Scenario | Impact |
|---|---|---|
| **SQL Injection** | Bypass login by injecting OR-based queries | Gain unauthorized access |
| **SQL Injection** | Inject UNION query into customer search | Extract sensitive data |
| **Stored XSS** | Inject `<script>` tags in customer names | Persistent script execution |
| **Reflected XSS** | Inject payload in URL query parameters | Immediate script execution |

---

## 🐳 Deployment Instructions

1️⃣ **Clone Repository**
```bash
git clone https://github.com/ItayVazana1/ComLTD_FullProject.git
cd ComLTD_FullProject
```

2️⃣ **Configure Environment**
- Set database credentials and backend URLs in `.env` files (frontend & backend).

3️⃣ **Launch with Docker Compose**
```bash
docker-compose up --build
```
4️⃣ **Access Application**
- Frontend: [http://localhost:3000](http://localhost:3000)
- **Protected Backend:** [http://localhost:10000](http://localhost:10000)
- **Vulnerable Backend:** [http://localhost:11000](http://localhost:11000)

---

## 📂 Project Structure

```
ComLTD_FullProject/
├── frontend/              # ReactJS frontend
├── backend_protected/     # Secure FastAPI backend
├── backend_vulnerable/    # Vulnerable FastAPI backend
├── docker-compose.yml     # Docker configuration
└── init.sql                # Initial MySQL schema & data
```

---

## 🛡️ Secure Coding Practices (Protected Backend Highlights)

- ✅ **Input Validation & Sanitization**
- ✅ **Use of Parameterized Queries (SQLAlchemy)**
- ✅ **Password Hashing & Secure Storage**
- ✅ **Cross-Origin Resource Sharing (CORS) Controls**
- ✅ **Centralized Error Handling & Logging**

---

## 🚨 Key Security Risks Highlighted (Vulnerable Backend)

| Risk | Description |
|---|---|
| **SQL Injection** | Dynamic queries without sanitization |
| **XSS** | Direct rendering of unsanitized user input |
| **Weak Authentication** | No hashing or token expiration enforcement |

---

## 🔬 Key Technologies

| Layer | Tools |
|---|---|
| **Frontend** | ReactJS, HTML, CSS |
| **Backend** | FastAPI (Python), SQLAlchemy (secure), MySQL-Connector (vulnerable) |
| **Database** | MySQL |
| **Containerization** | Docker, Docker Compose |

---

## 💼 Key Takeaways

This project showcases:
- ✅ My ability to build **full-stack web applications**.
- ✅ My understanding of **web security vulnerabilities**.
- ✅ My proficiency in **ReactJS, FastAPI, and Docker**.
- ✅ My analytical thinking in identifying & mitigating risks.
- ✅ My experience balancing **functionality, usability, and security**.

---

## 👤 About the Author

**Itay Vazana**  
Aspiring Full-Stack Developer & Security Enthusiast  
🔗 [GitHub Profile](https://github.com/ItayVazana1)

---

## ⭐️ If you found this project valuable, please consider starring the repository!
