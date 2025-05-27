# portus_sa_module\sa_manager.py

from pathlib import Path

from portus_config_module.config_manager import reload_config, get_provider_name
from portus_sa_module.sa_writer import write_individual_scores
from portus_sa_module.sa_report import generate_sa_report

def handle_sentiment_analysis(site: str, clean_file_path: Path) -> None:
    reload_config()
    provider = get_provider_name()

    write_individual_scores(clean_file_path)

    output_folder = clean_file_path.parent
    generate_sa_report(clean_file_path, provider=provider, output_folder=output_folder)