# 🚀 Kaggle Training Instructions

## Step 1: Upload Files to Kaggle

1. **Create a Kaggle Dataset:**
   - Go to https://www.kaggle.com/datasets
   - Click "New Dataset"
   - Upload `C:\Users\Nike\Documents\Programming\Projects\N8N\data\dataset.jsonl`
   - Name it: `n8n-workflow-dataset`
   - Make it public or private
   - Click "Create"

2. **Add Dataset to Your Notebook:**
   - In your `Trainer.ipynb` notebook on Kaggle
   - Click "Add Data" (top right)
   - Search for your dataset name
   - Click "Add"

## Step 2: Update the Dataset Path in Cell 10

In cell 10, change this line:
```python
with open('/kaggle/input/your-dataset/dataset.jsonl', 'r', encoding='utf-8') as f:
```

To:
```python
with open('/kaggle/input/n8n-workflow-dataset/dataset.jsonl', 'r', encoding='utf-8') as f:
```

## Step 3: Run All Cells in Order

Execute cells **1-22** in sequence:

### ✅ Cells You Can Run Now:
- **Cell 1**: Check GPU ✓ (already done)
- **Cell 4**: Install dependencies (~5 minutes)
- **Cell 6**: Check if workflows folder exists (will fail - expected)
- **Cell 8**: Build training dataset (SKIP - you have dataset.jsonl)
- **Cell 10**: Load dataset from JSONL ✓ (**RUN THIS**)
- **Cell 12**: Load base model (~10 minutes)
- **Cell 14**: Configure LoRA adapters (~1 minute)
- **Cell 16**: Set training parameters
- **Cell 18**: **START TRAINING** (~30-90 minutes) 🚀
- **Cell 20**: Save trained model
- **Cell 22**: Test the model (optional)

### ⏭️ Skip These Cells:
- Cell 6: Check workflows folder (not needed)
- Cell 8: Build dataset (you already have it)

## Step 4: Monitor Training Progress

The training cell (18) will show:
- Loss values decreasing
- Training steps progress
- Estimated time remaining

**Expected training time**: 30-90 minutes for 1001 examples

## Step 5: Download Trained Model

After training completes:

1. Go to Kaggle's **"Output"** tab (top right)
2. Find folder: `n8n-workflow-generator-final`
3. Click **"Download"** (may take 5-10 minutes)
4. Extract the downloaded file to:
   ```
   C:\Users\Nike\Documents\Programming\Projects\N8N\models\n8n-workflow-generator-final
   ```

## Step 6: Update Your .env File

Open `C:\Users\Nike\Documents\Programming\Projects\N8N\.env` and update:

```env
# Local LLM settings
LOCAL_MODEL_PATH=C:\Users\Nike\Documents\Programming\Projects\N8N\models\n8n-workflow-generator-final
LOCAL_MODEL_PORT=5001
```

## Step 7: Start Inference Server

In your local PowerShell:
```powershell
cd C:\Users\Nike\Documents\Programming\Projects\N8N
python scripts\serve\local_inference.py
```

## Step 8: Test Your Model

Open http://localhost:5000 and try:
- "Create a workflow that sends an email"
- "Build a workflow with Google Sheets and Slack"
- "Create an HTTP webhook that processes data"

---

## 🔥 Quick Training Checklist

- [ ] Upload `dataset.jsonl` to Kaggle dataset
- [ ] Add dataset to notebook
- [ ] Update path in cell 10
- [ ] Run cells 1, 4, 10, 12, 14, 16, 18, 20, 22
- [ ] Wait ~30-90 minutes for training
- [ ] Download model from Output tab
- [ ] Extract to `models/n8n-workflow-generator-final`
- [ ] Update `.env` with model path
- [ ] Run `python scripts/serve/local_inference.py`
- [ ] Test at http://localhost:5000

---

## ⚠️ Common Issues

**Issue**: "File not found" in cell 10
**Fix**: Update the path to match your Kaggle dataset name

**Issue**: "CUDA out of memory"
**Fix**: Restart kernel and reduce `per_device_train_batch_size` to 1 in cell 16

**Issue**: "Model download is too slow"
**Fix**: Normal - model is ~3-5GB, takes 5-10 minutes

**Issue**: "Cannot connect to local model"
**Fix**: Make sure inference server is running before testing

---

## 🎉 Success Indicators

✅ Training loss decreases from ~5.0 to ~1.0-2.0
✅ Model generates valid JSON with "nodes" and "connections"
✅ Inference server responds at http://localhost:5001/health
✅ Web UI generates workflows from natural language

Good luck with training! 🚀
