# Latency Measurement - Quick Start Guide

## 🚀 Quick Start (30 seconds)

1. **Open your chat page** at http://localhost:8000/chat-page
2. **Send any message** to the AI
3. **Look below the AI response** - you'll see latency metrics!

Example:
```
⚡ 1234ms total  🔧 1100ms server  🌐 134ms network
RAG: 980ms | DB: 45ms
```

## 📊 What Do The Numbers Mean?

| Metric | What It Measures | Good Range |
|--------|------------------|------------|
| **Total** | Complete request-to-response time | < 1500ms |
| **Server** | Backend processing time | < 1200ms |
| **Network** | Network + transfer time | < 300ms |
| **RAG** | AI query processing | < 1000ms |
| **DB** | Database operations | < 100ms |

## 🎨 Color Codes

- 🟢 **Green badge** (< 1500ms): Fast! Everything is working great
- 🟡 **Yellow badge** (1500-3000ms): Medium. Acceptable but could be better
- 🔴 **Red badge** (> 3000ms): Slow. Consider optimization

## 🧪 Testing

### Quick Test
```bash
# 1. Edit test_latency.py - add your username/password
# 2. Run:
python test_latency.py
```

### Manual Test
1. Open browser dev tools (F12)
2. Go to Network tab
3. Send a chat message
4. Check the `/api/chat` request timing
5. Compare with displayed metrics

## 🔧 Troubleshooting

### No latency shown?
- Hard refresh: Ctrl+Shift+R (Ctrl+Cmd+R on Mac)
- Check browser console for errors
- Verify backend is updated

### Numbers seem wrong?
- Server metrics are accurate
- Client metrics can vary based on browser/system load
- Network time affected by connection quality

### Still having issues?
```bash
# Check if server returns latency data
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' | grep -o '"latency":{[^}]*}'
```

## 📈 Performance Tips

### If RAG is slow (> 2000ms)
```python
# Option 1: Use smaller embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')  # Faster

# Option 2: Cache results
from functools import lru_cache
@lru_cache(maxsize=100)
def get_response(query):
    ...
```

### If DB is slow (> 200ms)
```python
# Add database indexes
class ChatMessage(models.Model):
    ...
    class Meta:
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]
```

### If Network is slow (> 500ms)
- Check internet connection
- Consider hosting closer to users
- Enable response compression

## 📚 More Information

- **Full Documentation**: See `LATENCY-MEASUREMENT.md`
- **Visual Examples**: See `LATENCY-VISUAL-EXAMPLE.md`
- **Test Script**: Run `test_latency.py`

## ✅ Quick Checklist

After implementing latency measurement:

- [ ] Can see latency metrics in chat UI
- [ ] Badges show correct colors
- [ ] Numbers make sense (server + network ≈ total)
- [ ] Test script runs successfully
- [ ] Performance is acceptable (< 1500ms most of the time)

## 🎯 Next Steps

1. **Monitor**: Check latency for a few days
2. **Analyze**: Identify bottlenecks (RAG, DB, or Network)
3. **Optimize**: Focus on the biggest time consumer
4. **Repeat**: Measure again after optimization

## 💡 Pro Tips

- **Compare queries**: Simple queries should be faster
- **Time of day**: Performance may vary with server load
- **User location**: Affects network time significantly
- **Cache warming**: First query might be slower

---

**Need Help?** Check the full documentation or run the test script for detailed diagnostics.
