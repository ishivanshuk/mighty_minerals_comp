import pandas as pd
import csv
import rsa

number_prod=43
test_name='sos'
batch_number='WP500556FASD123'
mfg_date='21-03-2012'

f=open(batch_number+'.csv','w')
header = ['name', 'mfg_date_dd-mm-yy','batch_number', 'number_products','checked','prod_id','hash']
writer = csv.writer(f)
writer.writerow(header)


data = [[test_name,mfg_date,batch_number,number_prod,'NO','','']]
writer = csv.writer(f)

for i in range(0,number_prod):
    writer.writerows(data)
f.close()


import pandas as pd
df=pd.read_csv(batch_number+'.csv')


for i in range(0,number_prod):
    x="{:03d}".format(i) #enter number of digits in number of products in table
    df.loc[i,'prod_id']=df.loc[0,'batch_number']+x

print(df)


def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey

def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False

privateKey, publicKey =loadKeys()

for i in range(0,number_prod):
    enc_data=df.loc[i,'prod_id']
    df.loc[i,'hash']=encrypt(enc_data,publicKey)


print(df)


df.to_csv('prod_data.csv', mode='a', index=True, header=False)
df.to_csv(batch_number+'.csv')


import qrcode
from PIL import Image
import os
import pandas as pd
import csv


df=pd.read_csv(batch_number+'.csv')

y=df.loc[0,"batch_number"]
os.mkdir(y)

with open(batch_number+'.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
	
    for row in csv_reader:
					Logo_link = 'logo.jpg'

					logo = Image.open(Logo_link)

# taking base width
					basewidth = 100

# adjust image size
					wpercent = (basewidth/float(logo.size[0]))
					hsize = int((float(logo.size[1])*float(wpercent)))
					logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
					QRcode = qrcode.QRCode(
						error_correction=qrcode.constants.ERROR_CORRECT_H
					)
					id = row["hash"]

# adding URL or text to QRcode
					QRcode.add_data(id)

# generating QR code
					QRcode.make()

# taking color name from user
					QRcolor = 'black'

# adding color to QR code
					QRimg = QRcode.make_image(
						fill_color=QRcolor, back_color="white").convert('RGB')

# set size of QR code
					pos = ((QRimg.size[0] - logo.size[0]) //2,
						(QRimg.size[1] - logo.size[1]) // 2)
					QRimg.paste(logo, pos)

# save the QR code generated
					x=row["prod_id"]
					save_name=y+'/qr_'+x+'.png'
					if(QRimg.save(save_name)):
						print('QR generation failed for',x)
					else:
						print('QR generated for',x)
					
					del x


import os

os.remove(batch_number+'.csv')



