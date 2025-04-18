# E-Commerce Backend API

Backend API untuk aplikasi e-commerce menggunakan Flask dan SQLAlchemy.

## 📁 Struktur Project

```
project/
├── model/
│   ├── userModel.py      # Model untuk user dan autentikasi
│   ├── productModel.py   # Model untuk produk
│   ├── cartModel.py      # Model untuk shopping cart
│   └── orderModel.py     # Model untuk order dan items
├── services/
│   ├── auth_service.py   # Logic autentikasi (register, login)
│   ├── product_service.py # Logic manajemen produk
│   ├── cart_service.py   # Logic shopping cart
│   └── order_service.py  # Logic order dan checkout
├── schemas/
│   ├── auth_schema.py    # Validasi request/response auth
│   ├── product_schema.py # Validasi product
│   ├── cart_schema.py    # Validasi cart
│   └── order_schema.py   # Validasi order
├── routes/              # (Coming soon)
├── connector/
│   └── db.py           # Konfigurasi database
├── app.py              # File utama aplikasi
├── .env               # Environment variables
├── .gitignore
├── poetry.lock        # Dependencies lock
└── pyproject.toml     # Project configuration
```

## 💻 Teknologi yang Digunakan

- Python 3.9+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Flask-JWT-Extended (Autentikasi)
- Marshmallow (Validasi)
- Poetry (Package Manager)

##  Penjelasan Kode

### Services

#### 1. Auth Service (`services/auth_service.py`)
- Menangani registrasi user baru
- Login dan generate JWT token
- Validasi email dan password
- Handling optional profile fields

#### 2. Product Service (`services/product_service.py`)
- CRUD operations untuk produk
- Filtering dan sorting produk
- Pagination hasil query
- Soft delete untuk produk

#### 3. Cart Service (`services/cart_service.py`)
- Manajemen shopping cart
- Add/update/remove items
- Validasi stok produk
- Perhitungan total items dan amount

#### 4. Order Service (`services/order_service.py`)
- Checkout process
- Order history
- Pembatalan order
- Manajemen stok produk

## 🚀 Langkah Selanjutnya

### 1. Implementasi Routes
- [ ] Buat route auth (`/auth/register`, `/auth/login`)
- [ ] Buat route products (`/products`, `/products/<id>`)
- [ ] Buat route cart (`/cart`)
- [ ] Buat route orders (`/checkout`, `/orders`)

### 2. Setup Database
- [ ] Buat migration files
- [ ] Setup initial data/seeder
- [ ] Test koneksi database

### 3. Security & Middleware
- [ ] Implementasi JWT authentication middleware
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Error handling

### 4. Testing
- [ ] Unit tests untuk services
- [ ] Integration tests untuk API endpoints
- [ ] Load testing

### 5. Documentation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Setup instructions
- [ ] Deployment guide

## 🛠 Setup Development

1. Clone repository
```bash
git clone <repository-url>
```

2. Install dependencies
```bash
poetry install
```

3. Setup environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations
```bash
flask db upgrade
```

5. Run development server
```bash
poetry run flask run
```

## 📝 API Endpoints (Coming Soon)

### Auth
- `POST /auth/register` - Register user baru
- `POST /auth/login` - Login user

### Products
- `GET /products` - List semua produk
- `GET /products/<id>` - Detail produk
- `POST /products` - Tambah produk baru
- `PUT /products/<id>` - Update produk
- `DELETE /products/<id>` - Hapus produk

### Cart
- `GET /cart` - Lihat cart
- `POST /cart` - Tambah item ke cart
- `PUT /cart/<item_id>` - Update quantity
- `DELETE /cart/<item_id>` - Hapus item dari cart

### Orders
- `POST /checkout` - Checkout cart
- `GET /orders` - List order history
- `GET /orders/<id>` - Detail order
- `POST /orders/<id>/cancel` - Batalkan order

## 👥 Contributors
- [Your Name]

## 📄 License
MIT License