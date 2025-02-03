# 🎲 FunNumberAPI 🎲

Welcome to the Number Classification API! This API takes a number as input and returns detailed mathematical properties, including whether the number is Armstrong, Perfect, Prime, Odd, or Even. It also computes the digit sum of the number. Additionally, it fetches fun facts about the number using the Numbers API, providing an engaging and informative experience

## Overview
The Number Classification API was built using Flask in Python. It classifies a number into various mathematical properties and retrieves fun facts using the Numbers API.

## 🌟 Features
- ✅ Identifies Armstrong, Perfect, Prime, Odd, Even numbers
- ✅ Computes the sum of digits
- ✅ Fetches fun facts about numbers
- ✅ Implements caching for efficiency
- ✅ Supports CORS for cross-origin requests
- ✅ Designed for fast response times (<500ms)

## 🚀 Deployment & Hosting
#### 🏗 Deployment to EC2
**Step 1: Launch EC2 Instance**
- Start an Ubuntu EC2 instance
- Open inbound rules for ports 22(SSH), 80(HTTP), and 5000(Custom TCP)
- Connect to your EC2 instance

**Step 2: Set Up Environment on EC2**
```
  sudo apt update && sudo apt upgrade -y #Update the System
  sudo apt install python3-pip nginx -y #Install Python and Pip
  python3 -m venv .venv #Create virtual environment
  source .venv/bin/activate #Activate virtual environment
  pip install flask gunicorn flask_cors requests # Install Flask and Required Dependencies
```
**Step 3: Clone & Run the App**
```
  git clone https://github.com/yourusername/FunNumberAPI.git
  cd FunNumberAPI
  python3 app.py
```
**Step 4. Deploy the Flask App with Gunicorn**
1. **Run the App with Gunicorn**:
   - Use Gunicorn to serve your Flask app:
      ```
      gunicorn --bind 0.0.0.0:5000 app:app
      ```
     Replace app:app with the name of your Flask app file and app instance (e.g., if your file is app.py and the Flask app is named app, use app:app)
2. **Test the App**:
   - Open a browser and go to http://<public-ip-of-ec2>:5000/api/classify-number?number=371.
   - You should see the JSON response from your API.
**Step 5: Set Up Systemd Service**:
1. **Create a Systemd Service File**
   To ensure your Flask app runs continuously and starts on boot, set up a systemd service.
    ```
      sudo nano /etc/systemd/system/flask-app.service
    ```
2. **Paste this**
    ```
    [Unit]
    Description=Gunicorn instance to serve Flask app
    After=network.target
    
    [Service]
    User=ubuntu
    WorkingDirectory=/home/ubuntu/FunNumberAPI
    ExecStart=/home/ubuntu/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    ```
    Then save with 'Ctrl+X' then y and enter
3. **Reload Systemd and Start the Service** 
```
  sudo systemctl daemon-reload
  sudo systemctl start flask-app
  sudo systemctl enable flask-app
```
4. **Check Status**
    ```
    sudo systemctl status flask-app
    ``` 
**Step 5. Set Up Nginx as a Reverse Proxy**
To make your app accessible on port 80 (HTTP) and improve performance, set up Nginx as a reverse proxy.
1. **Install NGINX**
    ```
    sudo apt install nginx -y
   ```
2. **Configure NGINX**
- Edit the default Nginx configuration file:
```
  sudo nano /etc/nginx/sites-available/default
```
Replace with:
```
server {
    listen 80;
    server_name <public-ip-of-ec2>;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
3. **Test and Restart NGINX**
    ```
      sudo nginx -t
      sudo systemctl restart nginx
    ```
4. **Test the App**
   - Open a browser and go to http://<public-ip-of-ec2>/api/classify-number?number=371.
   - You should see the JSON response from your API.
     
## 📡 API Usage

🔹 Endpoint:

GET /api/classify-number?number=<number>

**✅ Example Response (200 OK)**
```
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
``` 
**❌ Example Response (400 Bad Request)**
```
{
    "number": "not-a-number",
    "error": true,
    "message": "Input must be a valid integer"
}
```

## 📜 Project Structure
```
📂 FunNumberAPI
├── 📄 app.py          # Main Flask application
└── 📄 README.md       # This file 😎
```

## 🤝 Contributing
Feel free to fork this repo, make improvements, and submit a PR! 🛠️

## 👑 Author
👤 Oluwademilade Oyekanmi
🔗 [GitHub](https://github.com/MsOluwademilade)
📧 oyekanmidemilade2@gmail.com

## 🏆 Acknowledgements
- Flask for making Python APIs a breeze 🍃
- [Numbers API]( http://numbersapi.com) for the fun facts 🔢
- You, for checking out this project! 🎉
