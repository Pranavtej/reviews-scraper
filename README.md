# Reviews Scraper

A web application that scrapes product reviews from Capterra and G2, allowing users to search for specific companies and filter reviews by date range.

## Features

- Search for products from multiple sources (Capterra and G2)
- Filter reviews by date range
- View detailed product information, including ratings and reviews
- Paginated review display with tabular format
- Anti-blocking techniques to ensure reliable scraping

## Getting Started

### Prerequisites

1. Python 3.7+ installed
2. Node.js 18+ installed
3. npm or yarn package manager

### Installation

#### Backend Setup

1. Navigate to the server directory:

```bash
cd server
```

2. Create a Python virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required Python packages:

```bash
pip install flask flask-cors beautifulsoup4 requests fake-useragent
```

4. Start the Flask server:

```bash
python app.py
```

The backend server will start running on http://127.0.0.1:3200

#### Frontend Setup

1. Install the required Node.js packages:

```bash
npm install
# or
yarn install
```

2. Run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Usage

1. Enter a company name in the search field (e.g., "Microsoft", "Slack", "Zoom")
2. Select a source (Capterra or G2)
3. Optionally, set a date range to filter reviews
4. Click the "Search" button
5. From the search results, click "View Reviews" on any product to see its reviews

## Sample JSON Output

### Search Results JSON:

```json
[
  {
    "product_name": "Microsoft Teams",
    "company": "Microsoft",
    "href": "/software/125691/microsoft-teams",
    "full_url": "https://www.capterra.in/reviews/125691/microsoft-teams",
    "rating": "4.4",
    "reviews_count": "15987",
    "description": "Microsoft Teams is a collaboration platform that combines workplace chat, video meetings, file storage, and application integration.",
    "logo_url": "https://www.capterra.in/images/logos/microsoft-teams.svg"
  },
  {
    "product_name": "Microsoft 365",
    "company": "Microsoft",
    "href": "/software/7901/microsoft-365",
    "full_url": "https://www.capterra.in/reviews/7901/microsoft-365",
    "rating": "4.6",
    "reviews_count": "7458",
    "description": "Microsoft 365 is a cloud-based subscription service that brings together premium Office apps with advanced security and device management.",
    "logo_url": "https://www.capterra.in/images/logos/microsoft-365.png"
  }
]
```

### Product Reviews JSON:

```json
[
  {
    "reviewer_name": "John D.",
    "reviewer_info": "Verified LinkedIn User",
    "linkedin_verified": "Yes",
    "company_info": "Information Technology, 51-200 Employees",
    "usage_duration": "1-2 years",
    "review_title": "Great Collaboration Tool",
    "rating": "4.5",
    "date": "Apr 15, 2025",
    "pros": "Easy integration with other Microsoft products. Good video quality for meetings. Chat feature is intuitive and easy to use.",
    "cons": "Can be resource-intensive. Occasional lag during large meetings. Mobile app could be improved.",
    "review_id": "review-125691-58794",
    "source": "capterra"
  },
  {
    "reviewer_name": "Sarah M.",
    "reviewer_info": "",
    "linkedin_verified": "No",
    "company_info": "Healthcare, 1000+ Employees",
    "usage_duration": "2+ years",
    "review_title": "Reliable for Enterprise Use",
    "rating": "4.0",
    "date": "Mar 28, 2025",
    "pros": "Reliable platform for enterprise communications. File sharing and collaboration is seamless. Good admin controls.",
    "cons": "Interface can be cluttered. Some features are hard to find. Performance issues on older devices.",
    "review_id": "review-125691-58723",
    "source": "capterra"
  }
]
```

## Architecture

The application consists of two main components:

1. **Backend (Flask API)**
   - Handles scraping of search results and reviews from Capterra and G2
   - Implements anti-blocking techniques to ensure reliable data retrieval
   - Exposes endpoints for searching and retrieving reviews

2. **Frontend (Next.js)**
   - Provides a user-friendly interface for searching and viewing reviews
   - Implements responsive design for various device sizes
   - Includes pagination and filtering capabilities

## API Endpoints

- **GET /get_reviews**
  - Parameters:
    - `company_name` (required): Name of the company to search for
    - `source` (optional): Source to search on (`capterra` or `g2`, defaults to `capterra`)
  - Returns: Array of product search results

- **GET /get_product_reviews**
  - Parameters:
    - `product_url` (required): URL of the product reviews page
    - `source` (optional): Source of the reviews (`capterra` or `g2`)
    - `start_date` (optional): Start date filter in YYYY-MM-DD format
    - `end_date` (optional): End date filter in YYYY-MM-DD format
  - Returns: Array of product reviews

## Troubleshooting

- If you encounter 403 Forbidden errors, the application will attempt alternative methods to retrieve data. If issues persist, you may need to:
  1. Wait a few minutes before trying again
  2. Use a VPN or change your network
  3. Check if the review site has changed their HTML structure

- The application saves HTML responses to files for debugging purposes:
  - `capterra_response.html`
  - `g2_response.html`
  - `capterra_alternative_response.html`
  - `g2_alternative_response.html`

## License

This project is open source and available under the MIT License.

## Acknowledgements

- [Next.js](https://nextjs.org) - Frontend framework
- [Flask](https://flask.palletsprojects.com) - Backend framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Fake UserAgent](https://github.com/hellysmile/fake-useragent) - User-Agent rotation
