import os
import logging

home_dir = os.path.expanduser('~')
log_folder = f'{home_dir}/.trasba/log'
log_file = f'{log_folder}/mail2print'
os.makedirs(log_folder, exist_ok=True)

# Configure logging globally (assumes no prior logging setup in other files)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=log_file
)

# Create a single logger instance with desired configuration
logger = logging.getLogger('mail2print')