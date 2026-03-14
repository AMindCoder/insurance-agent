# Demo Commands Log

## Git Clone - Checkout Repository
```bash
# Clone the insurance-agent repo into agent_demo folder
git clone https://github.com/Gr8Learning-2312/insurance-agent.git /path/to/agent_demo/insurance-agent-temp

# Move contents to agent_demo root and clean up temp folder
mv insurance-agent-temp/* insurance-agent-temp/.* /path/to/agent_demo/
rm -rf insurance-agent-temp
```

## Verify Cloned Contents
```bash
ls -la /Users/gauravchopra/work/code/workspace/customer/great_learning/agent_demo/
```

---

## Docker - Containerization

### Check Docker Version
```bash
docker --version
```

### Build Docker Image
```bash
docker build -t insurance-agent .
```

### Run Container with Environment File
```bash
docker run -d --name insurance-agent-test -p 8501:8501 --env-file .env insurance-agent
```
- `-d` : Run in detached (background) mode
- `--name insurance-agent-test` : Name the container
- `-p 8501:8501` : Map host port 8501 to container port 8501
- `--env-file .env` : Load environment variables from .env file

### Check Container Logs
```bash
docker logs insurance-agent-test
```

### Verify Container is Running
```bash
docker ps --filter "name=insurance-agent-test"
```

### Test App is Accessible
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8501
```

### Check Docker Image Size
```bash
docker images insurance-agent
```

### Stop and Remove Container (cleanup)
```bash
docker stop insurance-agent-test
docker rm insurance-agent-test
```

### Alternative: Run with Inline Environment Variables
```bash
docker run -d --name insurance-agent-test -p 8501:8501 \
  -e OPENAI_API_KEY="your-key-here" \
  -e OPENAI_BASE_URL="https://your-endpoint/v1" \
  insurance-agent
```

---

## Debugging - Docker Container Errors

### Issue: ChromaDB InvalidArgumentError with quoted .env values
**Error**: `chromadb.errors.InvalidArgumentError: Expected a name containing [a-zA-Z0-9._-]. Got: "insurance_policies"`

**Root Cause**: Docker `--env-file` passes quotes as literal characters. `CHROMA_COLLECTION="insurance_policies"` becomes `"insurance_policies"` (with quotes) inside the container.

**Fix**: Remove quotes from `.env` values:
```env
# WRONG (quotes become part of the value in Docker --env-file)
MODEL_NAME="gpt-4o-mini"
CHROMA_COLLECTION="insurance_policies"

# CORRECT
MODEL_NAME=gpt-4o-mini
CHROMA_COLLECTION=insurance_policies
```

### Restart Container After Fix
```bash
# Stop and remove old container
docker stop insurance-agent-test
docker rm insurance-agent-test

# Re-run with fixed .env
docker run -d --name insurance-agent-test -p 8501:8501 --env-file .env insurance-agent
```

### Tail Latest Logs
```bash
docker logs --tail 15 insurance-agent-test
```

---

## Docker Hub - Push Image

### Step 1: Login to Docker Hub

**Option A: Access Token (Recommended, required for 2FA)**
Generate a token at: Docker Hub > Account Settings > Security > Access Tokens
```bash
docker login -u <YOUR_DOCKERHUB_USERNAME>
# When prompted for password, paste the Access Token (not your password)
```

**Option B: Password (only works without 2FA)**
```bash
docker login -u <YOUR_DOCKERHUB_USERNAME>
# Enter your Docker Hub password when prompted
```

### Step 2: Tag the Image

**Tagging conventions:**
- `latest` — always points to the most recent build
- Semantic versioning (`v1.0.0`) — for release tracking

```bash
# Tag as latest
docker tag insurance-agent <YOUR_DOCKERHUB_USERNAME>/insurance-agent:latest

# Tag with semantic version
docker tag insurance-agent <YOUR_DOCKERHUB_USERNAME>/insurance-agent:v1.0.0
```

### Step 3: Push to Docker Hub
```bash
# Push latest tag
docker push <YOUR_DOCKERHUB_USERNAME>/insurance-agent:latest

# Push versioned tag
docker push <YOUR_DOCKERHUB_USERNAME>/insurance-agent:v1.0.0
```

### Step 4: Verify on Docker Hub
```bash
# List remote tags to confirm push
docker manifest inspect <YOUR_DOCKERHUB_USERNAME>/insurance-agent:latest
```
Or visit: `https://hub.docker.com/r/<YOUR_DOCKERHUB_USERNAME>/insurance-agent`

### Pull and Run from Docker Hub (on any machine)
```bash
docker pull <YOUR_DOCKERHUB_USERNAME>/insurance-agent:latest
docker run -d --name insurance-agent -p 8501:8501 --env-file .env <YOUR_DOCKERHUB_USERNAME>/insurance-agent:latest
```

---

## Streamlit Community Cloud - Deployment

**Note**: Vercel does not support Docker containers. Streamlit Cloud is purpose-built for Streamlit apps.

### Step 1: Login
- Go to https://share.streamlit.io
- Sign in with GitHub account (must have access to the repo)

### Step 2: Create New App
- Click **"New app"**
- Repository: `Gr8Learning-2312/insurance-agent`
- Branch: `main`
- Main file path: `app/main.py`

### Step 3: Add Secrets (Advanced Settings)
Expand "Advanced settings" and paste in **Secrets** (TOML format):
```toml
OPENAI_API_KEY = "your-api-key"
OPENAI_BASE_URL = "https://your-endpoint/v1"
MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHROMA_PERSIST_DIR = "./chroma_db"
CHROMA_COLLECTION = "insurance_policies"
POLICY_PDF_PATH = "./data/policy.pdf"
COVERAGE_CSV_PATH = "./data/coveragedata.csv"
```
Set Python version to `3.11`.

### Step 4: Deploy
- Click **Deploy** — app will be live at `https://<app-name>.streamlit.app`
