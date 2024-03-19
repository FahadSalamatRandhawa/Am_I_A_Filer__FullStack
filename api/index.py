from fastapi import FastAPI,Query,Depends,Body,HTTPException,status
from api.Model__Read_XLSX_File import Read_XLSX
import pandas as pd
import asyncio
import datetime
from sqlmodel import Field, SQLModel
from typing import Annotated

app:FastAPI=FastAPI()

class FilterData(SQLModel):
    filter:str=Field(min_length=1)
    value:str=Field(min_length=1)

    def __iter__(self):
        return iter((self.filter, self.value))
def validate_body(request_body:FilterData):
    print(request_body)
    try:
        FilterData.model_validate(request_body)
        return request_body
    except Exception as e:
        raise HTTPException(status_code=420, detail="Invalid request body")
# async def read_file(file_object):
#     try:
#         print("started reading",file_object.url)
#         await file_object.read_file()
#     except Exception as e:
#         print({"error":e})

@app.on_event("startup")
async def on_startup():
    global incomeTaxObject, salesTaxObject
    incomeTaxObject = Read_XLSX("https://fbr.gov.pk/Downloads/?id=3901&Type=Docs")
    salesTaxObject = Read_XLSX("https://www.fbr.gov.pk/Downloads/?id=77772&Type=Docs")

    #creating asynchoronous tasks to start reading files in background due to long read time
    loop = asyncio.get_event_loop()
    loop.create_task(salesTaxObject.read_file())
    loop.create_task(incomeTaxObject.read_file())



@app.get("/api")
def API_Status():
    return {"status":"ok"}

#check file reading completion status
@app.get("/api/status")
def data_status():
    print(incomeTaxObject.read_complete,salesTaxObject.read_complete)
    return {"incometax status":incomeTaxObject.read_complete,"salestax status":salesTaxObject.read_complete}

# find a tax payer 
@app.post("/api/check")
# @title Finding Tax Payer
def check_filer(requestdata:FilterData=Depends(validate_body)): #requestdata:FilterData=Depends(validate_body)
    print("Running POST CHECK api")
    filter,value=requestdata
    print("valeu : "+value,"filter : "+filter)
    if (not salesTaxObject.read_complete or not incomeTaxObject.read_complete):
        return {'success':False,'message':"files not read yet"}
    tax_payer=None
    try:
        #only this file has CNIC list
        if (filter=="CNIC"):
            print("Reading salesTax")
            sales_dataframe=salesTaxObject.get_file()
            print(sales_dataframe)
            tax_payer=sales_dataframe[sales_dataframe["CNIC"]==value]
        else:

        # both files have overlapping columns, combine both files and filter
            print("Reading ATL")
            incomeTax_frame=incomeTaxObject.get_file()
            salesTax_frame=salesTaxObject.get_file()
            ATL_List = pd.concat([incomeTax_frame, salesTax_frame])
            tax_payer=ATL_List[ATL_List[filter].str.lower()==value.lower()]

        if not tax_payer.empty:
            # Convert SR_NO and SR to string to avoid out of Bound error for float values
            tax_payer = tax_payer.fillna("")
            tax_payer.loc[:, "SR_NO"] = tax_payer["SR_NO"].astype(str, errors='ignore')
            tax_payer.loc[:, "SR"] = tax_payer["SR"].astype(str, errors='ignore')
            print(tax_payer)
            
            # Reset index and convert DataFrame to JSON
            return tax_payer.reset_index(drop=True).to_json(orient='records')
        else:
            return {'success':False,'message':"record not found"}

    except Exception as e:
        print(e)
        return {"error":str(e)}


@app.get("/api/incometax")
async def get_incometax():
    if incomeTaxObject.read_complete:
        print(incomeTaxObject.get_file())
        return incomeTaxObject.get_file().to_json()
    else:
        return {"status": "File not ready"}

@app.get("/api/salestax")
def get_salestax():
    if salesTaxObject.read_complete:
        print(salesTaxObject.get_file())
        return salesTaxObject.get_file().to_json()
    else:
        return {"status": "File not ready"}
