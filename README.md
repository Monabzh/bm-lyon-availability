# BM Lyon Availability Checker
This project was made to add missing features to the *OPAC* (Online Public Access Catalog) of the public library of Lyon.
> https://catalogue.bm-lyon.fr/accueil

## How it works
> Instead of searching the availability of every books **one by one** of your TBR (To Be Read) shelf, just check which one is available in an instant !

![alt text](image/Image%20collée.png)

Given a list of books made with your library account, you can check in which library they are available.

Further features coming soon...

## Requirements

## Setup

### 1. Clone the repository
In your bash, clone the repository :
`git clone https://github.com/Monabzh/bm-lyon-availability.git`

Then go the created files : `cd bm-lyon-availability`
### 2. Install dependencies
Create a virtual environnement `python -m venv venv`

Activate it : `source venv/bin/activate`

Install the requirements : `pip install -r requirements.txt`
### 3. Configure your credentials (.env)
You need to create a *.env* file (with `touch .env` for exemple) and complete the following values named with the given key name :

**Your account information :**

    BM_ID = [number of your account ID]
    BM_PSW = [password of your account]

**Your TBR list :**

    BM_TBR_ID = [ID of your reading-shelf list]

This is the blocks of letters and numbers in the URL of your list after /my/list/.

For exemple my TBR ID is **a53ec95e-b0c7-4529-86c0-e9a346698b8b** because when I go to my list on my account the URL is https://catalogue.bm-lyon.fr/my/list/a53ec95e-b0c7-4529-86c0-e9a346698b8b

**Localisation of Firefox in your computer :**
*Selenium* (more after) is used and need to access to Firefox :

    LOC_FIREFOX = "your/path/to/firefox"

To find your Firefox binary, in your terminal :

`which firefox` shows the path but might be a shell wrapper (was my case using Ubuntu with Snap)

`file $(which firefox)` (to check if this is a binary or shell wrapper)

`find / -name "firefox-bin" 2>/dev/null` if 'which firefox' returns a shell wrapper this command finds the real binary

## Usage



## Technical notes
### Why Selenium?
To access the Data, we needed multiple authentication header (API-key), and especially *X-InMedia-Authorization: Bearer <...>*.

The X-InMedia Authorization header has 3 parts : `Bearer <auth_token> <api_token> <hash>`

The website is a React app - content is generated at runtime by JavaScript, not served as plain HTML. This means `api_token` (from window.mobileSettings) and session cookies are only accessible from inside a real browser. Selenium drives a real Firefox instance to retrieve them.


### API reverse engineering
I struggled finding documentation on the API used. I had to search through the DevTools > Network of different pages to understand the structure of the pipelines.

The base URL is `https://catalogue.bm-lyon.fr/in/rest/api`

**The endpoints :**
- `POST /authenticate` login
- `POST /FetchBasket` reading list
- `GET /notice?aspect=Stock` availability of books
- `GET /notice?aspect=Meta` meta of books

**The authentication mechanism :**
- The X-InMedia-Authorization header is required on every request
- Its format is `Bearer null <api_token> <hash>`
- The api_token lives in `window.mobileSettings.apiToken` in the browser
- The hash is computed from the URL parameters using a specific algorithm

**The data structure :**
- Books are identified by p::usmarcdef_XXXXXXXXXX
- Availability is in monographicCopies > children > data > stat_desc
- "On Shelf" means available
- branch_desc gives the library name

**Where things are stored :**
- Session is maintained via JSESSIONID cookie
- Book titles are in the title attribute of DOM elements
- Book IDs are embedded in cover image URLs

### The hash function
A hash function is needed for the third element of the X-InMedia-Authorization header : it's a basic security measure from the server. This function that takes a URL string and computes a number from it.

I didn't figure it by myself — I found a Firefox extension on GitHub (bm-lyon-favorites) that had already reverse engineered it. The algorithm was in the popup.js file.

### Credits
- GitHub repository **[bm-lyon-favorites](https://github.com/ncherel/bm-lyon-favorites)**