
from datetime import datetime, timedelta
import json
import os


import uuid
import requests
from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import default_storage

from fees.models import ServicesTokenStorage

# font = ImageFont.truetype('arial.ttf', size=10)
# font1 = ImageFont.truetype('arial.ttf', size=10)

from django.core.mail import send_mail, BadHeaderError,EmailMessage


from schoolinfo.models import SchoolInformation

def generate_ref_code():
    code=str(uuid.uuid4()).replace("_","")[:6]
    return code


def send_email_func(recipient_list,from_email,body,subject,):
    
    try:
        send_mail(subject=subject, message=body, from_email=str(
                    from_email), recipient_list=recipient_list, fail_silently=True)
        print("send")
        
       
      
        return True
    
    except BadHeaderError:
        print("not sent")
        return False
    
    
     
def send_email_with_attachment_func(recipient_list,from_email,body,subject,):
    
    try:
        send_mail(subject=subject, message=body, from_email=str(
                    from_email), recipient_list=recipient_list, fail_silently=True)
        
        EmailMessage(subject=subject, body=body, from_email=str(
                    from_email), to=recipient_list,reply_to=[from_email,], fail_silently=True)
        return True
    
    except BadHeaderError:
        return False
    
    
 
 
# print(str(uuid.uuid4()))
# pk='c934f571a1904d9ea4cc696c1ba2eef4'
# x_ref='94d91e11-862d-4076-8c4d-3aa530e5511c'
# appId='cid-v1:e996501c-e721-4ac1-97ff-dc6887b85e8c'
# apiKey= "68ebe1a656f84f0187f3f68e8b8f3640"

# {
# "providerCallbackHost": "http://codewithmiki/miki",
# "targetEnvironment": "sandbox"
# }
 
    
    
def get_api_key():
    url="https://sandbox.momodeveloper.mtn.com/collection/token/"
    headers = {
    # Request headers
    'Authorization': 'basic-auth',
     "providerCallbackHost": "http://codewithmiki/miki",
        "x-targetEnvironment": "sandbox",
    'Content-Type': 'application/x-www-form-urlencoded',
    'Ocp-Apim-Subscription-Key': '27fb3691d8ee4fcf93ca32074b766f08',
    
        }
    auth_v=('94d91e11-862d-4076-8c4d-3aa530e5511c','68ebe1a656f84f0187f3f68e8b8f3640')
   
    
    # check if token exist
    if ServicesTokenStorage.objects.filter(name__icontains="mtn").exists():
        token_obj=ServicesTokenStorage.objects.get(name__icontains="mtn")
        db_hours=token_obj.created_time.hour
        ctm=datetime.now().time().hour
        # check if token has expire if so create a new one and update the system
        if ctm-db_hours>0:
            token_obj.delete()
            try:
                response=requests.post(url, auth=auth_v,headers=headers)
                response=response.json()['access_token']
                ServicesTokenStorage.objects.create(name='mtn',token=response)
            except:
                pass
            
            print("ok==>",ctm-db_hours,ctm,db_hours,)
        # else just return the available one
        else:
            response=token_obj.token
            
    # if token doesn't exist call api and generate a new one  
    
    else:
        try:
            # print("last")
            response=requests.post(url, auth=auth_v,headers=headers)
            response=response.json()['access_token']
            ServicesTokenStorage.objects.create(name='mtn',token=response)
        except:
            pass
         
    # print(response)
    # print(response.status_code)
    # print(response.json())

    return response

def get_pay_status(ref,token):
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/"+str(ref)
    print(url)
    headers={
         'X-Target-Environment': 'sandbox',
         'Ocp-Apim-Subscription-Key': 'd581a2f3c28a493586f66521686f2584',
          'Authorization':token
    }
    
    r=requests.get(url,headers=headers)
    print(r)
    return r.json()

def request_to_pay(amount,phone_number,):
    
    token='Bearer '+get_api_key()
    x_ref=uuid.uuid4()
    
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
    

    payload = json.dumps({
    "amount": str(amount),
    "currency": "EUR",
    "externalId": str(uuid.uuid4()).replace("_","")[:8], #"23446545",
    "payer": {
        "partyIdType": "MSISDN",
        "partyId":str(phone_number) #"46733123451"
    },
    "payerMessage": "school fee payment",
    "payeeNote": "this money is for school fee"
    })
    headers = {
    'X-Reference-Id': str(x_ref),#'bc0d2565-cd82-4b8f-b667-4021438a0294',
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd581a2f3c28a493586f66521686f2584',
    'Authorization':token,
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code,'miki')
    # get_pay_status(x_ref,token)
    return response,x_ref,token

