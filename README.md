
# Shuvter

Commerce is an e-commerce platform for cars, built using Django. It provides a seamless and user-friendly interface for users to browse, search, and purchase cars online. This project demonstrates the use of Django for building scalable and efficient web applications with features tailored for the automotive market.


## Installation

Install my-project from below listed process.
Go to your terminal and use the below mentioned codes

```bash
  git clone https://github.com/shuvaaashish/commerce.git
  pip install django 
  cd commerce
  Python manage.py runserver 
  Then Visit http://127.0.0.1:8000/
```
Running the above codes might do the job coviniently.
If you want fresh database then use
```bash
rm db.sqlite3
python manage.py migrate
```
    
## Technology Stack
- Backend:Django
- Fronted:HTML,CSS,JavaScript
- Database:Sqlite3
- Others:Bootstrap

## Features

- Car Listings: Display cars with detailed specifications, images, and prices.
- User Authentication: Secure login and registration for buyers and sellers.
- Categories: Browse cars by selecting categories from the "Categories" link, making it easier to find specific types of cars.
- Bid on Cars: Users can bid on cars, but cannot place a bid lower than the current bid.
- Watchlist: Users can add cars to their watchlist and view them later. Cars can be removed from the watchlist as well.
- Admin Management: Django admin panel for managing users, listings, and transactions.
- Comments on Cars: Users can comment on cars that are listed for sale to engage with the sellers or other buyers.
- Auction Status: Once a car is sold, the winning bidder will see a congratulatory message when visiting the car's page, while losing bidders will be informed that the auction has been closed.



## Acknowledgements

 - [Brian Yu](https://github.com/brianyu28)
 


## Authors

- [@Shuva_Aashsih9](https://www.github.com/shuvaaasish)

