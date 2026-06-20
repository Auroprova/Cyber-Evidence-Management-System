import re

def extract_iocs(text):

    phones = re.findall(r"\b\d{10}\b", text)

    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    urls = re.findall(
        r"https?://\S+|www\.\S+",
        text
    )

    upi_ids = re.findall(
        r"\b[\w.-]+@[\w]+\b",
        text
    )

    return {
        "Phone Numbers": phones,
        "Email Addresses": emails,
        "URLs": urls,
        "UPI IDs": upi_ids
    }

print("IOC Extractor Ready")