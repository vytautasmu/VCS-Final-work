from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains




def get_jobs(keyword, num_jobs, verbose):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver_path = "chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_window_size(1120, 1000)
    actions = ActionChains(driver)

    url = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=" + keyword + "&clickSource=searchBox&locId=1&locT=N&locName=United%20States"
    #url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
    
        

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(5)

        #test for the "Sign Up" prompt and get rid of it.
        # try:
        #     driver.find_element_by_class_name("selected").click()
        #     print(' x out worked')
        # except ElementClickInterceptedException:
        #     print(' x out failed')
        #     pass

        # time.sleep(.1)
        # try:
        #     driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/span/svg').click() #clicking to the X.
        #     print(' x out worked')
        # except NoSuchElementException:
        #     print(' x out failed')
        #     pass

        #Going through each job in this page
        job_buttons = driver.find_elements_by_css_selector("li.react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        #job_buttons = driver.find_elements_by_css_selector("job-search-key-kgm6qi")
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            if len(jobs) % 150 == 0:
                tmp_df = pd.DataFrame(jobs)
                tmp_df.to_csv(f'engineer_jobs-{len(jobs)}.csv')
            
            # if len(jobs) == 500:
            #     tmp_df = pd.DataFrame(jobs)
            #     tmp_df.to_csv(f'jobs-{len(jobs)}.csv')
            
            # if len(jobs) == 800:
            #     tmp_df = pd.DataFrame(jobs)
            #     tmp_df.to_csv(f'jobs-{len(jobs)}.csv')

            if job_button == job_buttons[4]:
                actions.move_to_element(job_buttons[9]).perform()
            if job_button == job_buttons[9]:
                actions.move_to_element(job_buttons[14]).perform()
            if job_button == job_buttons[14]:
                actions.move_to_element(job_buttons[19]).perform()
            if job_button == job_buttons[19]:
                actions.move_to_element(job_buttons[24]).perform()
            if job_button == job_buttons[24]:
                actions.move_to_element(job_buttons[29]).perform()
            job_button.click()  #You might 
            time.sleep(3)

            if job_button == job_buttons[0]:
                try:
                    driver.find_element_by_css_selector('[alt="Close"]').click() #clicking to the X.
                except NoSuchElementException:
                    pass

            collected_successfully = False
            
            while not collected_successfully:
                try:
                    time.sleep(3)
                    #company_name = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[24]/div[2]/div[1]/a/span').text
                    company_name = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div/div[1]/div[1]').text
                    location = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]').text
                    job_title = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text

                    driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div[2]').click()
                    
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(3)

            try:
                salary_estimate = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div/div[1]/div[4]/span').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            # try:
            #     rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            #     print('x went trough')
            # except NoSuchElementException:
            #     rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                #print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            # try:
            #     driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                # try:
                #     #<div class="infoEntity">
                #     #    <label>Headquarters</label>
                #     #    <span class="value">San Francisco, CA</span>
                #     #</div>
                #     headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                #     print('x went trough')
                # except NoSuchElementException:
                #     headquarters = -1

            try:
                size = driver.find_element_by_class_name("e1pvx6aw2").text
            except NoSuchElementException:
                size = -1
            
            try:
                founded = driver.find_element_by_xpath('//div[@class="e1pvx6aw2"]' and './/span[contains(text(), "Founded")]//following-sibling::*').text
            except NoSuchElementException:
                founded = -1
                    
            try:
                type_of_ownership = driver.find_element_by_xpath('//div[@class="e1pvx6aw2"]' and './/span[contains(text(), "Type")]//following-sibling::*').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element_by_xpath('//div[@class="e1pvx6aw2"]' and './/span[contains(text(), "Industry")]//following-sibling::*').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element_by_xpath('//div[@class="e1pvx6aw2"]' and './/span[contains(text(), "Sector")]//following-sibling::*').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element_by_xpath('//div[@class="e1pvx6aw2"]' and './/span[contains(text(), "Revenue")]//following-sibling::*').text
            except NoSuchElementException:
                revenue = -1

            # try:
            #     competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            # except NoSuchElementException:
            #     competitors = -1

            # except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
            #     headquarters = -1
            #     size = -1
            #     founded = -1
            #     type_of_ownership = -1
            #     industry = -1
            #     sector = -1
            #     revenue = -1
            #     competitors = -1

                
            if verbose:
                # print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                # print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            # "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            # "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            # "Competitors" : competitors})
            #add job to jobs
            
        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div/div[1]/button[7]/span').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.