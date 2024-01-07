# Check sale Ebay

## Description

This project is a Flask-based web application that allows users to input a link to a product on eBay along with a desired price. The application monitors the prices of these products over time and sends email notifications if the price drops below the desired amount.

## Features

- **Product and Desired Price Input:** Users can input the link to a product and the corresponding desired price.

- **Regular Price Checks:** Data is updated every minute from the product links in the database.
- **Selenium-based Product Checking:** The application can check products with multiple options using Selenium.
- **Email Notifications:** Users receive email notifications if the product's price drops below the desired amount.
- ![image](https://github.com/LeonDuong24/Check-sale-Ebay/assets/114995131/efbccae3-507c-4e59-959d-dd12fee6366c)

- **Authorization and Pagination:** The website supports user authorization and pagination for an improved user experience.

## Installation Guide

1. **Clone Repository:**
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd main
    ```
2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Edit Env Configuration:**
    Open the folder config and update the MySQL, email services configuration to match your requirements.
4. **Initialize Database Models:**
     ```bash
    cd ..
    cd model
     python models.py
    ```
5. **Run the Application:**
    ```bash
    cd ..
    cd main
    python app.py
    ```

## Project Structure

- **app.py:** The main file containing Flask application logic.
- **main/templates/:** The folder containing HTML files.
- **main/static/:** The folder containing static files such as CSS and JS.
- **model/:** The folder containing the model database.
- **service/:** The folder containing the services.

## Future Features

- Extend functionality to support various other shopping websites.
- Improve and customize the user interface.

## Contributions

All contributions are welcome. Please create a pull request if you have suggestions or bug fixes.

## Author

Leon Duong

## License

This project is licensed under the [License Name]. See the LICENSE file for details.
