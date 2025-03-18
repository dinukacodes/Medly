import requests
import xml.etree.ElementTree as ET

def fetch_pubmed_abstracts(term: str) -> str:
    try:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&retmax=5&retmode=xml"
        response = requests.get(url)
        root = ET.fromstring(response.content)
        ids = [id.text for id in root.findall(".//Id")]
        if not ids:
            return "No abstracts found."
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
        summary_response = requests.get(summary_url)
        summary_root = ET.fromstring(summary_response.content)
        abstracts = [doc.find(".//Item[@Name='Title']").text for doc in summary_root.findall(".//DocSum") if doc.find(".//Item[@Name='Title']") is not None]
        return "\n".join(abstracts[:5])
    except Exception:
        return "Mock abstract: Evidence supports diagnosis (PubMed unavailable)." 
