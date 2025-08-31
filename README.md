

### Simple Invoice App

This is a Django-based web application designed to help a seller manage products and generate professional, customized receipts for clients. The application allows users to add, view, and delete products, and then select those products to generate a clean, printable PDF receipt.

### ✨ Features

  * **User Authentication:** Secure login and registration with a username and a 4-digit PIN.
  * **Product Management:** Easily add new products with details like name, quantity, price, discount, and tax.
  * **Dynamic Receipt Generation:** Select items from your product list, specify a quantity for each, and generate a PDF receipt for a client.
  * **Dashboard View:** A clean, responsive dashboard for managing products and generating receipts.
  * **Data Persistence:** Products, clients, and receipts are stored in a database.

### 🚀 Technologies Used

  * **Backend:** Python, Django
  * **Frontend:** HTML, Tailwind CSS for styling
  * **Database:** SQLite (default Django)
  * **PDF Generation:** The application is set up to use a PDF generation library (e.g., ReportLab) to create receipts.

### 🔧 How to Run Locally

Follow these steps to get the project up and running on your local machine.

#### 1\. Clone the Repository

Open your terminal and clone the project.

```bash
git clone https://github.com/bizimanasoftware/simple-invoice-app.git
cd simple-invoice-app
```

#### 2\. Create a Virtual Environment

It's a best practice to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

  * **On Windows:** `venv\Scripts\activate`
  * **On macOS/Linux:** `source venv/bin/activate`

#### 3\. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### 4\. Run Migrations

Apply the database migrations to set up the necessary tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5\. Create a Superuser

Create an admin account to access the Django admin panel and manage your data directly.

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your username and PIN.

#### 6\. Start the Development Server

Run the server to see the application in your browser.

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`. You can now register, log in, and start managing products and generating receipts\!

### 📂 Project Structure

A brief overview of the key directories and files:

  * **`myproject/`**: Main Django project configuration.
  * **`menu/`**: The core application, containing most of the project's logic.
      * **`models.py`**: Defines the database models for `CustomUser`, `Product`, `Client`, and `Receipt`.
      * **`views.py`**: Handles all the application logic, including user authentication, product management, and receipt generation.
      * **`forms.py`**: Contains the forms for registration, login, and adding products.
      * **`templates/`**: HTML templates for the different pages.
      * **`urls.py`**: Defines the URL routes for the `menu` app.
  * **`requirements.txt`**: Lists all Python dependencies for the project.
