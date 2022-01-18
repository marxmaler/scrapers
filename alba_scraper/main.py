from functions import extract_brand_url, extract_page_data, save_as_csv

urls = extract_brand_url()
jobs = extract_page_data(urls)
save_as_csv(jobs)



