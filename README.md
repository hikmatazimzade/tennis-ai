# Tennis AI 🎾

A machine learning-powered tennis match prediction system that analyzes player statistics, historical performance, and match conditions to predict match outcomes with confidence scores.

## 🎥 Demo Video
https://github.com/user-attachments/assets/74e32a06-c6bf-44c8-b873-169983571883

## 🚀 Features

- **Advanced ML Models**: Three trained models (CatBoost, XGBoost, Random Forest) for accurate match predictions
- **Player Database**: Comprehensive player statistics and historical data
- **Smart Search**: Find players by name or country code
- **Prediction Interface**: Get match predictions with confidence scores and winning odds
- **Modern Web Interface**: Clean, responsive design built with SvelteKit
- **REST API**: FastAPI backend with comprehensive endpoints

## 🤖 Model Performance

The system uses three different machine learning models, with CatBoost as the default:

| Model | Accuracy | ROC AUC | Log Loss |
|-------|----------|---------|----------|
| **CatBoost** (Default) | 67.21% | 0.73 | 0.60     |
| XGBoost | 66.70% | 0.73 | 0.61     |
| Random Forest | 65.70% | 0.72 | 0.62     |

## 📊 Feature Engineering

The models are trained on 137 carefully engineered features including:

- **Player Characteristics**: Entry type, playing hand, physical attributes
- **Match Context**: Tournament level, surface type, date, draw size
- **Performance Metrics**: Aces, double faults, service statistics
- **Historical Data**: Head-to-head records, recent form (last 5, 10, 20, 50 matches)
- **Ranking & Elo**: Current rankings, Elo ratings, surface-specific performance
- **Comparative Analysis**: Differential features between players

## Feature Correlation Analysis
![Correlation Matrix](images/Correlation%20Matrix.png)

## 🛠️ Tech Stack

**Backend:**
- FastAPI with Pydantic for data validation
- Python 3.11 with ML libraries (CatBoost, XGBoost, scikit-learn)
- UV for dependency management

**Frontend:**
- SvelteKit for modern, reactive UI
- Responsive design for all devices

**Deployment:**
- Docker & Docker Compose for containerization
- Hot-reload development environment

## 📡 API Endpoints

- `POST /prediction` - Get match prediction with confidence scores
- `GET /players` - Retrieve all players data
- `GET /players/{player_id}` - Get specific player information
- `GET /players-lookup` - Search players by name or country code

## 🚀 Getting Started

### Prerequisites

This project uses Git LFS (Large File Storage) for dataset files. You'll need to install and configure Git LFS:

```bash
# Install Git LFS (if not already installed)
# On macOS with Homebrew:
brew install git-lfs

# On Ubuntu/Debian:
sudo apt-get install git-lfs

# On Windows, download from: https://git-lfs.github.io/

# Initialize Git LFS
git lfs install
```

### Option 1: Docker (Recommended)

1. **Clone the repository and pull LFS files**
   ```bash
   git clone https://github.com/hikmatazimzade/tennis-ai.git
   cd tennis-ai
   git lfs pull
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. **Clone the repository and pull LFS files**
   ```bash
   git clone https://github.com/hikmatazimzade/tennis-ai.git
   cd tennis-ai
   git lfs pull
   ```

2. **Backend Setup**
   ```bash
   # Install UV (if not already installed)
   pip install uv
   
   # Install dependencies
   uv sync
   
   # Run the backend
   uv run uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Frontend Setup**
   ```bash
   cd ui-app
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## 💡 How to Use

1. **Browse Players**: Visit the players page to explore the database of tennis players
2. **Search Players**: Use the search functionality to find specific players by name or country
3. **View Player Details**: Click on any player to see their detailed statistics and performance history
4. **Make Predictions**: Go to the prediction page, select two players, and get AI-powered match predictions with confidence scores

## 🤝 Contributing

All contributions are welcome! Whether it's improving the ML models, adding new features, or enhancing the UI, your input is valuable.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.