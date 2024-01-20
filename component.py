import openai
from random import choice
import requests
import os
import json
from time import sleep
from googleapiclient.discovery import build
from bing_image_downloader import downloader
import re
from tkinter import END
from PIL import Image, ImageFont, ImageDraw, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from openai import OpenAI

def image_operation_bing(command, log):
    print('Image operation ..............')
    log.insert(END,'Image operation ..............\n')
    try:
        os.mkdir('bulkimg')
    except FileExistsError:
        pass
    try:
        downloader.download(command, limit=1, output_dir='bulkimg', filter='.jpg', verbose=False)
        try:
            im = Image.open('bulkimg/' + command + '/Image_1.jpg')
        except:
            try:
                im = Image.open('bulkimg/' + command + '/Image_1.png')
            except:
                im = Image.open('bulkimg/' + command + '/Image_1.JPEG')

        # Define the desired size
        desired_size = (670, 330)
        # Calculate the cropping area based on the desired size
        width, height = im.size
        left = (width - desired_size[0]) / 2
        upper = (height - desired_size[1]) / 2
        right = (width + desired_size[0]) / 2
        lower = (height + desired_size[1]) / 2

        # Crop the image
        cropped_image = im.crop((left, upper, right, lower))
        cropped_image.save('bulkimg/' + command + '.jpg')
    except:
        pass


def body_img(command, json_url, headers, body_img_status, log):
    if body_img_status == 'On':
        image_operation_bing(command, log)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ', image)
            log.insert(END, f'Body IMG : --------- {image}\n')
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            print('Body Image:\n.......\n.........\n.........\n', image_wp, '...........\n.........\n.....\n')
            log.insert(END, f'Body Image:\n.......\n.........\n.........\n {image_wp} ...........\n.........\n.....\n')
            return image_wp
        except:
            return ''
    else:
        return ''

def feature_image(command, json_url, headers, feature_img_status, log):
    if feature_img_status == 'On':
        image_operation_bing(command, log)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ', image)
            log.insert(END, f'Body IMG : --------- {image}\n')
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            f_img = [post_id, image_wp]
            return f_img
        except:
            f_img = [0, '']
            return f_img
    else:
        f_img = [0, '']
        return f_img

def youtubevid(keyword, youtube_api, youtube_status, log):
    print('Youtube API .................')
    log.insert(END, 'Youtube API .................\n')
    if youtube_status == 'On':
        try:
            youtube = build('youtube', 'v3', developerKey=youtube_api.strip())
            request = youtube.search().list(q=keyword, part='snippet', type='video', maxResults=1)
            res = request.execute()
            id = res['items'][0]['id']['videoId']
            youtube_url = '<!-- wp:html --><figure  style="text-align: center"><iframe width="640" height="360" src="https://www.youtube.com/embed/' + id + '?rel=0&amp;enablejsapi=1"></iframe></figure><!-- /wp:html --><!-- wp:separator {"align":"center"} --><hr class="wp-block-separator aligncenter"/><!-- /wp:separator -->'
        except Exception as oops:
            print(oops)
            log.insert(END, str(oops)+'\n')
            log.insert(END, '*** Youtube API Has Been Finished or Invalid API*** \n')
            youtube_url = ''
        return youtube_url
    else:
        log.insert(END, 'The Youtube Option was turned off\n')
        return ''

def text_generate(prompt, openai_key, model="gpt-3.5-turbo"):
    client = OpenAI(api_key=openai_key)
    print('prompts ', prompt)
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": ''},
            {"role": "user","content": prompt}
            ],
            model=model,
        )
    return response.choices[0].message.content



def text_render(prompt, openai_key, engine, engine_type, temp, log):
    openai.api_key = openai_key
    sleep_sec = 0
    attempts = 1
    max_attempts = 4
    while attempts < max_attempts:
        try:
            text = text_generate(prompt, openai_key, engine_type)
            break
        except Exception as Opps:
            print(f"OpenAI Fail, trying {str(attempts + 1)} time...waiting time {str(sleep_sec)} seconds...")
            print(f'Error Message from OpenAI Server : {str(Opps)}')
            log.insert(END, f"OpenAI Fail, trying {str(attempts + 1)} time...waiting time {str(sleep_sec)} seconds...\n")
            log.insert(END, f'Error Message from OpenAI Server : {str(Opps)}\n')
            sleep(sleep_sec)
            sleep_sec += 20
            attempts += 1
    else:
        text = 'openaierror'
        print("Maximum number of attempts reached. Operation failed...")
        log.insert(END, "Maximum number of attempts reached. Operation failed...\n")
    return text

