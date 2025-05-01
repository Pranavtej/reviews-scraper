from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app) 

def search_capterra(company_name):
    """Search for a company on Capterra and return search results"""
    import random
    import time
    
    # Try to use fake_useragent for rotating user agents
    try:
        from fake_useragent import UserAgent
        ua = UserAgent()
        user_agent = ua.random
    except:
        # Fallback to a list of common user agents
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
        ]
        user_agent = random.choice(user_agents)
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.capterra.in/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
    }
    
    
    cookies = {
        'visitor_id': f"{random.randint(1000000, 9999999)}",
        'session_visited': 'true',
        'search_term': company_name
    }
    
    search_url = f"https://www.capterra.in/search/?q={company_name}"
    
    try:
       
        session = requests.Session()
        
       
        time.sleep(random.uniform(1, 3))
        
      
        home_response = session.get('https://www.capterra.in/', headers=headers, timeout=30)
        
       
        for cookie in home_response.cookies:
            cookies[cookie.name] = cookie.value
        
      
        time.sleep(random.uniform(2, 4))
        

        headers['Referer'] = 'https://www.capterra.in/'
        
       
        response = session.get(
            search_url, 
            headers=headers,
            cookies=cookies,
            timeout=30
        )
        response.raise_for_status()
        
       
        if 'captcha' in response.text.lower() or 'access denied' in response.text.lower() or 'forbidden' in response.text.lower():
            print("Capterra has detected scraping attempt. Trying alternative approach...")
            return try_alternative_capterra_search(company_name, session, headers)
        
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
      
    
        product_entries = soup.select('a.entry.d-flex.my-4.text-decoration-none')
        
     
        if not product_entries:
            product_entries = soup.select('div.search-result-card') or soup.select('div[data-testid*="product-card"]')
        
        print(f"Found {len(product_entries)} product entries on Capterra")
        
        search_results = []
        for entry in product_entries:
            try:
              
                href = entry.get('href', '') if entry.name == 'a' else None
                
               
                if not href:
                    link_elem = entry.select_one('a[href*="/products/"]') or entry.select_one('a[href*="/software/"]')
                    href = link_elem.get('href', '') if link_elem else ''
                
               
                if not href:
                    continue
                
               
                product_name_elem = entry.select_one('span.h4.fw-bold') or entry.select_one('h2') or entry.select_one('div.fw-bold')
                product_name = product_name_elem.get_text(strip=True) if product_name_elem else "Unknown Product"
                
               
                company_elem = entry.select_one('span.text-body.fw-bold span em') or entry.select_one('span em')
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                
              
                rating_elem = entry.select_one('span.ms-1') or entry.select_one('div[class*="rating"]') or entry.select_one('span:contains("/")')
                rating = rating_elem.get_text(strip=True) if rating_elem else "No Rating"
                
              
                if rating != "No Rating":
                    rating_match = re.search(r'(\d+\.?\d*)', rating)
                    rating = rating_match.group(1) if rating_match else rating
                
               
                reviews_elem = entry.select_one('span.star-rating-component span:nth-of-type(2)') or entry.select_one('span:contains("review")')
                reviews_count = "0"
                if reviews_elem:
                    reviews_text = reviews_elem.get_text(strip=True)
                    
                    reviews_match = re.search(r'(\d+[,\d]*)', reviews_text)
                    reviews_count = reviews_match.group(1).replace(',', '') if reviews_match else "0"
                
            
                desc_elem = entry.select_one('div.search-results__target-description') or entry.select_one('div[class*="description"]')
                description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
                
        
                logo_elem = entry.select_one('img.search-results__thumbnail__img') or entry.select_one('img')
                logo_url = ""
                if logo_elem:
                    if logo_elem.has_attr('data-src'):
                        logo_url = logo_elem['data-src']
                    elif logo_elem.has_attr('src'):
                        logo_url = logo_elem['src']
                
               
                if logo_url and not logo_url.startswith(('http://', 'https://')):
                    logo_url = f"https://www.capterra.in{logo_url}" if logo_url.startswith('/') else f"https://www.capterra.in/{logo_url}"
                
               
                parsed_href = href.split('/')
                
                
                if len(parsed_href) >= 4 and parsed_href[1] == "software":
                    new_reviews_url = f"https://www.capterra.in/reviews/{parsed_href[2]}/{parsed_href[3]}"
                else:
                   
                    new_reviews_url = f"https://www.capterra.in{href}" if href.startswith('/') else href
                
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
                print(f"Processed: {product_name}")
            except Exception as e:
                print(f"Error parsing entry: {e}")
                continue
        
        return search_results
    
    except Exception as e:
        print(f"Error searching Capterra: {e}")
        return []

