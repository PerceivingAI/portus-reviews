# clean_module\clean_columns.py

from pathlib import Path
from writer_module.writer_clean import write_clean_excel

def clean_columns(site: str, columns_to_keep: list, source_file: Path, target_file: Path):
    write_clean_excel(
        site=site,
        input_file=source_file,
        output_file=target_file,
        columns=columns_to_keep
    )
