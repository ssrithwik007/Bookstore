# 📚 BookStore App

A web-based bookstore management system with a clear role-based access model. Built using **Streamlit** for the frontend and **FastAPI** for the backend, powered by **PostgreSQL** with **SQLAlchemy ORM**.

---

## 🧱 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL

---

## 👥 Roles & Permissions

### 🔐 Admin (Superuser)
- Only one admin exists.
- Admin account is **auto-created** when the database is initialized.
- **Capabilities**:
  - View all books
  - Add, update, and delete *any* book
  - View all user information (excluding passwords)

### 🧪 Trial-Admin
- Created by others for demo purposes with **limited admin privileges**.
- **Capabilities**:
  - View all books
  - Add new books
  - Update/delete only the books *they* added
  - Update their own credentials
  - Delete their own account

### 👤 User
- Regular account created by visitors.
- **Capabilities**:
  - Browse all books
  - Add books to cart
  - Purchase books & checkout
  - Refund specific books or all books
  - Update own credentials
  - Delete own account

---

| Feature            | Admin | Trial-Admin | User |
| ------------------ | ----- | ----------- | ---- |
| View all books     | ✅     | ✅           | ✅    |
| Add books          | ✅     | ✅           | ❌    |
| Update any book    | ✅     | ❌           | ❌    |
| Update own books   | -     | ✅           | ❌    |
| Delete any book    | ✅     | ❌           | ❌    |
| Delete own books   | -     | ✅           | ❌    |
| View user info     | ✅     | ❌           | ❌    |
| Update own profile | ❌     | ✅           | ✅    |
| Delete account     | ❌     | ✅           | ✅    |
| Add to cart        | ❌     | ❌           | ✅    |
| Checkout cart      | ❌     | ❌           | ✅    |
| Refund books       | ❌     | ❌           | ✅    |

