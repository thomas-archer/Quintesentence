from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tweepy
import urllib.request
from PIL import Image
import random
import text2emotion as te
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import yake

#Connect to twitter API
def get_twitter_api():
    consumer_key = ''
    consumer_secret = ''

    access_token = ''
    access_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    return api

#Retrieve most recent tweet from specified account
def get_recent_tweet(api):
    user_twitter_id = 'MagicRealismBot'
    tweets = api.user_timeline(screen_name=user_twitter_id)
    most_recent_tweet = tweets[0].text
    return most_recent_tweet

#Use Computer Vision Explorer tool to generate image from input text
def generate_image(input_text):
    options = Options()
    #Controls whether browser is visible. Comment out to make visible
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver')
    driver.set_window_size(1300,1300)

    #Login Process
    generation_url = 'https://vision-explorer.allenai.org/text_to_image_generation'
    driver.get(generation_url)

    input_area = driver.find_element_by_class_name('ant-input')
    input_area.send_keys(input_text)

    run_button = driver.find_element_by_css_selector('.ant-btn > span:nth-child(1)')
    run_button.click()
    #Get output image
    output_image= WebDriverWait(driver,300).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/section/section/section/main/main/div[6]/div[2]/div/div[2]/div/div/div/canvas')))
    #output_image = driver.find_element_by_xpath('/html/body/div/section/section/section/main/main/div[6]/div[2]/div/div[2]/div/div/div/canvas')
    location = output_image.location
    size = output_image.size
    driver.save_screenshot('/Users/tarcher/Documents/Classwork/TextToImageBot/'+"shot.png")
    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h - 1
    im = Image.open('/Users/tarcher/Documents/Classwork/TextToImageBot/'+'shot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    random_photo_file_name = 'auto_image'+str(random.randint(0,10000))+'.png'
    im.save('/Users/tarcher/Documents/Classwork/TextToImageBot/'+random_photo_file_name)
    driver.close()
    return random_photo_file_name

#Use sentiment/emotion and keyword extraction to create more quintessential phrase/sentence
def transform(text):
    emotion_ratings = te.get_emotion(text)
    emotion_ratings
    significant_emotion = max(emotion_ratings, key = emotion_ratings.get)

    kw_extractor = yake.KeywordExtractor()
    language = 'en'
    max_ngram_size = 3
    deduplication_threshhold = 0.9
    numOfKeywords = 10
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshhold,top=numOfKeywords,features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    keywords.reverse()
    top_keywords = keywords[:5]

    significant_emotion

    emotion_colors={'Happy':'Yellow','Angry':'Red','Surprise':'Green','Sad':'Blue','Fear':'Dark'}
    significant_color = emotion_colors[significant_emotion]

    top_keywords_wo_scores = [x[0] for x in top_keywords]
    top_keywords_wo_scores

    final_string=''+significant_emotion+' '+significant_color
    for i in top_keywords_wo_scores:
        final_string+=' '+i
    return final_string


#main function to run script/bot
def main():
    print('Starting program!')
    api = get_twitter_api()
    #recent_tweet = get_recent_tweet(api)
    recent_tweet =  'test'
    generation_input = transform(recent_tweet)
    generated_image = generate_image(generation_input)
    api.update_with_media('/Users/tarcher/Documents/Classwork/TextToImageBot/'+generated_image,recent_tweet)
    print('Media Uploaded!')


if __name__ == "__main__":
    main()
