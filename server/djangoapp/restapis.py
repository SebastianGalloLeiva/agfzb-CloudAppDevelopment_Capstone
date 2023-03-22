import requests
import json
from .models import *
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                    auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey','api_key'))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, payload, **kwargs):
    status_code = None
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    try:
        response = requests.post(url, params=kwargs, json=payload, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey','api_key'))
    except:
        status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result      
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result
        
    
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                
                                short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj




# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    if json_result:
        reviews = json_result["data"]["docs"]
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"],
                                        purchase=review["purchase"], review=review["review"],
                                        sentiment="S")

            if "id" in review:
                review_obj.id = review["id"]
            if "purchase_date" in review:
                review_obj.purchase_date = review["purchase_date"]
            if "car_make" in review:
                review_obj.car_make = review["car_make"]
            if "car_model" in review:
                review_obj.car_model = review["car_model"]
            if "car_year" in review:
                review_obj.car_year = review["car_year"]

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)
            
    return results




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7ca20360-b671-4e70-b4ff-c2511c74514d"
    api_key = "t9qGTy6QFJXQl4KTDdlKxxo4bAqUrJlHO-puYBYWAuNK"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    print(label)
    
    return(label) 
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



