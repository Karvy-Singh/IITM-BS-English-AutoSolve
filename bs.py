
import time,os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import openai

link= "" #provide link of assignment
service=Service("/usr/local/bin/chromedriver") 
driver = webdriver.Chrome(service=service)
driver.get(link)
driver.maximize_window()
button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".google-login-btn")))
button.click()
time.sleep(3)
handles = driver.window_handles 
for i in handles: 
    driver.switch_to.window(i) 
    print(i)
    print(driver.title) 

time.sleep(3)
element = driver.switch_to.active_element
element.send_keys("") #enter your email id
time.sleep(2)
next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")
next_button.send_keys(Keys.ENTER)
time.sleep(4)
element2 = driver.switch_to.active_element
element2.send_keys("") #enter your password
next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")
next_button.send_keys(Keys.ENTER)

time.sleep(15)
handles = driver.window_handles 
for i in handles: 
    driver.switch_to.window(i) 
    print(i)
    print(driver.title) 


questions= driver.find_elements(By.XPATH,"//div[contains(@class,'qt-mc-question qt-embedded')]" )
for i,container in enumerate(questions, start=1):
    with open("question.txt",'a') as f:
        question = container.find_element(By.CLASS_NAME, "qt-question").text
        f.writelines(str(i)+question+'\n')
        choices= container.find_element(By.CLASS_NAME, "qt-choices").text
        f.writelines(choices+'\n')
    
time.sleep(10)


openai.api_key = "" #enter your openai key made from openrouter 
openai.api_base = "https://openrouter.ai/api/v1"

with open("question.txt", 'r') as file:
    mcqs= file.read()

response = openai.ChatCompletion.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        {"role":"system", "content":"""" You return final answer to each question in form of a python list with string, DO NOT  put '' or "" """},
        {"role": "user", "content": f"""answer the following english questions, just provide the final answer to each of them, not in option number but option text whatever that is: {mcqs} """}
        ]
)

final_ans= response["choices"][0]["message"]["content"]
print(final_ans)
os.remove('question.txt')

answers= driver.find_elements(By.XPATH,"//div[contains(@class,'qt-choices')]" )
for i,container in enumerate(answers, start=0):
    ans=final_ans.strip('[]').split(',')[i]
    options = container.find_elements(By.CLASS_NAME, "gcb-mcq-choice")

    for option in options:
        label = option.find_element(By.TAG_NAME, "label")         
        time.sleep(1)
        if str(label.text.strip()) == str(ans.strip(""" ''"" """)):  
            print(f"Found: {label.text}")
            label.click()
            time.sleep(2)
            break

submit= driver.find_element(By.XPATH, "//button[contains(@class,'gcb-button qt-check-answer-button')]")
submit.click()

time.sleep(3)

ok=driver.find_element(By.XPATH, "//button[contains(@class,'btn btn-link btn-submit ng-star-inserted')]")
ok.click()

time.sleep(15)
driver.quit()
