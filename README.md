# Accept payments with Stripe Checkout
## Check out session with one time payment

### Tasks yet to do
[x] Integrate PostgreSQL  
[ ] Update Database with the trasaction happening in Stripe
### Client directory
The client director contains some sample for the front-end part in `html`.The cancel, success and the index pages. 

### Server directory
The server directory contains APIs for making payments. The client will make requests to the server with the ids, and quantities of each items.  
The details of the products are to be stored in the server or a Database in the server, to prevent any malicious attempts from the client side.    

## Requirements

- Python 3 or Conda environments
- Configured .env file

  
## How to run
1. Clone the branch and change directory in the server folder:
```bash
cd checkout-one-time-payments/server/
```

2. Create a new conda environment:
```bash
conda create -n payment python=3.9.0
conda activate payment
```  
   
3. Install the dependencies in the environment:
```bash
pip install -r requirements.txt 
```  
4. Rename and move the .env.example file into a file named .env 
```bash
cp .env.example .env
```
Now provide the your Stripe keys from your developer dashboard.   
You will need a Stripe account in order to run the demo. Once you set up your account, go to the [Stripe developer](https://stripe.com/docs/development#api-keys) dashboard to find your API keys.

The other environment variables are configurable:

`STATIC_DIR` : tells the server where to the client files are located and does not need to be modified unless you move the server files.

`DOMAIN` : is the domain of your website, where Checkout will redirect back to after the customer completes the payment on the Checkout page.
6. Run the file `app.py`:
```bash
uvicorn app:app
```
Then go to `localhost:8000/docs`. Here you can add products, in the `add_products` endpoint.   
![Endpoints](https://i.imgur.com/wISFkfc.png)


5. Now run the server:
```bash 
uvicorn server:app --port 8000
```

Send request to the server through Postman, on the URL `localhost:5000/create-checkout-session`, make a `POST` request with the format:
```python
[
  {
    "product_id" : 2,
    "quantity":3
  },
  {
    "product_id" : 3,
    "quantity":2
  }
]
```
You will get a response back with the status, URL along with the details of the transaction session.    
Follow the link and it will lead you to the pre-built checkout page.   
![Checkout Page](https://i.imgur.com/APk5KhJ.png)

