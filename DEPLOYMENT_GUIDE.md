# Deploying to Streamlit Community Cloud

This guide outlines the steps to deploy your **AI Grant Architect** application to Streamlit Community Cloud.

## 1. Secrets Management

Since Streamlit apps are public repositories, **NEVER** hardcode API keys in your code. We have updated the application to use `st.secrets` instead.

### How it works
In `modules/image_generator.py`, we replaced:
```python
api_key = os.environ.get("GOOGLE_API_KEY")
```
with:
```python
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    # Error handling...
```
This tells Streamlit to look for a secure configuration variable named `GOOGLE_API_KEY`.

### Setting up Secrets on Streamlit Cloud
When you deploy your app, you will need to provide your actual API key in the Streamlit dashboard:
1.  Go to your app dashboard.
2.  Click on **App Settings** (three dots) -> **Settings**.
3.  Go to the **Secrets** tab.
4.  Paste your TOML-formatted secrets into the text area:
    ```toml
    GOOGLE_API_KEY = "your-actual-google-api-key-here"
    ```
5.  Click **Save**.

## 2. Configuration Files (Prepared)
We have already created the necessary files for a smooth deployment:
-   `requirements.txt`: Lists all Python dependencies (Streamlit, Google Generative AI, Pillow, etc.).
-   `.gitignore`: Ensures sensitive files (like `.env` or local secrets) are **never** uploaded to GitHub.

## 3. Deployment Checklist

Follow these steps to launch your app:

### Step 1: Push to GitHub
1.  Initialize a git repository (if you haven't already):
    ```bash
    git init
    git add .
    git commit -m "Initial commit for Streamlit deployment"
    ```
2.  Create a new specific repository on GitHub.
3.  Push your local code to the new repository:
    ```bash
    git remote add origin <your-repo-url>
    git push -u origin main
    ```

### Step 2: Connect to Streamlit Community Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **New app**.
3.  Select your GitHub repository (`<your-username>/<repo-name>`).
4.  Select the branch (usually `main`).
5.  **Main file path**: Ensure this is set to `app.py`.

### Step 3: Configure Secrets & Launch
1.  Before clicking "Deploy", click on **Advanced settings**.
2.  In the **Secrets** field, paste your API key as described in Section 1.
3.  Click **Save**.
4.  Click **Deploy!**

Your app should now be live! Streamlit will install the dependencies from `requirements.txt` and launch the application.