def remove_wh(text):
    words_to_remove = ["what ", "which ", "when ", "is ", "how ", "who ", "where ", "did "]
    symbols_to_remove = ["?", ":", "#", "@", "$", "%", "&", "(", ")","!",".","<h2>","</h2>","<",">","/"]
    word_pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, words_to_remove)))
    symbol_pattern = r'[{}]+'.format(''.join(map(re.escape, symbols_to_remove)))
    cleaned_text = re.sub(word_pattern, '', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(symbol_pattern, '', cleaned_text)
    return cleaned_text

def remove_content(text_data):
    words_to_remove = ["Introduction:","Introduction","Q:","A:","Q1:","Q2:","Q3:","Q4:", "Q5:", "A1:","A2:","A3:","A4:","A5:"]
    word_pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, words_to_remove)))
    cleaned_text = re.sub(word_pattern, '', text_data, flags=re.IGNORECASE)
    return cleaned_text

def outline_format(data):
  datas = data.splitlines()
  outline = ''
  for heading in datas:
    if len(heading) > 0 and not 'conclusion' in heading.lower() and not 'introduction' in heading.lower():
      if 'H1' in heading.upper() or 'H2' in heading.upper() or 'H3' in heading.upper():
        outline += heading + '\n'
  return outline

def content_format(content, keyword, youtube_api, youtube_status, json_url, headers, body_img_status, log):
  if '</h1>' in content:
    content_strip = content.split('</h1>')[1].replace('</b>','</b></br>').replace('<h2>','~~<h2>').replace('</h2>','</h2>~~').split('~~')
  elif '</H1>' in content:
    content_strip = content.split('</H1>')[1].replace('</b>', '</b></br>').replace('<h2>', '~~<h2>').replace('</h2>', '</h2>~~').split('~~')
  else:
    content_strip = content.replace('<h2>','~~<h2>').replace('</b>','</b></br>').replace('</h2>','</h2>~~').split('~~')
  content_body = ''
  youtube_added = 0
  youtube = ''
  for parse in content_strip:
    if '<h2>' in parse.lower() and not 'conclusion' in parse.lower() and not 'frequently' in parse.lower():
      image = body_img(remove_wh(parse), json_url, headers, body_img_status, log)
      parse += image
    if 'conclusion' in parse.lower() or 'frequently' in parse.lower() and youtube_added == 0:
      if '<h2>' in parse.lower() or '<h3>' in parse.lower():
        youtube = youtubevid(keyword, youtube_api, youtube_status, log)
        youtube += parse
        parse = youtube
        youtube_added += 1
    if '<h2>' in parse.lower() and "introduction" in parse.lower():
        parse = ''
    content_body += parse
  if youtube_added == 0:
    content_body += youtube
  content_regex = remove_content(content_body)
  return content_regex

def content_body(keyword, outline_prompt, content_prompt, openai_key, engine, engine_type, youtube_api, youtube_status, json_url,headers, body_img_status, log):
    print('Content body .................')
    log.insert(END, f'Content body .................\n')
    outline = outline_format(text_render(outline_prompt.replace('((keyword))',keyword), openai_key, engine, engine_type, log))
    print(outline)
    log.insert(END, f'{outline}\n')
    if outline != 'outlineerror':
        content = content_format(text_render(f"{outline} \n {content_prompt.replace('((keyword))',keyword).replace('((WPFormatting))','This is important to Bold the Title and all headings of the article, and use appropriate headings for H tags. Every single output must be wrapped be HTML Markup, like Heading (<h1></h1>, <h2></h2>, <h3></h3>, <h4></h4>), text(<p></p>), List(<ul><li></li></ul>), table(<table><tr><th></th></tr><tr><td></td></tr></table>), bold(<b></b>) etc tags. But please ignore unnecessary talk like --Heres the HTML markup for the article--, cause this content is for my reader.')}", openai_key, engine, engine_type, log).replace('\n', ''), keyword, youtube_api, youtube_status, json_url, headers, body_img_status, log)
        print('Content body done .................')
        log.insert(END, f'Content body done .................\n')
        return content
    else:
        return 'contenbodyerror'

