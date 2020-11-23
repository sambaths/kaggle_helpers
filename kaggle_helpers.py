
import subprocess
import os


def download_from_kaggle(comp_name, print_bash_output=False):
  '''
  Works only on Colab
  Download data from kaggle
  '''
  if 'COLAB_GPU' in os.environ:
    files = os.listdir()
    if 'kaggle.json' not in files:
        print('Please upload your kaggle.json file to connect with Kaggle API !!')
        from google.colab import files
        files.upload()
    try:
        files = os.listdir('input/')
    except:
        files=[]
    if 'train.csv' not in files:
        bashCmds = ["pip uninstall -y kaggle", "pip install --upgrade pip", "pip install -q kaggle==1.5.6", "mkdir -p ~/.kaggle","cp kaggle.json ~/.kaggle/", "chmod 600 ~/.kaggle/kaggle.json",
        "mkdir input", "kaggle competitions download -c comp_name", "sudo unzip -q -n '*.zip' -d 'input/'", "sudo rm *.zip"]
        for cmd in bashCmds:
          if 'comp_name' not in cmd:
            try:
              process = subprocess.run(cmd,shell=True, check=True, stdout=subprocess.PIPE)
            except:
              pass
          else:
            cmd = f"kaggle competitions download {comp_name}"
            process = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
          if print_bash_output:
              for out in process.stdout.decode('utf-8').split('\n'):
                  print(out)

