# 🛒 Grocery Checkout System (Python / Tkinter)

## Overview

This project is a **desktop-based grocery checkout simulator** built with Python and Tkinter.

It models a simplified **point-of-sale (POS) system**, allowing users to:
- Select products
- Add quantities to a cart
- Apply membership-based discounts
- View a detailed bill and receipt

The application focuses on **clean business logic, user interaction, and real-world workflow simulation**.

---

## 🎯 Purpose

This project was created to explore:
- Structuring business logic in Python
- Building interactive desktop applications with Tkinter
- Modeling real-world systems like checkout and billing
- Implementing validation, state management, and user feedback

It serves as a **foundation for more advanced retail, POS, or inventory systems**.

---

## ✨ Features

### 🧾 Checkout Flow
- Add items to cart
- Automatically aggregates duplicate products
- Real-time subtotal calculation

### 💳 Membership Discounts
- Bronze → 0% discount
- Silver → 5% discount
- Gold → 10% discount

### 📊 Cart Management
- View all selected items
- Remove individual items
- Clear entire cart

### 💰 Billing System
- Itemized receipt preview
- Discount breakdown
- Final total calculation

### 🖥️ GUI Interface
- Built with Tkinter
- Structured layout (product input, cart view, totals)
- Input validation and error handling

---

## 🧠 Technical Highlights

- Uses `dataclasses` for clean data modeling
- Separates **business logic** from **UI layer**
- Handles invalid inputs gracefully
- Maintains cart state dynamically
- Designed with scalability in mind (can evolve into full POS system)

---

## 🚀 Getting Started

### Requirements

- Python 3.9+

(No external dependencies required)

### Run the Application

```bash
python grocery_checkout.py
```

🗂️ Project Structure (Recommended)
grocery-store/
│
├── grocery_checkout.py   # Main application
├── README.md
├── OLD/                  # Legacy code (optional)
⚠️ Known Limitations
No persistent storage (cart resets on restart)
Fixed product catalog (hardcoded items)
No inventory tracking
No database integration
Desktop-only (no web/mobile support)
🔧 Future Improvements (IMPORTANT)
🧠 Architecture & Code Quality
Split into modules:
ui/
services/
models/
Add logging instead of relying on UI-only feedback
💾 Data Persistence
Store:
transaction history
product catalog
Suggested tools:
SQLite (lightweight)
JSON (quick implementation)
🛍️ Inventory System
Track stock levels
Prevent purchases beyond available quantity
Add restocking functionality
📈 Enhanced Features
Add tax calculation
Add coupon / promo codes
Add multiple customers / sessions
Export receipt to file (TXT or PDF)
🌐 UI / UX Improvements
Add images for products
Improve layout and styling
Add keyboard shortcuts
Add search/filter for products
🌍 Expansion Ideas
Convert to web app (Flask / React)
Turn into REST API backend
Integrate with barcode scanner simulation
Multi-user checkout system
🧊 Portfolio Value

This project demonstrates:

Real-world problem modeling (checkout systems)
GUI application development
Input validation and error handling
Separation of concerns (logic vs UI)
Incremental system design thinking
👤 Author

Kenneth Lloyd Boller
AI / Automation / Systems Builder
Creator of Snowball AI