def create_category(cat_name, json_url, headers):
    id = 0
    if len(cat_name) > 0:
        data = {"name":cat_name}
        cat = requests.post(json_url + '/categories', headers=headers, json=data)
        try:
            id = str(json.loads(cat.content)['id'])
        except:
            try:
                id = str(json.loads(cat.content)['additional_data'][0])
            except:
                pass
    return id

'''
import requests
from requests.auth import HTTPBasicAuth

def get_or_create_category(category_name, consumer_key, consumer_secret, site_url):
    # WooCommerce API endpoint and credentials
    categories_url = f"{site_url}/wp-json/wc/v3/products/categories"
    auth = HTTPBasicAuth(consumer_key, consumer_secret)

    # Check if the category already exists
    params = {"search": category_name}
    response = requests.get(categories_url, auth=auth, params=params)

    if response.status_code == 200:
        categories = response.json()
        if categories:
            existing_category_id = categories[0]["id"]
            print(f"Category '{category_name}' already exists with ID: {existing_category_id}")
            return existing_category_id

    # If the category doesn't exist, create it
    new_category_data = {"name": category_name}
    response = requests.post(categories_url, auth=auth, json=new_category_data)

    if response.status_code == 201:
        new_category_id = response.json().get("id")
        print(f"Category '{category_name}' created with ID: {new_category_id}")
        return new_category_id
    else:
        print(f"Failed to create category '{category_name}'. Status code: {response.status_code}")
        print("Error details:", response.json())
        return None

def create_product(product_name, category_name, consumer_key, consumer_secret, site_url):
    # Get or create the category and get its ID
    category_id = get_or_create_category(category_name, consumer_key, consumer_secret, site_url)

    if category_id is not None:
        # WooCommerce API endpoint and credentials for product creation
        products_url = f"{site_url}/wp-json/wc/v3/products"
        auth = HTTPBasicAuth(consumer_key, consumer_secret)

        # Product data to be posted, including category and images
        product_data = {
            "name": product_name,
            "type": "simple",
            "regular_price": "19.99",
            "description": f"This is a sample {product_name} description.",
            "categories": [
                {
                    "id": category_id
                }
            ],
            "images": [
                {
                    "src": "https://m.media-amazon.com/images/I/41GcCeBaq5L._AC_SL1080_.jpg",  # Replace with the actual URL of the image
                    "position": 0
                },
                {
                    "src": "https://m.media-amazon.com/images/I/51fyK8EsRLL._AC_SL1500_.jpg",
                    "position": 1
                }
                # Add more images as needed
            ],
            "short_description": "Short description of the product.",
            "sku": "ABC123",  # Stock Keeping Unit
            "stock_quantity": 10,  # Available stock quantity
            "status": "publish",
            # Add more product details as needed
        }

        # Make the API request to create a new product
        response = requests.post(products_url, auth=auth, json=product_data)

        # Check the response
        if response.status_code == 201:
            created_product = response.json()
            print(f"{product_name} created successfully!")
            print(f"{product_name} ID:", created_product.get("id"))
            
            # Print the product link
            product_link = f"{site_url}/product/{created_product.get('slug')}/"
            print("Product Link:", product_link)
        else:
            print(f"Failed to create {product_name}. Status code:", response.status_code)
            print("Error details:", response.json())

# Example usage
product_name_input = "Sample Product by python 2"
category_name_input = "New Category"
consumer_key_input = "ck_2f9c3979e726fe187d91be14d5156358191f55eb"
consumer_secret_input = "cs_bc39de27b69cd558bb33199ea23472c1a3b5e429"
site_url_input = "https://ebookwise.com"

create_product(product_name_input, category_name_input, consumer_key_input, consumer_secret_input, site_url_input)


'''