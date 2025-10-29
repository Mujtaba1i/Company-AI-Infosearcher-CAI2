# COMPANY-AI-INFOSEARCHER-CAI2

*Empowering Insights Through Automated Global Company Profiles*

![last commit](https://img.shields.io/github/last-commit/Mujtaba1i/Company-AI-Infosearcher-CAI2)
![python](https://img.shields.io/badge/python-100%25-blue)
![languages](https://img.shields.io/badge/languages-1-orange)

**Built with the tools and technologies:**

![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Output Format](#output-format)
- [Performance](#performance)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**CAI2 (Company AI Infosearcher)** is an intelligent Python automation tool that leverages Google's Gemini AI to research and generate comprehensive company profiles. It processes lists of companies organized by country, providing detailed 200-character descriptions and relevant industry categorizations.

Perfect for:
- 📊 Market research and competitive analysis
- 🏢 Business intelligence gathering
- 🌍 Multi-country company profiling
- 📈 Investment research and due diligence

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Mujtaba1i/Company-AI-Infosearcher-CAI2.git
cd Company-AI-Infosearcher-CAI2
```

2. **Install required dependencies:**
```python
pip install google-genai
```

3. **Set up your API key:**

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

The script will automatically create this file with instructions if it doesn't exist.

### Usage

**Basic usage:**
```bash
python3 .\'Company AI Infosearcher CAI2.py' --file companies.txt
```

**Input file format:**
```
United States:
1- Company Name
2- Another Company

Canada:
1- Company Name
2- Another Company

```

**Help:**
```bash
python3 .\'Company AI Infosearcher CAI2.py' --help
```

---

## Features

### 🤖 Intelligent AI Processing
- Powered by **Google Gemini 2.5 Flash-Lite** for accurate, up-to-date company information
- Generates 200-character descriptions with comprehensive industry categorization
- Utilizes the latest web sources for current company data

### 🛡️ Robust Error Handling
- **Smart rate limiting:** 15 requests per minute with automatic 1-minute pauses
- **Retry mechanism:** Exponential backoff for failed requests (up to 3 attempts)
- **Request stability:** 2-second delay between requests to prevent throttling
- Detailed error logging and reporting

### 📊 Comprehensive Output
- Organized results by country with clear headers
- Execution metadata (start time, end time, duration, model used)
- Sequential numbering for easy reference
- UTF-8 encoding for international company names

### ⚡ Performance Optimized
- Processes ~100 companies in approximately 9 minutes
- Accurate ETA calculation based on request count
- Real-time progress tracking with company names
- Efficient sequential processing

---

## Configuration

Customize processing parameters in the `call_gemini_api_sequential()` function:
```python
sleep_after = 15        # Requests before rate limit pause
sleep_time = 60         # Rate limit pause duration (seconds)
request_delay = 2       # Delay between requests (seconds)
model = "gemini-2.5-flash-lite"  # Gemini model to use
max_retries = 3         # Maximum retry attempts
```

---

## Output Format

The script generates a detailed log file (`gemini_log.txt`) with the following structure:
```
============================================================
EXECUTION SUMMARY
============================================================
Start Time: 2025-10-29 14:30:15
End Time: 2025-10-29 14:42:06
Total Duration: 11 min 51.51 sec
Total Companies Processed: 100
Model Used: gemini-2.5-flash
============================================================

=== United States ===

1- Apple Inc. - Apple Inc. is a global technology leader designing and manufacturing consumer electronics, software, and online services, including iPhone, Mac, iPad, and innovative digital platforms. | [Technology, Consumer Electronics, Software, Digital Services, Hardware]

2- Microsoft Corporation - Microsoft Corporation: Global tech giant developing software, cloud computing, hardware, and AI solutions. Leader in operating systems, productivity software, and enterprise services. | [Technology, Software, Cloud Computing, Artificial Intelligence, Enterprise Services]

=== Canada ===

3- Air Canada - Air Canada: Canada's largest airline offering domestic and international passenger and cargo transportation services across six continents. | [Airlines, Transportation, Aviation, Cargo Services]
```

---

## Performance

**Benchmarks:**
- **Processing Speed:** ~1.5 seconds per API request
- **Total Time:** ~9 minutes for 100 companies (including rate limits)
- **Success Rate:** 99%+ with retry mechanism
- **Rate Limit Compliance:** Automatic handling of API quotas

**Timing Breakdown:**
```
API Response:     ~1.5s per request
Request Delay:    2.0s per request
Rate Limit Wait:  60s per 15 requests
Average:          ~3.5s per company + periodic pauses
```

---

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Ideas for contributions:**
- Multi-threading optimization
- Additional AI model support
- CSV/Excel input support
- JSON output format
- Web scraping fallback
- GUI interface

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Powered by [Google Gemini AI](https://ai.google.dev/)
- Built with Python 3
- Inspired by the need for automated business intelligence gathering

---

## Support

For issues, questions, or suggestions:
- 🐛 [Report a Bug](https://github.com/Mujtaba1i/Company-AI-Infosearcher-CAI2/issues)
- 💡 [Request a Feature](https://github.com/Mujtaba1i/Company-AI-Infosearcher-CAI2/issues)

---

**Note:** This tool requires a valid Google Gemini API key. Rate limits and costs apply according to your API plan. Always review generated content for accuracy before use in critical applications.

---

<p align="center">Made with ❤️ for researchers and analysts worldwide</p>
