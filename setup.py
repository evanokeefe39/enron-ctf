import kagglehub

import shutil

# TODO: upload custom dataset, figure out why binary when csv gets downloaded
path = kagglehub.dataset_download(
  
  "wcukierski/enron-email-dataset",
  path="emails.csv",
 
)

print(f"downloaded {path}")

# shutil.move(path, "./sample_data/emails.csv")
