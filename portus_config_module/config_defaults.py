# portus_config_module/config_defaults.py

from pathlib import Path
from typing import Optional
from portus_config_module.config_utils import candidate_dirs, find_config_path, find_env_path
import textwrap

DEFAULT_OUTPUT_PATH = Path.home() / "Downloads"

# ——— YAML defaults ————————————————————————————————————————————————

CONFIG_FILENAME = "portus_review_config.yaml"

CONFIG_ID = Path(CONFIG_FILENAME).stem
CONFIG_PATH = find_config_path(CONFIG_FILENAME) or Path(CONFIG_FILENAME)
ENV_PATH = find_env_path() or Path(".env")

DEFAULT_CONFIG_CONTENT = textwrap.dedent(f"""\
config_id: {CONFIG_ID}

selected_tab: user_1

user_prompt_bank:
  selected_prompt: prompt_1

  prompt_1: 'You are assisting the customer service please provide a short and warm
    reply to the following review:' 
  prompt_2: 'You are assisting the customer service please provide a short and warm
    reply to the following review:'
  prompt_3:
  prompt_4:
  prompt_5:
  prompt_6:
  prompt_7:
  prompt_8: 

review_sites:
  tripadvisor: true
  google: true
  booking: true
  expedia: true

writer_config:
  output_folder: ""

hotel_url_bank:
  selected_hotel: hotel_1

  hotel_1:
    hotel_1_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_2:
    hotel_2_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_3:
    hotel_3_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_4:
    hotel_4_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_5:
    hotel_5_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_6:
    hotel_6_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_7:
    hotel_7_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

  hotel_8:
    hotel_8_name: 
    tripadvisor: 
    google: 
    booking: 
    expedia: 

jobs:
  scan: true
  clean: true
  reply: true
  sa: true

scan_config:
  scan_general_parameters:
    review_number: 5
    sort_by: newest
    cutoff_date: '2025-01-01'
    review_ratings:
    - ALL
    review_languages:
    - ALL
    proxyEnabled: true

  tripadvisor_add:
    scrapeReviewerInfo: true

  google_add:
    reviews_origin: google
    personal_data: true
    place_id: []

  apify_actors:
    actor_tripadvisor: maxcopell~tripadvisor-reviews
    actor_google: compass~google-maps-reviews-scraper
    actor_booking: voyager~booking-reviews-scraper
    actor_expedia: tri_angle~expedia-hotels-com-reviews-scraper

clean_config:
  columns_to_keep:
    tripadvisor:
    - publishedDate
    - rating
    - title
    - user/name
    - text

    google:
    - publishedAtDate
    - rating
    - title
    - name
    - text

    booking:
    - reviewDate
    - rating
    - reviewTitle
    - userName
    - dislikedText
    - likedText

    expedia:
    - submissionTime/longDateFormat
    - reviewScoreWithDescription/label
    - title
    - reviewAuthorAttribution/text
    - text

model_parameters:
  system_prompt_bank:
    selected_system_prompt: sys_prompt_a
    sys_prompt_a: test a
    sys_prompt_b: test b
    sys_prompt_c: test c
  general_parameters:
    temperature: 0.7
    top_p: 1
    stream: true
    tools: []
    tool_choice: auto
    max_output_tokens: 256000
    store: false

  xai_additional:
    reasoning_effort: low

  additional:
    n_ctx: 512000
    max_tokens: 256000
    top_k: 40
    presence_penalty: 0.2
    frequency_penalty: 0.2

mode:
  default_mode: api

  api:
    default_provider: google

    openai:
      model: gpt-4.1-nano-2025-04-14
      base_url: https://api.openai.com/v1

    google:
      model: gemini-2.0-flash
      base_url: https://generativelanguage.googleapis.com/v1beta/openai/

    xai:
      model: grok-3-mini
      base_url: https://api.x.ai/v1
""")

def reset_config_defaults(config_path: Optional[Path] = None):
    if config_path is None:
        config_path = find_config_path(CONFIG_FILENAME) or next(candidate_dirs()) / CONFIG_FILENAME

    config_path.write_text(DEFAULT_CONFIG_CONTENT, encoding="utf-8")

# ——— ENV defaults ——————————————————————————————————————————————————

DEFAULT_ENV_CONTENT = textwrap.dedent("""\
# AI provider API keys (replace placeholders with real keys)
OPENAI_API_KEY=your-api-key-goes-here
GOOGLE_API_KEY=your-api-key-goes-here
XAI_API_KEY=your-api-key-goes-here
# Apify API key (replace placeholder with real keys)
APIFY_API_KEY=your-api-key-goes-here
""")

def reset_env_defaults(env_path: Optional[Path] = None):
    if env_path is None:
        env_path = find_env_path() or next(candidate_dirs()) / ".env"

    env_path.write_text(DEFAULT_ENV_CONTENT, encoding="utf-8")