import csv
f=open('prod_data.csv','w')
header = ['index','name', 'mfg_date_dd-mm-yy','batch_number', 'number_products','checked','prod_id','hash']
writer = csv.writer(f)
writer.writerow(header)
f.close()