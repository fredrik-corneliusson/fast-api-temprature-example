# Minimalt exempel för att spara och visa tempraturer 
Skapat för att lära ut grunder i python webbprogrammering.

## Installation
Testat med python 3.7.

### Installera beroenden 

    pip install -r requirements.txt

### Köra appen

    uvicorn main:app --reload
   
### Lägga in mätvärden (posta mot api)

    curl --location --request POST 'http://127.0.0.1:8000/tempraturer/sovrum/21.2'
    
### Visa mätvärden 

    http://127.0.0.1:8000/static/index.html
    