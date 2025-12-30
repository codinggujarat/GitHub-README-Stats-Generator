# GitHub README Stats Generator

A production-ready web application to generate dynamic GitHub stats for your profile README.

## Features
- **Dynamic Stats**: Fetches real-time data from GitHub API.
- **Custom Themes**: Choose between Dark, Light, Neon, and Glass styles.
- **Live Preview**: See how it looks before copying.
- **Production Ready**: Scalable Flask backend + React frontend.

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python Flask, Requests, SVGWrite
- **Deployment**: Ready for Vercel (Frontend) and Render (Backend)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- GitHub Personal Access Token

### Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file (copy example or create new):
   ```env
   GITHUB_TOKEN=your_github_token_here
   PORT=5000
   ```
4. Run the server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Deployment
- **Frontend**: Run `npm run build` and deploy the `dist/` folder to Vercel/Netlify.
- **Backend**: Push to GitHub and connect to Render/Railway. Set `GITHUB_TOKEN` in your cloud provider's environment variables.

## License
MIT
