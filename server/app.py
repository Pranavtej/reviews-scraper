from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import json
import re

app = Flask(__name__)
CORS(app)

def search_capterra(company_name):
    """Search for a company on Capterra and return search results"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.capterra.in/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }
    
    search_url = f"https://www.capterra.in/search/?q={company_name}"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=30)
        response.raise_for_status()  
        
      
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        product_entries = soup.select('a.entry.d-flex.my-4.text-decoration-none')
        
        search_results = []
        for entry in product_entries:
            try:
              
                href = entry.get('href', '')
                
             
                product_name_elem = entry.select_one('span.h4.fw-bold')
                product_name = product_name_elem.get_text(strip=True) if product_name_elem else "Unknown Product"
                
               
                company_elem = entry.select_one('span.text-body.fw-bold span em')
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                
                
                rating_elem = entry.select_one('span.ms-1')
                rating = rating_elem.get_text(strip=True) if rating_elem else "No Rating"
                
              
                reviews_elem = entry.select_one('span.star-rating-component span:nth-of-type(2)')
                reviews_count = reviews_elem.get_text(strip=True).strip('()') if reviews_elem else "0"
                
              
                desc_elem = entry.select_one('div.search-results__target-description')
                description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
                
                
                logo_elem = entry.select_one('img.search-results__thumbnail__img')
                logo_url = logo_elem.get('src') if logo_elem else ""
                
             
                parsed_href = href.split('/')
                
                new_reviews_url = f"https://www.capterra.in/reviews/{parsed_href[2]}/{parsed_href[3]}"
                result = {
                    'product_name': product_name,
                    'company': company,
                    'href': href,
                    'full_url': new_reviews_url,
                    'rating': rating,
                    'reviews_count': reviews_count,
                    'description': description,
                    'logo_url': logo_url
                }
                
                search_results.append(result)
            except Exception as e:
                print(f"Error parsing entry: {e}")
                continue
        
        return search_results
    
    except Exception as e:
        print(f"Error searching Capterra: {e}")
        return []

def scrape_reviews(product_url):
    """Scrape reviews from a product page on Capterra"""
    import random
    import time
    from fake_useragent import UserAgent
    
   
    try:
        ua = UserAgent()
        user_agent = ua.random
    except:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.capterra.in/search',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
    }
    
    reviews = []
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
          
            time.sleep(random.uniform(1, 3))
            
            session = requests.Session()
           
            session.get('https://www.capterra.in/', headers=headers, timeout=30)
            
            
            time.sleep(random.uniform(1, 2))
            
          
            response = session.get(product_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
           
            if 'captcha' in response.text.lower() or 'access denied' in response.text.lower() or 'forbidden' in response.text.lower():
                print(f"Detected access restriction (attempt {retry_count + 1}/{max_retries})")
                retry_count += 1
                time.sleep(random.uniform(5, 10)) 
                continue
            
           
            review_cards = soup.select('div.i18n-translation_container.review-card')
            
         
            if not review_cards:
                review_cards = soup.select('div[data-translation-id].pt-4')
            
         
            if not review_cards:
                print(f"No review cards found. HTML structure might have changed.")
                with open('capterra_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Response HTML saved to capterra_response.html for inspection")
            
            for card in review_cards:
                try:
                
                    reviewer_name_elem = card.select_one('div.h5.fw-bold')
                    reviewer_name = reviewer_name_elem.get_text(strip=True) if reviewer_name_elem else "Anonymous"
                    
                  
                    linkedin_elem = card.select_one('div.text-ash svg.icon-linkedin-square')
                    is_linkedin_verified = "Yes" if linkedin_elem else "No"
                    
                  
                    reviewer_desc_elem = card.select_one('div.text-ash')
                    reviewer_info = reviewer_desc_elem.get_text(strip=True) if reviewer_desc_elem else ""
                    
      
                    company_info_elems = card.select('div.col-12.col-md-6.col-lg-12.pt-3.pt-md-0.pt-lg-3.text-ash div.mb-2')
                    company_info = company_info_elems[0].get_text(strip=True) if company_info_elems and len(company_info_elems) > 0 else ""
                    
                   
                    usage_info = company_info_elems[1].get_text(strip=True) if company_info_elems and len(company_info_elems) > 1 else ""
                    
                    
                    review_title_elem = card.select_one('h3.h5.fw-bold')
                    if not review_title_elem:
                        review_title_elem = card.select_one('div.fw-bold')  
                    review_title = review_title_elem.get_text(strip=True) if review_title_elem else ""
                    
                 
                    rating_text_elem = card.select_one('span.ms-1')
                    if not rating_text_elem:
                        rating_text_elem = card.select_one('div.star-rating-component')
                    rating = rating_text_elem.get_text(strip=True) if rating_text_elem else "0.0"
                    

                    date_elem = card.select_one('div.text-ash.mb-3 span.ms-2')
                    if not date_elem:
                        date_elem = card.select_one('span.ms-2')
                    date = date_elem.get_text(strip=True) if date_elem else ""
                    
   
                    pros_section = card.select_one('div:has(h3:-soup-contains("Pros"))') or card.select_one('div:has(strong:-soup-contains("Pros"))')
                    pros = ""
                    if pros_section:
                        pros_elem = pros_section.find('p')
                        pros = pros_elem.get_text(strip=True) if pros_elem else ""
                    else:
                      
                        pros_elem = card.select('p')[1] if len(card.select('p')) > 1 else None
                        pros = pros_elem.get_text(strip=True) if pros_elem else ""
                    
                  
                    cons_section = card.select_one('div:has(h3:-soup-contains("Cons"))') or card.select_one('div:has(strong:-soup-contains("Cons"))')
                    cons = ""
                    if cons_section:
                        cons_elem = cons_section.find('p')
                        cons = cons_elem.get_text(strip=True) if cons_elem else ""
                    else:
                       
                        cons_elem = card.select('p')[3] if len(card.select('p')) > 3 else None
                        cons = cons_elem.get_text(strip=True) if cons_elem else ""
                    
                   
                    review_id = card.get('data-translation-id', '')
                    
                   
                    review = {
                        'reviewer_name': reviewer_name,
                        'reviewer_info': reviewer_info,
                        'linkedin_verified': is_linkedin_verified,
                        'company_info': company_info,
                        'usage_duration': usage_info,
                        'review_title': review_title,
                        'rating': rating,
                        'date': date,
                        'pros': pros,
                        'cons': cons,
                        'review_id': review_id
                    }
                    
                    reviews.append(review)
                except Exception as e:
                    print(f"Error parsing review card: {e}")
                    continue
            
            break
        
        except requests.exceptions.HTTPError as e:
            retry_count += 1
            print(f"HTTP Error: {e} (attempt {retry_count}/{max_retries})")
            if retry_count < max_retries:
                time.sleep(random.uniform(5, 15))
            else:
                print(f"Failed to scrape reviews after {max_retries} attempts")
                return []
        except Exception as e:
            print(f"Error scraping reviews: {e}")
            return []
    
    return reviews

@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    company_name = request.args.get('company_name')
    
    if not company_name:
        return jsonify({
            "error": "Missing company_name parameter"
        }), 400
    
  
    search_results = search_capterra(company_name)
    
    return jsonify(search_results)

@app.route('/get_product_reviews', methods=['GET'])
def get_product_reviews():
    product_url = request.args.get('product_url')
    
    if not product_url:
        return jsonify({
            "error": "Missing product_url parameter"
        }), 400
    
   
    reviews = scrape_reviews(product_url)
    
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3200)