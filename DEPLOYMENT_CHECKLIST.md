# Deployment Checklist: Manual Upload (No Git Required)

Since you don't have Git installed, we will upload the files manually to GitHub.

## 1. Create a GitHub Repository

1.  Go to [GitHub.com](https://github.com/new) and log in.
2.  Create a **New Repository**.
3.  **Repository Name**: `ai-grant-architect`.
4.  **Public/Private**: Public is fine (Streamlit Cloud works with both).
5.  **Initialize with a README**: Check this box (makes it easier to upload files).
6.  Click **Create repository**.

## 2. Upload Your Files

1.  In your new repository, click the **Add file** button -> **Upload files**.
2.  Open your project folder on your computer: `Desktop\ANTIGRAVITY PROJECTS\AI_Grant_Architect`.
3.  **Select all files and folders** EXCEPT:
    *   `venv` folder (Do NOT upload this)
    *   `.streamlit` folder (Do NOT upload this)
    *   `__pycache__` folder (Do NOT upload this)
4.  **Drag and drop** the selected files into the GitHub page.
    *   Ensure `requirements.txt`, `app.py`, and the `modules` folder are included.
5.  Scroll down to "Commit changes".
6.  Message: "Initial upload".
7.  Click **Commit changes**.

## 3. Deploy on Streamlit Cloud

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **New app**.
3.  **Repository**: Select your new repository (`YourUsername/ai-grant-architect`).
4.  **Branch**: `main` (or `master`).
5.  **Main file path**: `app.py`.
6.  **DO NOT click "Deploy" yet!**

## 4. Configure Secrets (CRITICAL)

Your app needs the `GOOGLE_API_KEY` to work.

1.  Click on **Advanced settings**.
2.  Find the field labeled **Secrets**.
3.  Paste the following (replacing with your actual key):

```toml
GOOGLE_API_KEY = "AIzaSyAjsjzIdfodIS1ZUqNfQEpdRQ_X89-yfNg"
```

4.  Click **Save**.
5.  **NOW** click **Deploy!**

## Optional: Install Git for Future Use

If you want to use the command line in the future, download and install Git from:
[https://git-scm.com/download/win](https://git-scm.com/download/win)
