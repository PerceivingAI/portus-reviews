from typing import List, Dict, Tuple
from portus_api_module.api_factory import get_client
import time
import re

INDIVIDUAL_PROMPT = (
    "Rate the sentiment of the following hotel review on a scale from 1 (very negative) to 10 (very positive). "
    "Respond ONLY with the numeric score. Do not include any explanation or comments.\n\n"
    "Title: {title}\nReview: {text}"
)

OVERALL_PROMPT = (
    "Given the following hotel reviews, respond with the overall sentiment score on a scale from 1 (very negative) "
    "Take all the reviews into consideration to get the overall sentiment."
    "to 10 (very positive), followed by a brief summary (2–3 sentences). Start your response with the score on its own line.\n\n"
    "{reviews}"
)

def _extract_score(text: str) -> float:
    match = re.search(r"\b\d+(\.\d+)?\b", text)
    if not match:
        raise ValueError("No numeric score found in model response")
    return float(match.group(0))

def score_individual_review(title: str, text: str) -> float:
    client = get_client()
    prompt = INDIVIDUAL_PROMPT.format(title=title.strip(), text=text.strip())

    retry_delays = [2, 5, 10]
    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            response = client.chat(messages=[{"role": "user", "content": prompt}])
            if hasattr(response, "choices"):
                content = response.choices[0].message.content
            else:
                content = "".join(chunk for chunk in response if isinstance(chunk, str))
            #print(f"[score_individual_review] Raw model response: {repr(content)}")
            return max(1.0, min(_extract_score(content), 10.0))
        except Exception as exc:
            #print(f"[score_individual_review] ❌ Attempt {attempt} failed: {exc}")
            if attempt == len(retry_delays):
                return float("nan")
            time.sleep(delay)

def score_all_reviews(reviews: List[Dict[str, str]]) -> Tuple[float, str]:
    client = get_client()
    blob = ""
    for i, r in enumerate(reviews, 1):
        blob += f"Review {i}:\nTitle: {r.get('title','')}\nText: {r.get('text','')}\n\n"
    prompt = OVERALL_PROMPT.format(reviews=blob)

    retry_delays = [2, 5, 10]
    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            response = client.chat(messages=[{"role": "user", "content": prompt}])
            if hasattr(response, "choices"):
                content = response.choices[0].message.content
            else:
                content = "".join(chunk for chunk in response if isinstance(chunk, str))
            #print(f"[score_all_reviews] Raw model response: {repr(content)}")
            score_line, *rest = content.split("\n", 1)
            score = max(1.0, min(_extract_score(score_line), 10.0))
            summary = rest[0].strip() if rest else ""
            return score, summary
        except Exception as exc:
            print(f"[score_all_reviews] ❌ Attempt {attempt} failed: {exc}")
            if attempt == len(retry_delays):
                return float("nan"), "Error during overall scoring."
            time.sleep(delay)
