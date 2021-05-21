from revwrapper import session
from string import Template
import requests
import json



class inputs(object):
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
        #self.title

    def send_file(self):
        jsonpayload = {"url": self.proxy_url}
        headerspayload = {'Content-Type': 'application/json'}

        #print('payload is', jsonpayload)
        path = 'https://api.rev.com/api/v1/inputs'
        #add in error checking for reponse error codes list in rev documetation! 
        
        try:
            response = session.post(path, json=jsonpayload, headers=headerspayload)
            response.raise_for_status()
            r = response.headers
            rev_URI = r['Location']
            #print('successfully told Rev about the file: ', rev_URI)
        
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return rev_URI
        


class orders(object):
    def order_list(self):
        path = 'https://api.rev.com/api/v1/orders/'
        try:
            response = session.get(path)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return response.json()        


class single_order(object):
    def __init__(self):
        pass

    def order_info(self, order_id):
        path = 'https://api.rev.com/api/v1/orders/{}/'.format(order_id)
        try:
            print('getting info from rev')
            response = session.get(path)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            print(response.status_code)
            order_json = response.json()

            print('order info is: ', order_json)
            order_info = {}
            order_info['order_id'] = order_json.get('order_number')
            #set order status
            order_info['status'] = order_json.get('status')

            #get latest comment from Rev order info 
            sorted_comments = sorted(order_json['comments'], key = lambda i: i['timestamp'],reverse=True)
            order_info['latest_comment'] = sorted_comments[0]['text']
            print('latest order comment: ',order_info['latest_comment'])


            #loop through all attachments in JSON, elminate all but transcription type
            for x in order_json['attachments']:
                #append attachment id and link key value pairs to a dict
                if x['kind'] == 'transcript':
                    order_info['attachment_id'] = x['id']
                    #order_info['attachment_url'] = x['links'][0]['href']
            
            return order_info


    def submit_order(self, inputURI, duration):
        single_order_json = {}
        single_order_json['transcription_options'] = {}
        single_order_json['transcription_options']['inputs'] = []
        single_order_json['transcription_options']['inputs'] = [{'audio_length_seconds': duration, 'uri': inputURI}]
        single_order_json['transcription_options']['timestamps'] = True
        single_order_json['transcription_options']['output_file_formats'] = ["Text", "JSON"]

        single_order_json['notification'] = {}
        single_order_json['notification']['url'] = 'https://webhook.site/5e5e2db4-1a60-4c20-b443-8c2e6f7891ef'
        single_order_json['notification']['level'] = "Detailed"

        path = 'https://api.rev.com/api/v1/orders'

        prepped_json = json.dumps(single_order_json)
        print('submitting order:',prepped_json)
        
        try:
            response = session.post(path, json=single_order_json)
            print('submit order reponse code:', response.status_code)
            print(response.url)
            response.raise_for_status()
            # Code here will only run if the request is successful
  
            r = response.headers
            order_url = r['Location']
            order_URI = order_url.replace('https://api.rev.com/api/v1/orders/', '')
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return order_URI
    
    def json_link(self, attachment_id):
        path = 'https://api.rev.com/api/v1/attachments/{}/content.json'.format(attachment_id)
        try:
            response = session.get(path)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            transcript_json = response.json()
            return transcript_json


    def download_json(self, attachment_url):
        try:
            response = session.get(attachment_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return response.json()

    def editor_link(self, attachment_id):
        path = 'https://api.rev.com/api/v1/attachments/{}/share'.format(attachment_id)
        data = {"access_level": "ReadOnly"}
        try:
            response = session.post(path, data=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            r = response.headers
            editor_link = r['Location']
        return editor_link

    def cancel_order(self):
        pass
    

class attachments(object):
    def __init__(self, job_title):
        self.job_title = job_title
    

