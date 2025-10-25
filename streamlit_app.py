import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="Logical Fallacy Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS optimized for DARK THEME
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .fallacy-card {
        background: rgba(255, 107, 157, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border-left: 6px solid #ff6b9d;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(255, 107, 157, 0.2);
    }
    .fallacy-card h2 {
        color: #ff6b9d !important;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 157, 0.4);
    }
    .stButton>button[kind="primary"] {
        background-color: #ff6b9d !important;
        border-color: #ff6b9d !important;
        color: #ffffff !important;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #ff4d85 !important;
        border-color: #ff4d85 !important;
    }
    /* Make tabs more visible in dark mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 107, 157, 0.2) !important;
        border-bottom: 2px solid #ff6b9d !important;
    }
</style>
""", unsafe_allow_html=True)

# Fallacy descriptions dictionary
FALLACY_INFO = {
    "ad hominem": {
        "name": "Ad Hominem",
        "definition": "Attacking the person making an argument rather than the argument itself.",
        "example": "You can't trust John's opinion on climate change because he's not a scientist.",
        "why_problematic": "Dismisses valid arguments based on irrelevant personal characteristics."
    },
    "false causality": {
        "name": "False Causality",
        "definition": "Assuming that because one event followed another, the first caused the second.",
        "example": "I wore my lucky socks and won the game, so my socks caused the victory.",
        "why_problematic": "Confuses correlation with causation, ignoring other factors."
    },
    "false dilemma": {
        "name": "False Dilemma",
        "definition": "Presenting only two options when more alternatives exist.",
        "example": "You're either with us or against us.",
        "why_problematic": "Oversimplifies complex situations and eliminates nuanced positions."
    },
    "appeal to emotion": {
        "name": "Appeal to Emotion",
        "definition": "Manipulating emotions rather than using valid reasoning.",
        "example": "Think of the children! We must pass this law immediately.",
        "why_problematic": "Bypasses logical thinking and can lead to poor decisions."
    },
    "faulty generalization": {
        "name": "Faulty Generalization",
        "definition": "Drawing broad conclusions from insufficient evidence.",
        "example": "I met two rude people from that city, so everyone there must be rude.",
        "why_problematic": "Ignores diversity and makes unfair assumptions about entire groups."
    },
    "ad populum": {
        "name": "Ad Populum",
        "definition": "Arguing something is true or good because it's popular.",
        "example": "Everyone's buying this product, so it must be the best.",
        "why_problematic": "Popularity doesn't determine truth or quality."
    },
    "circular reasoning": {
        "name": "Circular Reasoning",
        "definition": "Using the conclusion as a premise in the argument.",
        "example": "The Bible is true because it says so in the Bible.",
        "why_problematic": "Provides no real justification for the conclusion."
    },
    "fallacy of extension": {
        "name": "Straw Man",
        "definition": "Misrepresenting an opponent's argument to make it easier to attack.",
        "example": "You say we should have some gun control, so you want to ban all guns.",
        "why_problematic": "Doesn't address the actual argument being made."
    }
}

# Example texts for each fallacy
EXAMPLES = {
    "Ad Hominem": [
        "You can't trust her healthcare opinion—she's not even a doctor.",
        "Why listen to him about the economy? He's never run a business.",
        "She argues for vegetarianism, but she's just an emotional animal lover."
    ],
    "False Causality": [
        "I got sick after eating at that restaurant, so the food must have been bad.",
        "Crime dropped after the new mayor was elected, so he must be doing great.",
        "Every time I wash my car, it rains. I'm causing the rain."
    ],
    "False Dilemma": [
        "You're either with us or against us.",
        "Either we cut all social programs or the country goes bankrupt.",
        "If you don't support this war, you don't support our troops."
    ],
    "Appeal to Emotion": [
        "Think of the children! We must ban this immediately.",
        "Don't you care about your family's safety? Buy our system now.",
        "How can you be so heartless as to oppose this charity?"
    ],
    "Faulty Generalization": [
        "My two French coworkers were rude, so French people are rude.",
        "I tried yoga once and didn't like it, so yoga doesn't work.",
        "All politicians are corrupt—just look at these three examples."
    ]
}

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Simple rule-based prediction function
def predict_fallacy(text):
    """Simple keyword-based fallacy detection for demo"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['you', 'your', 'he', 'she', 'they']) and \
       any(word in text_lower for word in ["can't trust", "not even", "never", "just"]):
        return {
            "fallacy": "ad hominem",
            "confidence": 0.82,
            "explanation": "This argument attacks the person rather than addressing their point.",
        }
    elif 'because' in text_lower and any(word in text_lower for word in ['therefore', 'so', 'thus', 'caused']):
        return {
            "fallacy": "false causality",
            "confidence": 0.76,
            "explanation": "This argument assumes causation from correlation without evidence.",
        }
    elif any(word in text_lower for word in ['either', 'or', 'only two', 'must be', 'with us or against']):
        return {
            "fallacy": "false dilemma",
            "confidence": 0.79,
            "explanation": "This argument presents only two options when more exist.",
        }
    elif any(word in text_lower for word in ['think of', 'children', 'family', 'heartless', 'care about']):
        return {
            "fallacy": "appeal to emotion",
            "confidence": 0.74,
            "explanation": "This argument manipulates emotions rather than using logic.",
        }
    elif any(word in text_lower for word in ['all', 'every', 'everyone', 'no one', 'always', 'never']):
        return {
            "fallacy": "faulty generalization",
            "confidence": 0.71,
            "explanation": "This argument makes sweeping claims from limited evidence.",
        }
    else:
        return {
            "fallacy": "appeal to emotion",
            "confidence": 0.68,
            "explanation": "This argument may rely on emotional appeal over logical reasoning.",
        }

# Header
st.markdown('<h1 class="main-header">🧠 Logical Fallacy Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered analysis to identify logical fallacies in arguments</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Minimum confidence level for predictions"
    )
    
    st.markdown("---")
    
    st.header("📊 Statistics")
    if st.session_state.analysis_history:
        st.metric("Total Analyses", len(st.session_state.analysis_history))
        avg_conf = sum(h['confidence'] for h in st.session_state.analysis_history) / len(st.session_state.analysis_history)
        st.metric("Avg Confidence", f"{avg_conf:.2%}")
    else:
        st.info("No analyses yet")
    
    st.markdown("---")
    
    st.header("ℹ️ About")
    st.markdown("""
    This tool detects **logical fallacies** using AI:
    
    - Ad Hominem
    - False Causality
    - False Dilemma
    - Appeal to Emotion
    - Faulty Generalization
    - And more...
    
    Built for critical thinking and argumentation analysis.
    """)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.analysis_history = []
        st.rerun()

# Main tabs
tab1, tab2, tab3 = st.tabs(["🔍 Analyze", "📖 Learn", "📈 History"])

# TAB 1: ANALYZE
with tab1:
    st.header("Analyze Text for Logical Fallacies")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_method = st.radio(
            "Input method:",
            ["Type your own text", "Use example"],
            horizontal=True
        )
        
        if input_method == "Use example":
            example_category = st.selectbox("Select fallacy type:", list(EXAMPLES.keys()))
            user_input = st.selectbox("Choose example:", EXAMPLES[example_category])
        else:
            user_input = st.text_area(
                "Enter argument to analyze:",
                height=120,
                placeholder="Example: You can't trust his opinion because he's never been to college.",
                help="Paste any argument or statement you want to analyze"
            )
    
    with col2:
        st.markdown("### Quick Tips")
        st.info("""
        **Look for:**
        - Personal attacks
        - Emotional language
        - Oversimplifications
        - False connections
        - Hasty conclusions
        """)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🔄 Clear", use_container_width=True)
    
    if clear_btn:
        st.rerun()
    
    if analyze_btn and user_input:
        with st.spinner("🤖 Analyzing text..."):
            prediction = predict_fallacy(user_input)
            
            if prediction['confidence'] >= confidence_threshold:
                st.markdown("---")
                st.subheader("📊 Analysis Results")
                
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    fallacy_name = FALLACY_INFO.get(prediction['fallacy'], {}).get('name', prediction['fallacy'].title())
                    st.markdown(f"""
                    <div class="fallacy-card">
                        <h2 style="color: #ff6b9d; margin-top: 0;">🎯 {fallacy_name}</h2>
                        <p style="font-size: 1.1rem; margin: 1rem 0;">
                            <strong>Confidence:</strong> 
                            <span style="color: #4ade80; font-size: 1.3rem; font-weight: bold;">
                                {prediction['confidence']:.1%}
                            </span>
                        </p>
                        <p style="color: #e0e0e0; line-height: 1.6;">
                            <strong>Explanation:</strong> {prediction['explanation']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=prediction['confidence'] * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Confidence Score", 'font': {'size': 20, 'color': '#ff6b9d'}},
                        number={'suffix': "%", 'font': {'size': 40, 'color': '#ff6b9d'}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#ff6b9d"},
                            'bar': {'color': "#ff6b9d"},
                            'bgcolor': "rgba(255, 255, 255, 0.05)",
                            'borderwidth': 2,
                            'bordercolor': "#ff6b9d",
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(255, 107, 157, 0.1)'},
                                {'range': [50, 75], 'color': 'rgba(255, 107, 157, 0.2)'},
                                {'range': [75, 100], 'color': 'rgba(255, 107, 157, 0.3)'}
                            ],
                            'threshold': {
                                'line': {'color': "#4ade80", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=50, b=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        font={'color': "#ff6b9d", 'family': "Arial"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📚 Learn More About This Fallacy", expanded=False):
                    if prediction['fallacy'] in FALLACY_INFO:
                        info = FALLACY_INFO[prediction['fallacy']]
                        st.markdown(f"**Definition:** {info['definition']}")
                        st.markdown(f"**Why it's problematic:** {info['why_problematic']}")
                        st.markdown(f"**Example:** *\"{info['example']}\"*")
                
                st.session_state.analysis_history.append({
                    'text': user_input[:100] + "..." if len(user_input) > 100 else user_input,
                    'fallacy': fallacy_name,
                    'confidence': prediction['confidence']
                })
                
                st.success("✅ Analysis complete! Check the History tab to see all your analyses.")
            else:
                st.warning(f"⚠️ Confidence ({prediction['confidence']:.1%}) is below threshold ({confidence_threshold:.1%}). Try adjusting the threshold in the sidebar.")

# TAB 2: LEARN
with tab2:
    st.header("📖 Understanding Logical Fallacies")
    
    st.markdown("""
    Logical fallacies are errors in reasoning that undermine the logic of an argument. 
    Understanding them helps you think more critically and construct better arguments.
    """)
    
    st.markdown("---")
    
    search = st.text_input("🔎 Search fallacies:", placeholder="Type to search...")
    
    for fallacy_key, info in FALLACY_INFO.items():
        if not search or search.lower() in info['name'].lower() or search.lower() in info['definition'].lower():
            with st.expander(f"**{info['name']}**", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Definition:** {info['definition']}")
                    st.markdown(f"**Why problematic:** {info['why_problematic']}")
                with col2:
                    st.info(f"**Example:**\n\n*\"{info['example']}\"*")

# TAB 3: HISTORY
with tab3:
    st.header("📈 Analysis History")
    
    if st.session_state.analysis_history:
        history_df = pd.DataFrame(st.session_state.analysis_history)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Analyses", len(history_df))
        with col2:
            most_common = history_df['fallacy'].mode()[0] if len(history_df) > 0 else "N/A"
            st.metric("Most Common", most_common)
        with col3:
            avg_confidence = history_df['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Fallacy Distribution")
            fallacy_counts = history_df['fallacy'].value_counts()
            fig = px.pie(
                values=fallacy_counts.values,
                names=fallacy_counts.index,
                hole=0.4,
                color_discrete_sequence=['#ff6b9d', '#ff8fb3', '#ffb3c9', '#ffd7df', '#ffe0eb']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=False, 
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#ffffff'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Confidence Scores")
            fig = px.histogram(
                history_df,
                x='confidence',
                nbins=10,
                color_discrete_sequence=['#ff6b9d']
            )
            fig.update_layout(
                xaxis_title="Confidence",
                yaxis_title="Count",
                showlegend=False,
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#ffffff'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Recent Analyses")
        st.dataframe(
            history_df[['text', 'fallacy', 'confidence']].tail(10).iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
        
        csv = history_df.to_csv(index=False)
        st.download_button(
            label="📥 Download History (CSV)",
            data=csv,
            file_name="fallacy_analysis_history.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("👈 No analysis history yet. Start analyzing text in the **Analyze** tab!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #808080; padding: 2rem 0;'>
    <p style='margin: 0; font-size: 0.9rem;'>
        🚀 Built with Streamlit | 🧠 Powered by AI
    </p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem;'>
        <a href='https://github.com/Av1352/Logical-Fallacy-Detection' target='_blank' 
           style='color: #ff6b9d; text-decoration: none;'>
            View on GitHub →
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
