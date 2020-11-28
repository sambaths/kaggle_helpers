
import subprocess
import os
from time import time
import functools
from sklearn.model_selection import StratifiedKFold

from typing import Int, List, Dict, Optional, Tuple, Any,

def timer(function):
  '''
  function to time other functions
  '''
  @functools.wraps(function)
  def wrapper(*args, **kwargs):
    start = time()
    function(*args, **kwargs)
    end = time()
    print('Function ran in', round((end-start)/60, 2),'minutes.')
  return wrapper

@timer
def download_from_kaggle(comp_name, download_folder='input',print_bash_output=False):
  '''
  Use Kaggle API to download data from kaggle to specified folder
  Works only on Google Colab
  Download data from kaggle provide kaggle.json folder is already present in the working directory
  Works only in Linux based machines.
  Arguments:
  comp_name: Name of competition as in the kaggle-api command
  download_folder (optional): download location 
  print_bash_out (optional) : print output from bash command, default=False

  '''
  cwd = os.getcwd()
  cwd_files = os.listdir(cwd)
  if 'COLAB_GPU' in os.environ:
    if 'kaggle.json' not in cwd_files:
        print('Please upload your kaggle.json file to connect with Kaggle API !!')
        from google.colab import files
        files.upload()
        cwd_files = os.listdir(cwd)
  try:
      files = os.listdir(download_folder)
  except:
      files=[]
  assert 'kaggle.json' in cwd_files, ('Please place kaggle.json file in current working directory')
  if 'train.csv' not in files:
      bashCmds = ["pip uninstall -y kaggle", "pip install --upgrade pip", "pip install -q kaggle==1.5.6", "mkdir -p ~/.kaggle","cp kaggle.json ~/.kaggle/", "chmod 600 ~/.kaggle/kaggle.json",
      "mkdir input", f"kaggle competitions download -c {comp_name}", f"sudo unzip -q -n '*.zip' -d {download_folder}", "sudo rm *.zip"]
      for cmd in bashCmds:
        try:
          process = subprocess.run(cmd,shell=True, check=True, stdout=subprocess.PIPE)
        except:
          pass
        if print_bash_output:
            for out in process.stdout.decode('utf-8').split('\n'):
                print(out)

@timer
def create_kfold(df, target_column, n_folds: Optional = 5, save: Optional=False):
  df.loc[:, 'kfold'] = -1
  df = df.sample(frac=1).reset_index(drop=True)
  targets = df[target_column].values
  skf = StratifiedKFold(n_splits=n_folds)

  for f, (t_idx, v_idx) in enumerate(skf.split(X=df, y=targets)):
      df.loc[v_idx, 'kfold'] = int(f)

  df['kfold'] = df['kfold'].astype(int)
  if save:
    df.to_csv(f'{os.getcwd}/data_with_folds.csv', index=False)

  return df