def try_alternative_capterra_search(company_name, session, headers):
    """Alternative method to search Capterra if the main method fails"""
  
    

    alt_url = f"https://www.capterra.in/directory/{company_name}"
    
    try:
      
        time.sleep(random.uniform(3, 6))
        
       
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        
        response = session.get(alt_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
                

            product_entries = soup.select('div.category-section-card') or soup.select('div[class*="product-card"]')
            
            search_results = []
            for entry in product_entries:
                try:
                 
                    link_elem = entry.select_one('a[href*="/software/"]') or entry.select_one('a[href*="/products/"]')
                    if not link_elem:
                        continue
                        
                    href = link_elem.get('href', '')
                    product_name_elem = link_elem.select_one('h2') or link_elem
                    product_name = product_name_elem.get_text(strip=True) if product_name_elem else "Unknown Product"
                    
                   
                    full_url = f"https://www.capterra.in{href}" if href.startswith('/') else href
                    
                  
                    if "/software/" in full_url:
                      
                        parts = href.split('/')
                        if len(parts) >= 3:
                            product_id = parts[2]
                            product_slug = parts[3] if len(parts) > 3 else ""
                            if product_id.isdigit() and product_slug:
                                full_url = f"https://www.capterra.in/reviews/{product_id}/{product_slug}"
                    
                    result = {
                        'product_name': product_name,
                        'company': "Information not available",
                        'href': href,
                        'full_url': full_url,
                        'rating': "0.0",
                        'reviews_count': "0",
                        'description': "Description not available",
                        'logo_url': ""
                    }
                    
                    search_results.append(result)
                except Exception as e:
                    print(f"Error in alternative parsing: {e}")
                    continue
                    
            return search_results
        else:
            print(f"Alternative search method failed with status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error in alternative search method for Capterra: {e}")
        return []

def search_g2(company_name):
    """Search for a company on G2 and return search results"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.g2.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    search_url = f"https://www.g2.com/search?utf8=%E2%9C%93&button=&query={company_name}"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        product_entries = soup.select('div.product-card')
        
        search_results = []
        for entry in product_entries:
            try:
            
                link_elem = entry.select_one('a.product-card__product-name')
                href = link_elem.get('href', '') if link_elem else ''
                
               
                product_name = link_elem.get_text(strip=True) if link_elem else "Unknown Product"
                
              
                company_elem = entry.select_one('div.product-card__vendor')
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                
             
                rating_elem = entry.select_one('span.product-card__rating')
                rating = rating_elem.get_text(strip=True) if rating_elem else "0.0"
                
                
                reviews_elem = entry.select_one('span.product-card__reviews')
                reviews_count = reviews_elem.get_text(strip=True).replace('reviews', '').strip() if reviews_elem else "0"
                

                desc_elem = entry.select_one('div.product-card__description')
                description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
                
               
                logo_elem = entry.select_one('img.product-card__logo')
                logo_url = logo_elem.get('src') if logo_elem else ""
                
             
                full_url = f"https://www.g2.com{href}/reviews" if href else ""
                
                result = {
                    'product_name': product_name,
                    'company': company,
                    'href': href,
                    'full_url': full_url,
                    'rating': rating,
                    'reviews_count': reviews_count,
                    'description': description,
                    'logo_url': logo_url
                }
                
                search_results.append(result)
            except Exception as e:
                print(f"Error parsing G2 entry: {e}")
                continue
        
        return search_results
    
    except Exception as e:
        print(f"Error searching G2: {e}")
        return []

def scrape_reviews(product_url, start_date=None, end_date=None, source="capterra"):
    """Scrape reviews from a product page on Capterra or G2"""
    import random
    import time
    from fake_useragent import UserAgent
    
    # Create a user agent generator (if not installed, will fall back to a default user agent)
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
        'Referer': 'https://www.capterra.in/search' if source == "capterra" else 'https://www.g2.com/search/products',
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
          
            homepage = 'https://www.capterra.in/' if source == "capterra" else 'https://www.g2.com/'
            session.get(homepage, headers=headers, timeout=30)
            
           
            time.sleep(random.uniform(1, 2))
            
         
            response = session.get(product_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
         
            if 'captcha' in response.text.lower() or 'access denied' in response.text.lower() or 'forbidden' in response.text.lower():
                print(f"Detected access restriction (attempt {retry_count + 1}/{max_retries})")
                retry_count += 1
                time.sleep(random.uniform(5, 10))  # Longer wait before retry
                continue
            

            if source == "capterra":
                reviews = scrape_capterra_reviews(soup, start_date, end_date)
            else:  
                reviews = scrape_g2_reviews(soup, start_date, end_date)
            
            
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

def scrape_capterra_reviews(soup, start_date=None, end_date=None):
    """Extract reviews from Capterra HTML"""
    reviews = []
    

    review_cards = soup.select('div.i18n-translation_container.review-card')
    
   
    if not review_cards:
        review_cards = soup.select('div[data-translation-id].pt-4')
    

    # if not review_cards:
    #     with open('capterra_response.html', 'w', encoding='utf-8') as f:
    #         f.write(str(soup))
    

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    for card in review_cards:
        try:
           
            date_elem = card.select_one('div.text-ash.mb-3 span.ms-2')
            if not date_elem:
                date_elem = card.select_one('span.ms-2')  # Simplified selector
            
            review_date_str = date_elem.get_text(strip=True) if date_elem else ""
            
          
            if (start_date_obj or end_date_obj) and not review_date_str:
                continue
                
           
            review_date_obj = None
            
           
            try:
                review_date_obj = datetime.strptime(review_date_str, "%b %d, %Y")
            except ValueError:
              
                if "days ago" in review_date_str:
                    days = int(review_date_str.split()[0])
           
                    review_date_obj = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                  
                elif "months ago" in review_date_str:
                    months = int(review_date_str.split()[0])
                 
                    review_date_obj = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                elif "years ago" in review_date_str:
                    years = int(review_date_str.split()[0])
                
                    review_date_obj = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            
       
            if review_date_obj:
                if start_date_obj and review_date_obj < start_date_obj:
                    continue  
                if end_date_obj and review_date_obj > end_date_obj:
                    continue 
            
         
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
                review_title_elem = card.select_one('div.fw-bold')  # Alternative selector
            review_title = review_title_elem.get_text(strip=True) if review_title_elem else ""
            
       
            rating_text_elem = card.select_one('span.ms-1')
            if not rating_text_elem:
                rating_text_elem = card.select_one('div.star-rating-component')
            rating = rating_text_elem.get_text(strip=True) if rating_text_elem else "0.0"
            

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
                'date': review_date_str,
                'pros': pros,
                'cons': cons,
                'review_id': review_id,
                'source': 'capterra'
            }
            
            reviews.append(review)
        except Exception as e:
            print(f"Error parsing review card: {e}")
            continue
            
    return reviews

def scrape_g2_reviews(soup, start_date=None, end_date=None):
    """Extract reviews from G2 HTML"""
    reviews = []
    

    review_cards = soup.select('div.paper.paper--box.mb-2')
    

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    for card in review_cards:
        try:

            date_elem = card.select_one('span.font-weight-light')
            review_date_str = date_elem.get_text(strip=True) if date_elem else ""
            

            if (start_date_obj or end_date_obj) and not review_date_str:
                continue
                
       
            review_date_obj = None
            
           
            try:
                review_date_obj = datetime.strptime(review_date_str, "%B %d, %Y")
            except ValueError:
                try:
                    review_date_obj = datetime.strptime(review_date_str, "%b %d, %Y")
                except ValueError:
                  
                    pass
            
        
            if review_date_obj:
                if start_date_obj and review_date_obj < start_date_obj:
                    continue 
                if end_date_obj and review_date_obj > end_date_obj:
                    continue 
            
          
            reviewer_elem = card.select_one('div.mb-1.font-weight-bolder')
            reviewer_name = reviewer_elem.get_text(strip=True) if reviewer_elem else "Anonymous"
            
          
            company_elem = card.select_one('div.pre-wrap.v-line-clamp-2')
            company_info = company_elem.get_text(strip=True) if company_elem else ""
            
         
            rating_elem = card.select_one('span.fw-semibold')
            rating = rating_elem.get_text(strip=True) if rating_elem else "0.0"
            
          
            title_elem = card.select_one('h3.review__title')
            review_title = title_elem.get_text(strip=True) if title_elem else ""
            
          
            pros = ""
            cons = ""
            
            pros_section = card.select_one('div.mb-2:has(h5:-soup-contains("What do you like best"))')
            if pros_section:
                pros_text = pros_section.select_one('div.pre-wrap')
                pros = pros_text.get_text(strip=True) if pros_text else ""
            
            cons_section = card.select_one('div.mb-2:has(h5:-soup-contains("What do you dislike"))')
            if cons_section:
                cons_text = cons_section.select_one('div.pre-wrap')
                cons = cons_text.get_text(strip=True) if cons_text else ""
            
          
            review = {
                'reviewer_name': reviewer_name,
                'reviewer_info': "",
                'linkedin_verified': "Unknown", 
                'company_info': company_info,
                'usage_duration': "", 
                'review_title': review_title,
                'rating': rating,
                'date': review_date_str,
                'pros': pros,
                'cons': cons,
                'review_id': "", 
                'source': 'g2'
            }
            
            reviews.append(review)
        except Exception as e:
            print(f"Error parsing G2 review card: {e}")
            continue
            
    return reviews

@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    company_name = request.args.get('company_name')
    source = request.args.get('source', 'capterra').lower() 
    
    if not company_name:
        return jsonify({
            "error": "Missing company_name parameter"
        }), 400
    
  
    if source == 'g2':
        search_results = search_g2(company_name)
    else:
        search_results = search_capterra(company_name)
    
    return jsonify(search_results)

@app.route('/get_product_reviews', methods=['GET'])
def get_product_reviews():
    product_url = request.args.get('product_url')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    source = request.args.get('source', 'capterra').lower()
    
    if not product_url:
        return jsonify({
            "error": "Missing product_url parameter"
        }), 400
    
 
    reviews = scrape_reviews(product_url, start_date, end_date, source)
    
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3200)