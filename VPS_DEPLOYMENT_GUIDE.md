# Deploying to a Linux VPS (Ubuntu/CentOS)

This guide walks you through setting up the **AI Grant Architect** on a Linux server using `systemd` and Nginx.

## 1. Prerequisites

Ensure your server matches these requirements:
*   **OS**: Ubuntu 22.04 LTS (recommended) or CentOS 8+
*   **Python**: Python 3.9+ installed
*   **Root Access**: Ability to run `sudo` commands.

## 2. Server Setup & Installation

### Step 1: Clone the Repository
Connect to your VPS and clone your project to `/var/www/grant_architect` (or your preferred location).
```bash
cd /var/www
git clone <your-repo-url> grant_architect
cd grant_architect
```

### Step 2: Create Virtual Environment
Create a virtual environment to isolate dependencies.
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required Python packages.
```bash
pip install -r requirements.txt
```

### Step 4: Test Manually
Use the `run.sh` script to verify the app starts correctly.
```bash
chmod +x run.sh
./run.sh
```
*Note: Make sure port 8501 is open in your firewall (`ufw allow 8501`) if you want to test accessing it directly via IP.*
Press `Ctrl+C` to stop the test.

## 3. Configure Systemd Service (Keep-Alive)

To ensure the app runs in the background and restarts automatically:

1.  **Edit the Service File**:
    Open `grant_architect.service` and update the paths if necessary.
    *   Set `User` to your non-root user if desired.
    *   Set `GOOGLE_API_KEY` to your actual API key.
    *   Verify `WorkingDirectory` and `ExecStart` paths match your installation.

2.  **Move & Enable Service**:
    ```bash
    sudo cp grant_architect.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable grant_architect
    sudo systemctl start grant_architect
    ```

3.  **Check Status**:
    ```bash
    sudo systemctl status grant_architect
    ```

## 4. setup Nginx Reverse Proxy

To access your app via domain (e.g., `http://mydomain.com`) instead of port 8501:

1.  **Install Nginx**:
    ```bash
    sudo apt install nginx  # Ubuntu
    # OR
    sudo yum install nginx  # CentOS
    ```

2.  **Create Configuration**:
    Create a new file `/etc/nginx/sites-available/grant_architect`:
    ```nginx
    server {
        listen 80;
        server_name mydomain.com www.mydomain.com;  # REPLACE with your actual domain

        location / {
            proxy_pass http://127.0.0.1:8501;
            proxy_http_version 1.1;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
        }

        # Optional: serve static assets directly if needed, but Streamlit handles this well usually.
    }
    ```

3.  **Enable Configuration (Ubuntu)**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/grant_architect /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default  # Optional: remove default site
    ```

4.  **Test & Restart**:
    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

Your app should now be accessible at `http://mydomain.com`!
