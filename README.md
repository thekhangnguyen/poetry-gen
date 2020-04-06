# Run web app with fine-tuned GPT-2 model
Setup virtual environment (optional) and install requirements:
``` 
virtualenv --system-site-packages -p python3 venv
source env/bin/activate
venv/bin/pip3 install -r requirements.txt
```

Download [this folder](https://drive.google.com/open?id=12SJMB-dT5Cp-psRH2n9CsbzDS85L1GzD) and copy to `webapp/gpt2/models/355M`:

Run the web application: 
```
python webapp/app.py
```
# Fine-tune GPT-2 from the beginning

# UKP model
Slight modification:
- Save_and_load.py: only for loading trained model (for further training)

    command: `python3 Save_and_Load.py [model_name]`
    
- RunModel_CoNLL_Format.py: add third parameter to specify the directory of the output file

    command: `python3 RunModel_CoNLL_Format.py [model_name] [conll_file] [stored_location]`
