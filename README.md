# Fragfrag Perfume Recognition API

A FastAPI-based backend that uses Google Gemini AI to identify perfume bottles from images. The project includes an automated scraper for importing perfume data into Supabase.

## 🚀 Tech Stack

- **Backend**: FastAPI (Python 3.11/3.12)
- **AI Service**: Google Gemini 1.5 Flash
- **Database**: Supabase
- **Deployment**: Fly.io
- **Automation**: GitHub Actions

## 🛠 Local Development

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   AI_API_KEY=your_gemini_api_key
   ```

3. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🚢 Backend Deployment (Fly.io)

The backend is hosted on Fly.io under the app name `fragy-api`.

### Automated Deployment
Deployment is fully automated via GitHub Actions. Any push to the `main` branch triggers the `.github/workflows/fly-deploy.yml` workflow, which builds the Docker image and deploys it to Fly.io.

### Manual Deployment
If you have `flyctl` installed, you can deploy manually:
```bash
fly deploy
```

### Managing Production Secrets
Since `.env` is not committed, you must set production secrets directly in Fly.io:
```bash
fly secrets set AI_API_KEY=your_key SUPABASE_KEY=your_key
```

## 🕷 Scraper & Importer (GitHub Actions)

The project includes a standalone scraper (`importer.py`) that populates the database.

### Scheduled Execution
A GitHub Action workflow (`.github/workflows/importer.yml`) runs the scraper as a **cron job** every day at **3:00 AM UTC**.

### Manual Execution
You can trigger the scraper manually at any time:
1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Perfume Importer Cron** workflow.
3. Click **Run workflow**.

### Scraper Configuration
The scraper requires the following **GitHub Repository Secrets**:
- `SUPABASE_URL`
- `SUPABASE_KEY`

## 📁 Project Structure

- `app/`: FastAPI application source code.
- `importer.py`: The scraper script.
- `Dockerfile`: Production container configuration.
- `fly.toml`: Fly.io deployment settings.
- `.github/workflows/`:
  - `fly-deploy.yml`: Backend CI/CD.
  - `importer.yml`: Scraper cron job.
