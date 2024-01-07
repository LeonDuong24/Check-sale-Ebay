# Check sale Ebay

## Description

This project is a Flask-based web application that allows users to input a link to a product on eBay along with a desired price. The application monitors the prices of these products over time and sends email notifications if the price drops below the desired amount.

## Features

- **Product and Desired Price Input:** Users can input the link to a product and the corresponding desired price.

- **Regular Price Checks:** Data is updated every minute from the product links in the database.

- **Email Notifications:** Users receive email notifications if the product's price drops below the desired amount.
- ![image](https://github.com/LeonDuong24/Check-sale-Ebay/assets/114995131/7b52da2c-3115-4c6f-9da0-de9d81c2c23f)


- **Selenium-based Product Checking:** The application can check products with multiple options using Selenium.

- **Authorization and Pagination:** The website supports user authorization and pagination for an improved user experience.

## Installation Guide

1. **Clone Repository:**
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python app.py
    ```

## Project Structure

- **app.py:** The main file containing Flask application logic.
- **templates/:** The folder containing HTML files.
- **static/:** The folder containing static files such as CSS and JS.
- **database/:** The folder containing the database.

## Future Features

- Extend functionality to support various other shopping websites.
- Improve and customize the user interface.

## Contributions

All contributions are welcome. Please create a pull request if you have suggestions or bug fixes.

## Author

Leon Duong

## License

This project is licensed under the [License Name]. See the LICENSE file for details.
