# GitHub setup

Recommended repository name:

```text
prompt-experiment-platform
```

Create an empty repository, then run inside this project folder:

```powershell
git init
git branch -M main
git add .
git commit -m "feat: launch Prompt Experiment Platform"
git remote add origin https://github.com/abdullahijaz5961/prompt-experiment-platform.git
git push -u origin main
```

After editing directly on GitHub, synchronise the local copy before the next push:

```powershell
git pull origin main
```

Never commit `.env`, private documents, credentials, model weights, or customer production data.
