import os
from pyairtable import Api, exceptions
# only  for development
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
os.environ['AIRTABLE_API_KEY'] = config["Airtable"]["API_KEY"]
os.environ['AIRTABLE_BASE_ID'] = config['Airtable']['BASE_ID']
os.environ['AIRTABLE_TABLE_ID'] = config['Airtable']['TABLE_ID']

def main():
    try:
        api = Api(os.environ['AIRTABLE_API_KEY'])
        table = api.table(os.environ['AIRTABLE_BASE_ID'],
                          os.environ['AIRTABLE_TABLE_ID'])
        answer = table.create(
            {"Full Name": "Bob", "Email": "bobquebola@gmail.com",
             "Message": "Necesito contratarte ya"})
    except exceptions.PyAirtableError:
        print('Communication error')
    else:
        print(answer)

if __name__ == '__main__':
    main()
