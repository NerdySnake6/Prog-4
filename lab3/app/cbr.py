import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

async def fetch_currencies() -> List[Dict[str, str]]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(CBR_URL)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
    
    currencies = []
    for valute in root.findall('Valute'):
        code = valute.find('CharCode').text
        name = valute.find('Name').text
        currencies.append({'code': code, 'name': name})
    return currencies

async def get_rate(currency_code: str) -> float:
    async with httpx.AsyncClient() as client:
        resp = await client.get(CBR_URL)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
    
    for valute in root.findall('Valute'):
        if valute.find('CharCode').text == currency_code:
            nominal = int(valute.find('Nominal').text)
            value = float(valute.find('Value').text.replace(',', '.'))
            return value / nominal
    raise ValueError(f"Currency {currency_code} not found")
