from pathlib import Path
import subprocess
import logging

# ====================
# Configuration
# Values in this section are safe to change without touching logic
# ====================
RCLONE_PATH = r"C:\Tools\rclone.exe"

ZIP_FILE = Path(r"C:\VM-Exports\hyperv-ubuntu-db-learning_2024-archive.zip")

REMOTE = "gdrive-archive:VM-Archives"

DRY_RUN = True # Safety switch: prevents actual upload

LOG_FILE = r"C:\VM-Exports\vm_archive_upload.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def validate_zip_file():
    """
    Ensure the VM archive exists before attempting any upload.
    Fails fast to avoid silent errors in automation.
    """
    if not ZIP_FILE.exists():
        raise FileNotFoundError(
            f"ZIP archive not found at: {ZIP_FILE}"
        )

    logging.info(f"ZIP file found: {ZIP_FILE}")

def build_rclone_command():
    """
    Build the rclone command used to upload VM archive.
    Returns the command as a list, ready to be executed.
    """

    command = [
        RCLONE_PATH,
        "copy",
        str(ZIP_FILE),
        REMOTE,
        "--progress",
    ]
    if DRY_RUN:
        command.append("--dry-run")
    
    return command

if __name__=="__main__":
    logging.info("=== VM archive upload job started ===")
    
    validate_zip_file()

    command = build_rclone_command()

    logging.info("Rclone command to be executed:")
    logging.info(" ".join(command))

    subprocess.run(command, check=True)
try:
    subprocess.run(command, check=True)
    logging.info("Rclone command completed successfully")
    logging.info("=== VM archive upload job finished ===")
except subprocess .CalledProcessError as error:
    logging.error("Rclone command failed")
    logging.error(str(error))
    raise