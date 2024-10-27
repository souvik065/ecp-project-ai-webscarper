from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from selenium import webdriver
import os

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
# SBR_WEBDRIVER="chromedriver-win64\chromedriver.exe"
print(f"Driver connected to : {SBR_WEBDRIVER}")
def scrape_website(website):
    print("Connecting to Scraping Browser...")
    # Set Chrome options (optional headless mode)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU rendering
    options.add_argument("--no-sandbox")  # Bypass OS security model
    # For Amazon Linux OS | EC2 Instance
    chrome_options.add_argument("--disable-dev-shm-usage")
    '''
    # `chrome_options.add_argument("--disable-dev-shm-usage")`
    This argument disables the use of `/dev/shm`, which is a temporary filesystem (shared memory) used by Linux for inter-process communication.

    # Why Use It?

    Shared Memory Limitations: In a headless environment, particularly on lightweight instances, the shared memory space (/dev/shm) may be limited. If Chrome tries to use more shared memory than is available, it may crash or not function properly.
    Prevent Crashes: By disabling this option, Chrome will not attempt to use shared memory, reducing the risk of running into memory-related errors.
    '''

    chrome_options.binary_location = "/usr/bin/google-chrome"

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    )
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    
     # Set up Chrome WebDriver service
    service = Service(executable_path=SBR_WEBDRIVER)
   # Initialize the WebDriver
    with webdriver.Chrome(service=service, options=options) as driver:
        print(f"Navigating to {website}...")
        driver.get(website)

        # Wait for the page to load
        driver.implicitly_wait(10)

        print("Scraping page content...")
        html = driver.page_source
        return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]