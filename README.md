# Smart Reminder Bot

A scalable, asynchronous Telegram bot built with FastAPI and MongoDB that allows users to schedule and manage reminders reliably.

---

## 📌 Overview
This project implements a reminder system that supports flexible time inputs and ensures reliable execution even after server restarts. It is designed with asynchronous processing to handle multiple users efficiently.

---

## ⚡ Key Features

### 🕒 Flexible Time Parsing
Supports multiple input formats:
- Relative: `10 mins`, `2 hours`
- Absolute: `19:30`, `1930`
- Specific dates: `31/03 10:00`

### 💬 Interactive Telegram UI
- Inline keyboards for managing reminders  
- Commands for creating, editing, and deleting tasks  

### 🌏 Timezone Handling (SGT - UTC+8)
- Consistent scheduling regardless of server location  
- Prevents timezone-related bugs  

### 💾 Persistent Storage
- Stores reminders in MongoDB Atlas  
- Data persists across server restarts  

### ⚙️ Asynchronous Architecture
- Built with FastAPI for non-blocking request handling  
- Supports multiple concurrent users efficiently  

---

## 🏗️ System Design

```
User → Telegram Bot → FastAPI Server → MongoDB Atlas
                              ↓
                        Scheduler / Worker
                              ↓
                      Sends Reminder to User
```

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** MongoDB Atlas  
- **Bot Framework:** python-telegram-bot  
- **Deployment:** Render  

---

## 📷 Example Usage

<img width="1403" height="1507" alt="image" src="https://github.com/user-attachments/assets/4c067746-4957-4790-b357-2628eb6e8f96" />

---

## 🧠 Key Engineering Decisions

- Used **asynchronous FastAPI** to handle concurrent users efficiently  
- Chose **MongoDB** for flexible schema design  
- Implemented **timezone normalization (UTC+8)** for consistent scheduling  
- Designed system to be **fault-tolerant** and recover after restarts  

---

## 🚧 Future Improvements

- Add Redis-based queue for distributed job scheduling  
- Support recurring reminders  
- Improve natural language parsing (e.g. “next Monday 5pm”)  
- Add user authentication & multi-device sync  

---


