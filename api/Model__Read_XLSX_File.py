import pandas as pd
import asyncio
from functools import partial

class Read_XLSX():
    file: pd.DataFrame
    read_complete = False

    def __init__(self, url: str, engine: str = "openpyxl"):
        self.engine = engine
        self.url = url
        self.file = None
        self.read_complete = False

    async def read_file(self):
        loop = asyncio.get_event_loop()
        print("starting file reading",self.url)
        try:
            read_excel_partial = partial(pd.read_excel, self.url, engine=self.engine, dtype={'CNIC': str})
            self.file = await loop.run_in_executor(None, read_excel_partial)
            print("File read complete")
            self.read_complete = True
        except Exception as e:
            print(f"An error occurred: {e}")


    def get_file(self):
        try:
            return self.file
        except Exception as e:
            print(e)
            return {"Error":e}

    async def update_file(self, url: str):
        self.url = url
        await self.read_file()
