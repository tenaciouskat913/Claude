import requests
import trafilatura
from bs4 import BeautifulSoup

import config


class ExtractionError(Exception):
    pass


def _fallback_extract(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def fetch_policy_text(url: str) -> str:
    try:
        response = requests.get(
            url,
            timeout=config.URL_FETCH_TIMEOUT_SECONDS,
            headers={"User-Agent": "Mozilla/5.0 (EMP Fact Sheet Generator)"},
        )
    except requests.exceptions.Timeout:
        raise ExtractionError("Could not reach that URL (timed out). Check the address or paste the policy text instead.")
    except requests.exceptions.ConnectionError:
        raise ExtractionError("Could not reach that URL. Check the address or paste the policy text instead.")
    except requests.exceptions.RequestException:
        raise ExtractionError("Could not reach that URL. Check the address or paste the policy text instead.")

    if response.status_code != 200:
        raise ExtractionError(f"The page returned an error (status {response.status_code}). Try pasting the text instead.")

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type and "application/xhtml" not in content_type:
        raise ExtractionError(
            "This looks like a non-HTML document (e.g. a PDF). Please paste the extracted text directly."
        )

    text = trafilatura.extract(response.text) or ""
    if len(text.strip()) < config.MIN_EXTRACTED_TEXT_CHARS:
        text = _fallback_extract(response.text)

    if len(text.strip()) < config.MIN_EXTRACTED_TEXT_CHARS:
        raise ExtractionError(
            "Couldn't extract readable text from that page (it may require JavaScript or be behind a "
            "login). Please paste the policy text instead."
        )

    return text.strip()
