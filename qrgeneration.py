# import modules
import qrcode
from PIL import Image
import os
import pandas as pd
import csv


df=pd.read_csv('prod_data.csv')

y=df.loc[0,"batch_number"]
os.mkdir(y)

with open('prod_data.csv', mode='r') as csv_file:
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