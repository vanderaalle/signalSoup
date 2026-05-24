# Publishing Signal Soup to GitHub - Quick Guide

## Files Ready for Publication

All files have been prepared and are ready to publish:

- ✅ **signalSoup.py** - Your main code module
- ✅ **README.md** - Comprehensive documentation emphasizing semiotic foundations
- ✅ **LICENSE** - MIT License
- ✅ **requirements.txt** - Python dependencies (graphviz)
- ✅ **.gitignore** - Ignores common Python temporary files
- ✅ **example.py** - Usage demonstrations
- ✅ **setup.py** - For pip installation

## Steps to Publish

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `signal-soup`
3. Description: "A computational model exploring emergent communication through semiotic sign functions"
4. Choose: **Public** (so others can use it)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### 2. Upload Files

**Option A: Using GitHub Web Interface** (easiest)
1. On your new repository page, click **uploading an existing file**
2. Drag and drop all the files listed above
3. Commit message: "Initial commit"
4. Click **Commit changes**

**Option B: Using Git Command Line**
```bash
# In the directory with your files
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/vanderaalle/signal-soup.git
git push -u origin main
```

### 3. You're All Set!

All your contact information has been added:
- ✅ Email: andrea.valle@unito.it
- ✅ GitHub: vanderaalle
- ✅ Institution: University of Turin

The files are ready to publish as-is. You can still update the citation in README.md later when your EVOLANG paper is officially published.

### 4. Optional Enhancements

**Add Topics** (helps people find your repo):
- On your repo page, click the gear icon next to "About"
- Add topics: `multi-agent-systems`, `semiotics`, `emergence`, `communication`, `python`, `language-evolution`

**Enable Discussions** (optional):
- Go to repo Settings → Features
- Check "Discussions"

**Add GitHub Actions** for testing (advanced, optional)

## Using the Published Code

Once published, users can install with:

```bash
# Clone the repository
git clone https://github.com/vanderaalle/signal-soup.git
cd signal-soup

# Install dependencies
pip install -r requirements.txt

# Run example
python example.py
```

Or for development:
```bash
pip install -e .
```

## Next Steps

1. **Test locally** - Run `example.py` to make sure everything works
2. **Publish to GitHub** - Follow steps above  
3. **Share** - Tweet, email, or share with colleagues
4. **Submit to PyPI** (optional) - Makes it installable via `pip install signal-soup`

## Optional: Publishing to PyPI

If you want to make it pip-installable:

1. Create account at https://pypi.org/
2. Install twine: `pip install twine`
3. Build distribution:
   ```bash
   python setup.py sdist bdist_wheel
   ```
4. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

Then anyone can install with:
```bash
pip install signal-soup
```

## Questions?

If you need help with any step, just let me know!

---

**Important**: Before publishing, make sure you've:
- ✅ Tested the code works (`python example.py`)
- ✅ Updated placeholder text (email, URLs, etc.)
- ✅ Reviewed the README for accuracy
- ✅ Verified the license (MIT is good for academic code)
