import os
import argparse
import re
import time
from pathlib import Path
from google import genai as GeminiAI
from datetime import datetime

# --------------------------- #
# ARGUMENT PARSING FUNCTION   #
# --------------------------- #
def parser():
    """
    Parse command-line arguments to get the path to the text file containing companies per country.
    Returns the absolute file path if valid, else None.
    """
    parser = argparse.ArgumentParser(
        description="CAI.py - Company AI Infosearcher.",
        usage="python3 CAI.py --file [your_text_file.txt]"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=False,
        help="Specify the text file to process."
    )
    args = parser.parse_args()

    # If no arguments provided, show help and exit
    if not args.file:
        parser.print_help()
        return None
        
    # Convert file path to absolute path
    abs_path = os.path.abspath(args.file)

    # Verify the file exists
    if not os.path.isfile(abs_path):
        print(f"❌ File not found: {abs_path}")
        return None
    else:
        print(f"✅ File found: {abs_path}")
        return abs_path

# --------------------------- #
# LOAD GOOGLE GEMINI API KEY  #
# --------------------------- #
def load_api():
    """
    Loads the Google Gemini API key from a .env file.
    Creates .env with instructions if it doesn't exist.
    Returns the API key if found, else None.
    """
    env_file = ".env"

    # Check if .env exists, create if not
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("# Add your Google Gemini API key below:\n# GEMINI_API_KEY=your_api_key_here\n")
        print("'.env' file created! Please add your Google Gemini API key and re-run the script.")
        return None

    # Read and validate API key from .env
    with open(env_file, "r") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                gemini_api = line.strip().split("=", 1)[1]
                if gemini_api:
                    print("✅ API key loaded successfully.")
                    return gemini_api
                else:
                    print("⚠️ API key is empty. Please fill it in '.env' and re-run.")
                    return None

    print("⚠️ No valid 'GEMINI_API_KEY' entry found in '.env'. Please add it and re-run.")
    return None

# --------------------------- #
# LOAD TEXT FILE AND PARSE    #
# --------------------------- #
def load_textfile(file_path):
    """
    Loads the text file containing countries and companies.
    
    Expected format:
        Country Name:
        1- Company One
        2- Company Two
        ...
    
    Returns:
        - countries: list of country names
        - companies_lists: list of lists containing companies per country
    """
    countries = []
    companies_lists = []
    current_country = None
    current_companies = []

    with open(file_path, "r") as f:
        print("✅ Text file loaded successfully.")

        for line in f:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue

            # Detect country header (ends with ":")
            if line.endswith(":"):
                # Save previous country's companies if they exist
                if current_country:
                    countries.append(current_country)
                    companies_lists.append(current_companies)

                # Start new country
                current_country = line[:-1].strip()
                current_companies = []
                
            elif current_country:
                # Extract all companies from the line (supports multiple companies per line)
                # Pattern: "1- CompanyName" or "2- CompanyName"
                matches = re.findall(r'\d+\-\s*([^\d]+?)(?=\s*\d+\-|$)', line)
                for company_name in matches:
                    company_name = company_name.strip()
                    if company_name:
                        current_companies.append(company_name)

    # Add the last country after the loop ends
    if current_country:
        countries.append(current_country)
        companies_lists.append(current_companies)

    return countries, companies_lists

