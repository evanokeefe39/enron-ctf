import kagglehub

import shutil

# Load the latest version
path = kagglehub.dataset_download(
  
  "wcukierski/enron-email-dataset",
  path="emails.csv",
 
)

shutil.move(path, "./sample_data/emails.csv")


