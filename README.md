![](https://i.imgur.com/UtR64IU.png)
This tool analyses the emotional sentiment of posts posted to the social media platform Bluesky https://bsky.app/

Posts can be searched via a user handle or by search term. Up to 100 posts can be retrieved at any time. Supports both 'Top' and 'Latest" search modes.

![](https://i.imgur.com/7NJNVqK.png)
 
 ## **Installation**  
### **1. Prerequisites:**  
Python 3.9+
  
### **2. Clone the Repo**  
 ```bash  
 git clone https://github.com/Mozochi/bluesky-sentiment-analyser.git
```  
  
### **3. Create Virtual Environment (Recommended):**  
```bash  
python -m venv venv  
  
### Activate (Linux/macOS)  
source venv/bin/activate 
### Activate (Windows - Git Bash/WSL)  
source venv/Scripts/activate
### Activate (Windows - Cmd/PowerShell)  
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
  
This project uses the Sentiment Analysis Dataset (https://www.kaggle.com/datasets/abhi8923shriv/sentiment-analysis-dataset) by Abhishek Shrivastava. Please cite their work if you use the dataset.  
Built using Gradio (https://www.gradio.app/).

## **Credits**

Ben Whiting, Josh Exton, Joshua Thomas, Lewis Jones, Millie Green 

To reach out, please email Joshua Thomas at [28005766@students.lincoln.ac.uk](mailto:28005766@students.lincoln.ac.uk) or Lewis Jones at [27668320@students.lincoln.ac.uk](mailto:27668320@students.lincoln.ac.uk)

## **License**
[MIT](https://choosealicense.com/licenses/mit/)
