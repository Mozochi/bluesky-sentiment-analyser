![](https://raw.githubusercontent.com/Mozochi/sentiment-analysis-TSE-Project/refs/heads/master/github-header-image.png?token=GHSAT0AAAAAADDK6BSSNLTVFYIMOGOHYMZ62A34PNQ)
This tool analyses the emotional sentiment of posts posted to the social media platform Bluesky https://bsky.app/

Posts can be searched via a user handle or by search term. Up to 100 posts can be retrieved at any time. Supports both 'Top' and 'Latest" search modes.

![](https://raw.githubusercontent.com/Mozochi/sentiment-analysis-TSE-Project/refs/heads/master/app-screencapture.png?token=GHSAT0AAAAAADDK6BSTVGWMBY4DGMWHTXGA2A334WQ)
 
 ## **Installation**  
### **1. Prerequisites:**  
Python 3.9+
  
### **2. Clone the Repo**  
 ```bash  
 git clone https://github.com/Mozochi/sentiment-analysis-TSE-Project.git  
```  
  
### **3. Create Virtual Environment (Recommended):**  
```bash  
python -m venv venv  
  
### Activate (Linux/macOS)  
```bash  
source venv/bin/activate```  
### Activate (Windows - Git Bash/WSL)  
```bash  
source venv/Scripts/activate```  
### Activate (Windows - Cmd/PowerShell)  
```bash  
.\venv\Scripts\activate  
```  
  
### **4. Install Dependencies**  
```bash  
pip install -r requirements.txt  
```

### **5. Access Bluesky API**  

 1. Make an account on Bluesky at https://bsky.app/. Ensure it is email verified.
 2. Make a new Bluesky app password at https://bsky.app/settings/app-passwords.
 3. Create a .env file at the root directory of the project in the format below
 ```  
IDENTIFIER="YOUR_BLUESKY_HANDLE"  
PASSWORD="YOUR_APP_PASSWORD"  
```

  
### **5. Data (For model training)**  
https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis?resource=download  

  
## **Usage**  
```bash  
python main.py
```  
  
## **Acknowledgements**  
  
This project uses the Twitter Sentiment Analysis dataset (https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis?resource=download) by passionate-nlp. Please cite their work if you use the dataset.  
Built using Gradio (https://www.gradio.app/).

## **Credits**

Ben Whiting 
Josh Exton
Joshua Thomas
Lewis Jones 
Millie Green 
