# Installed Extraction Methods

## ✅ All 10 Methods Installed!

### Traditional Methods (3)
1. **PDFPlumber** ⚡
   - Speed: ~12ms
   - Cost: Free
   - Usage: `uv run python methods/traditional/pdfplumber_extractor.py file.pdf`

2. **Camelot**
   - Speed: ~443ms
   - Cost: Free
   - Usage: `uv run python methods/traditional/camelot_extractor.py file.pdf`

3. **Tabula**
   - Speed: ~100ms (requires Java)
   - Cost: Free
   - Usage: `uv run python methods/traditional/tabula_extractor.py file.pdf`

### Deep Learning Methods (2)
4. **Table Transformer** (Microsoft)
   - Speed: ~100-300ms (CPU), faster on GPU
   - Cost: Free
   - SOTA accuracy
   - Usage: `uv run python methods/deep_learning/table_transformer_extractor.py file.pdf`

5. **Docling** (IBM Research)
   - Speed: ~200-500ms
   - Cost: Free
   - Modern architecture
   - Usage: `uv run python methods/deep_learning/docling_extractor.py file.pdf`

### LLM Vision Methods (3)
6. **GPT-4 Vision (GPT-4o)**
   - Speed: ~1-3s
   - Cost: ~$0.01-0.03 per page
   - Highest accuracy
   - Requires: OPENAI_API_KEY
   - Usage: `uv run python methods/llm/gpt4_vision_extractor.py file.pdf`

7. **Claude 3.5 Sonnet Vision**
   - Speed: ~0.5-1s
   - Cost: ~$0.003 per page
   - Best value
   - Requires: ANTHROPIC_API_KEY
   - Usage: `uv run python methods/llm/claude_vision_extractor.py file.pdf`

8. **Gemini 1.5 Flash Vision**
   - Speed: ~0.3-0.8s
   - Cost: ~$0.001 per page (very cheap)
   - Good speed/cost ratio
   - Requires: GOOGLE_API_KEY
   - Usage: `uv run python methods/llm/gemini_vision_extractor.py file.pdf`

### Hybrid Methods (1)
9. **Layout Detection + GPT-4**
   - Speed: ~1.5s
   - Cost: ~$0.01 per page
   - Combines fast detection with AI content extraction
   - Requires: OPENAI_API_KEY
   - Usage: `uv run python methods/hybrid/layout_gpt4_extractor.py file.pdf`

## 🚀 Quick Start

### Setup API Keys (for LLM methods)
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### Compare All Methods
```bash
# Test all available methods
uv run python compare_all_methods.py demo_table.pdf

# Test specific methods only
uv run python compare_all_methods.py file.pdf pdfplumber gpt4_vision claude_vision
```

### Test Individual Methods
```bash
# Traditional
uv run python methods/traditional/pdfplumber_extractor.py file.pdf

# Deep Learning
uv run python methods/deep_learning/table_transformer_extractor.py file.pdf

# LLM Vision (requires API key)
uv run python methods/llm/gpt4_vision_extractor.py file.pdf
uv run python methods/llm/claude_vision_extractor.py file.pdf
uv run python methods/llm/gemini_vision_extractor.py file.pdf

# Hybrid
uv run python methods/hybrid/layout_gpt4_extractor.py file.pdf
```

## 📊 Expected Performance

| Method | Speed | Cost | Accuracy | Best For |
|--------|-------|------|----------|----------|
| PDFPlumber | 12ms | Free | Good | Simple tables, speed |
| Camelot | 443ms | Free | Good | Bordered tables |
| Tabula | 100ms | Free | Good | Industry standard |
| Table Transformer | 100-300ms | Free | Excellent | SOTA free method |
| Docling | 200-500ms | Free | Very Good | Modern architecture |
| GPT-4 Vision | 1-3s | $0.02/pg | Excellent | Complex layouts |
| Claude 3.5 Sonnet | 0.5-1s | $0.003/pg | Excellent | Best value |
| Gemini 1.5 Flash | 0.3-0.8s | $0.001/pg | Very Good | Cheapest fast option |
| Hybrid (Layout+GPT-4) | 1.5s | $0.01/pg | Excellent | Production use |

## 🎯 Recommendations

**For Speed:** PDFPlumber (12ms, free)
**For Accuracy (Free):** Table Transformer (100-300ms, free)
**For Accuracy (Paid):** GPT-4 Vision (1-3s, $0.02/page)
**For Best Value:** Claude 3.5 Sonnet (0.5-1s, $0.003/page)
**For Production:** Hybrid Layout+GPT-4 (1.5s, $0.01/page)

## 💡 Notes

### API Keys
- Get OpenAI API key: https://platform.openai.com/api-keys
- Get Anthropic API key: https://console.anthropic.com/
- Get Google API key: https://aistudio.google.com/apikey

### Dependencies
All dependencies are already installed via `uv sync`.

### GPU Acceleration
Table Transformer will automatically use GPU if available (much faster).
Check with: `python -c "import torch; print(torch.cuda.is_available())"`

## 🔧 Troubleshooting

**"API key not configured"**
- Create `.env` file from `.env.example`
- Add your API keys

**Table Transformer slow?**
- Running on CPU (expected)
- Use GPU for 10x speed improvement

**Tabula not working?**
- Install Java: `sudo apt install default-jre`

## 📝 Next Steps

1. Test on your own PDFs
2. Compare results across methods
3. Choose best method for your use case
4. Run comprehensive benchmark on FinTabNet dataset
