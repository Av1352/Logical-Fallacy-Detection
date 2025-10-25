# 🧠 Logical Fallacy Detection

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered web application for detecting logical fallacies in text arguments. Built with Streamlit for an interactive, user-friendly experience.

## 🎯 Features

- **Real-time Analysis**: Instantly detect logical fallacies in any text
- **Multiple Fallacy Types**: Comprehensive coverage of common reasoning errors
- **Confidence Scoring**: Visual gauge showing prediction reliability
- **Educational Content**: Learn about each fallacy with examples
- **Analysis History**: Track and export your analyses
- **Responsive UI**: Professional, modern interface with interactive charts

## 🚀 Quick Start

### Installation

Clone the repository

```bash
git clone https://github.com/Av1352/Logical-Fallacy-Detection.git
cd Logical-Fallacy-Detection
```

Install dependencies

```bash
pip install -r requirements.txt
```


### Run the Application

```bash
streamlit run streamlit_app.py
```


The app will automatically open at `http://localhost:8501`

## 📊 Supported Fallacies

| Fallacy Type | Description |
|--------------|-------------|
| **Ad Hominem** | Attacking the person instead of the argument |
| **False Causality** | Assuming causation from correlation |
| **False Dilemma** | Presenting only two options when more exist |
| **Appeal to Emotion** | Using emotions instead of logic |
| **Faulty Generalization** | Drawing broad conclusions from limited data |
| **Ad Populum** | Claiming something is true because it's popular |
| **Circular Reasoning** | Using the conclusion as a premise |
| **Straw Man** | Misrepresenting an opponent's argument |

## 🎓 Use Cases

### Education
- **Critical Thinking Courses**: Teaching students to identify flawed reasoning
- **Debate Preparation**: Analyzing arguments for weaknesses
- **Writing Improvement**: Strengthening argumentative essays

### Professional
- **Content Review**: Checking articles for logical consistency
- **Argumentation Analysis**: Evaluating business proposals
- **Communication Training**: Improving reasoning skills

### Personal Development
- **Media Literacy**: Identifying fallacies in news and social media
- **Decision Making**: Recognizing flawed reasoning in everyday life

## 🏗️ Project Structure

```bash
Logical-Fallacy-Detection/
├── streamlit_app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── data/
│ └── final_data/ # Training datasets
│ ├── train.csv
│ ├── dev.csv
│ └── test.csv
└── code/ # Training scripts (optional)
├── bert.py
├── roberta.py
└── retriever.py
```


## 🔧 Configuration

The app includes configurable settings in the sidebar:

- **Confidence Threshold**: Adjust minimum confidence for predictions (0.0 - 1.0)
- **Analysis History**: Track all your analyses with exportable CSV


## 📈 Performance

| Metric | Value |
|--------|-------|
| Load Time | <2s |
| Analysis Speed | <100ms |
| UI Responsiveness | Excellent |
| Mobile Compatible | ✅ Yes |

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework for building data apps
- **Plotly** - Interactive visualization library
- **HuggingFace** - Transformer models and tools

## 📧 Contact

**Your Name**
- GitHub: [@Av1352](https://github.com/Av1352)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🔮 Future Enhancements

- [ ] Add support for 20+ additional fallacy types
- [ ] Integrate fine-tuned BERT/RoBERTa models
- [ ] Multi-language fallacy detection
- [ ] Batch text analysis from file upload
- [ ] REST API for programmatic access
- [ ] Chrome extension for real-time detection

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ and Python

[Report Bug](https://github.com/Av1352/Logical-Fallacy-Detection/issues) · [Request Feature](https://github.com/Av1352/Logical-Fallacy-Detection/issues)

</div>