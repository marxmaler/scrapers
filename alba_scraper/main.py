from functions import extract_brand_url, extract_page_data, save_as_csv

urls, companies = extract_brand_url()
jobs_list = extract_page_data(urls)
save_as_csv(jobs_list, companies)