# --------------------------- #
# SEQUENTIAL API CALL         #
# --------------------------- #
def call_gemini_api_sequential(gemini_api, countries, companies_lists, output_file="gemini_log.txt"):
    """
    Calls Google Gemini API sequentially for all companies.
    
    Features:
    - Processes one company at a time
    - Small delay between requests for stability
    - Proper rate limit handling (waits 1 minute after every 15 requests)
    - Retry mechanism with exponential backoff for failed requests
    - Saves results to file with country headers
    - Tracks and logs execution time
    
    Args:
        gemini_api: API key for Google Gemini
        countries: List of country names
        companies_lists: List of company lists per country
        output_file: Output file name (default: gemini_log.txt)
    """

    client = GeminiAI.Client(api_key=gemini_api)

    # Flatten all companies with their country info for easier processing
    tasks = []
    idx_counter = 1
    for country_index, country in enumerate(countries):
        companies = companies_lists[country_index]
        for company in companies:
            tasks.append({
                "index": idx_counter,
                "country": country,
                "company": company
            })
            idx_counter += 1

    total_companies = len(tasks)
    request_count = 0
    sleep_after = 15  # Wait after this many requests
    sleep_time = 60   # Wait duration in seconds (1 minute)
    request_delay = 1  # Small delay between each request (seconds)
    model = "gemini-2.5-flash-lite"
    
    # Calculate estimated time (including the small delays)
    request_time = 1.5  # Average seconds per request
    batches = total_companies // sleep_after
    remaining = total_companies % sleep_after
    eta_seconds = (batches * (sleep_after * (request_time + request_delay) + sleep_time)) + (remaining * (request_time + request_delay))
    eta_minutes, eta_seconds_only = divmod(eta_seconds, 60)
    print(f"⏱ Estimated total time: {eta_minutes} min {eta_seconds_only} sec")

    # Store results in order
    results = []

    # Process each company sequentially
    for task in tasks:
        print(f"Processing {task['country']}: Company {task['index']}/{total_companies} - {task['company']}")
        
        # Retry mechanism with exponential backoff
        max_retries = 3
        backoff = 5  # Initial backoff in seconds
        result_text = None
        
        for attempt in range(max_retries):
            try:
                # Make API request
                response = client.models.generate_content(
                    model=model,
                    contents=(
                        f"Provide a concise, 200-character description of {task['company']} in {task['country']}. "
                        'Include all relevant industry categories based on the company\'s activities. '
                        'Always use the latest information from reputable web sources. '
                        'The output must be exactly in this format, with nothing extra, no explanations, no greetings, no filler:\n\n'
                        '"200-character description" | [Relevant categories]'
                    )
                )
                result_text = response.text.strip()
                break  # Success, exit retry loop
                
            except Exception as e:
                # Handle rate limit errors (429)
                if "429" in str(e):
                    print(f"⚠️ 429 Too Many Requests for {task['company']}, retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2  # Exponential backoff
                else:
                    # Other errors
                    result_text = f"ERROR: {e}"
                    break
        
        # If all retries failed
        if result_text is None:
            result_text = f"ERROR: Too many retries for {task['company']}"
        
        # Save result
        results.append({
            "country": task['country'],
            "company": task['company'],
            "text": result_text
        })
        
        request_count += 1
        
        # Rate limit check: Wait 1 minute after every 15 requests
        if request_count % sleep_after == 0 and request_count < total_companies:
            print(f"⏱ {request_count} requests completed. Waiting 1 minute for rate limit...")
            time.sleep(sleep_time)
        else:
            # Small delay between requests (for stability and avoiding rate limits)
            time.sleep(request_delay)

    # End timer and calculate duration
    end_time = time.time()
    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration_seconds = end_time - start_time
    duration_minutes = int(duration_seconds // 60)
    duration_seconds_only = duration_seconds % 60

    # Write results to output file
    output_path = Path(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        # Write execution metadata at the top
        f.write("=" * 60 + "\n")
        f.write("EXECUTION SUMMARY\n")
        f.write("=" * 60 + "\n")
        f.write(f"Start Time: {start_datetime}\n")
        f.write(f"End Time: {end_datetime}\n")
        f.write(f"Total Duration: {duration_minutes} min {duration_seconds_only:.2f} sec\n")
        f.write(f"Total Companies Processed: {total_companies}\n")
        f.write(f"Model Used: {model}\n")
        f.write("=" * 60 + "\n\n")
        
        # Write company results
        current_country = None
        for idx, res in enumerate(results, start=1):
            # Add country header when country changes
            if res['country'] != current_country:
                current_country = res['country']
                f.write(f"\n=== {current_country} ===\n\n")
            
            # Write company result
            f.write(f"{idx}- {res['company']} - {res['text']}\n\n")

    print(f"✅ All responses saved to {output_file}")
    print(f"⏱ Total execution time: {duration_minutes} min {duration_seconds_only:.2f} sec")

# --------------------------- #
# MAIN EXECUTION              #
# --------------------------- #
def main():
    """
    Main execution function:
    1. Parse command-line arguments
    2. Load text file with countries and companies
    3. Load API key from .env
    4. Call Gemini API sequentially for all companies
    """
    # Parse arguments and get file path
    file_path = parser()
    if not file_path:
        return
    
    # Load countries and companies from file
    countries, companies = load_textfile(file_path)
    
    # Load API key
    api_key = load_api()
    if not api_key:
        return
    
    # Process all companies sequentially
    call_gemini_api_sequential(api_key, countries, companies)

# Start timer
start_time = time.time()
start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Run the script
main()
