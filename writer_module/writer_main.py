from pathlib import Path
from datetime import datetime

from portus_config_module.config_manager import get_selected_hotel_name
from writer_module.writer_utils import (
    get_site_folder,
    get_hotel_root_folder,
    generate_filenames
)

def prepare_writer_paths(base_output_folder: Path, site: str) -> dict:
    """
    Creates or reuses hotel and site folders and archive subfolder.
    Returns paths for archive file and cleaned file.
    """
    hotel_name = get_selected_hotel_name()
    hotel_root_folder = base_output_folder / get_hotel_root_folder(hotel_name)
    site_folder = hotel_root_folder / get_site_folder(site, hotel_name)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    names = generate_filenames(site, timestamp, hotel_name)

    archive_folder = site_folder / names["archive_folder"]
    site_folder.mkdir(parents=True, exist_ok=True)
    archive_folder.mkdir(parents=True, exist_ok=True)

    return {
        "site_folder": site_folder,
        "archive_path": archive_folder / names["archive_filename"],
        "clean_path": site_folder / names["clean_filename"],
        "timestamp": timestamp
    }