def request_to_pay1():
    
    token='Bearer '+get_api_key()['access_token']
    x_ref=uuid.uuid4()
    
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
    

    payload = json.dumps({
    "amount": "55000",
    "currency": "EUR",
    "externalId": "23543243f",
    "payer": {
        "partyIdType": "MSISDN",
        "partyId": "46733123451"
    },
    "payerMessage": "new",
    "payeeNote": "string"
    })
    headers = {
    'X-Reference-Id': str(x_ref),#'bc0d2565-cd82-4b8f-b667-4021438a0294',
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd581a2f3c28a493586f66521686f2584',
    'Authorization':token, #'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6Ijk0ZDkxZTExLTg2MmQtNDA3Ni04YzRkLTNhYTUzMGU1NTExYyIsImV4cGlyZXMiOiIyMDIyLTA4LTAyVDA0OjAxOjI3LjEzMSIsInNlc3Npb25JZCI6IjA0NjBhZTFiLTFhZjQtNGY2ZC1hYmUyLTYwOWM5NmM2NTdmYyJ9.JfffWroLA89bHFJp2ViHSHtuBKMVPIiN2AHKie1mvLl9z-aQ_TkOdzp60t0TG5NJCu4al6BrC3DLK6U8Wkw_xXwHr1iqqwEpdjQ6f8rObMZE6oJANrqNKXqj5D0WMIG634I-v724BD6kNNjie6vx9lzb7VuHEWI36it9axld3lRoNwW9vDr5QnWoaq7tKhLDK72t7zmrT88DKAA5a4UCT87OOnleZdt2ArNLAMWGVA642zdY6zFH4rmpCbU-ATY4qbc9w3-Rkk97Hbc3-kHb-GyRX-ezMB6eZFRDtD81X0wP9ccHi-gjiFG2DDdtDLo7rFGHwB1QxsKD9SZOtyxj-g'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code,'miki')
    get_pay_status(x_ref,token)
    return response,x_ref


# Create your views here.

def receipt_generator(id, st_name, semester, classroom, amount, total_fee, amount_in_words, prepared_by,date,due):
    # schoolinfo=SchoolInformation.objects.all()[0]
    # school_name=schoolinfo.school_name_full
    # school_logo=schoolinfo.school_logo
    # address=schoolinfo.address
    # scphone=schoolinfo.phone
    # pimage=schoolinfo.school_banner_image
    
    # path = os.environ['userprofile'] + f'\Desktop\schoolinformation\ReceiptS\\{st_name}_Receipt'
    # if not os.path.exists(path):
    #     os.makedirs(path, exist_ok=True)
    # save_path = path

    # template = Image.new('RGB', (350, 175), (190, 190, 255, 255))
    

    # pimage = Image.open(pimage).resize((35, 10), Image.ANTIALIAS)

    # logo = Image.open(school_logo).resize((30, 25), Image.ANTIALIAS)


    # template.paste(logo, (10, 3))
  
    # draw = ImageDraw.Draw(template)

    # draw.text((50, 3), f'{school_name}'.upper(), font=font1, fill='darkgreen')
    # draw.text((65, 17), f'P.O.Box: {address}'.upper(), font=font1, fill='darkred')
    # draw.text((98, 31), 'School Fees Receipt', font=font1, fill='gold')
    # draw.text((200, 41), 'Receipt No:', font=font, fill='black')
    # draw.text((258, 41), f'{id}', font=font, fill='black')
    # draw.text((10, 41), 'Date:', font=font, fill='black')
    # draw.text((40, 41), f'{date}', font=font, fill='black')

    # # draw.text((195, 77), 'Republic Of Cameroon'.upper(), font=font1, fill='gold')


    # draw.text((0, 43), '_______________________________________________________________', font=font, fill='black')
    # draw.text((93, 55), f'{st_name}'.title(), font=font, fill='black')
    # draw.text((10, 55), 'Student Name', font=font, fill='black')
    # draw.text((0, 58), '_______________|_______________________________________________', font=font, fill='black')


    # draw.text((93, 70), f'{classroom}'.title(), font=font, fill='black')
    # draw.text((10, 70), 'Class', font=font, fill='darkgreen')
    
    # draw.text((232, 70), f'{semester}'.title(), font=font, fill='black')
    # draw.text((180, 70), 'Semester', font=font, fill='darkgreen')
    
    # draw.text((0, 73), '_______________|_____________|_________|_________________________', font=font, fill='black')
    
    
    
    # draw.text((93, 85), f'{amount} frs', font=font, fill='black')
    # draw.text((10, 85), 'Amount', font=font, fill='darkgreen')
    
    # draw.text((232, 85), f'{total_fee} frs', font=font, fill='black')
    # draw.text((180, 85), 'Total', font=font, fill='darkgreen')
    
    # draw.text((0, 88), '_______________|_____________|_________|_________________________', font=font, fill='black')
    
    
    # draw.text((93, 102), f'  {amount_in_words}'.title(), font=font, fill='black')
    # draw.text((10, 102), 'Amount in Words', font=font, fill='darkgreen')
    # draw.text((0, 105), '_______________|_______________________________________________', font=font, fill='black')
    
    
    # draw.text((93, 116), f'{due} frs'.title(), font=font, fill='black')
    # draw.text((10, 116), 'Due/Owing Fee', font=font, fill='darkgreen')
    
    # # draw.text((232, 116), f'{total_fee}'.title(), font=font, fill='black')
    # # draw.text((180, 116), 'Total:', font=font, fill='darkgreen')
    
    # draw.text((0, 119), '_______________|_____________|_________|_________________________', font=font, fill='black')
    
    


    # draw.text((132, 138), f'  {prepared_by}'.title(), font=font, fill='black')
    # draw.text((5, 138), 'Prepared by', font=font, fill='darkgreen')
    # draw.text((130, 141), '|_______________________________________________', font=font, fill='black')

    # draw.text((137, 155), f'{prepared_by}'.title(), font=font, fill='black')
    # draw.text((10, 155), 'Recipient Signature:', font=font, fill='darkgreen')
    # draw.text((130, 155), '|_______________________________________________', font=font, fill='black')
    
    # # filename=default_storage.save(st_name,template)
    
    # # print(os.path.join('static', 'font.png'))
    # filename=template.save(os.path.join('static', f'receipts/{st_name}.png'))
    # f=os.path.relpath(f'static/receipts/{st_name}.png')
    

    # filename=open(f,mode='rb')
    # filename=default_storage.save(f'receipts/{st_name}.png',filename,)
    # os.remove(f)
    
    # return filename,st_name
    pass