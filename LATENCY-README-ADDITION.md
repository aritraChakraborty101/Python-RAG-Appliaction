# Add This Section to README.md

Add the following section to your main README.md file under a "Features" or "Performance Monitoring" section:

---

## 📊 Latency Measurement

The application includes built-in latency measurement to monitor response times and identify performance bottlenecks.

### Quick Start

1. **Use the chat**: Latency metrics automatically appear below each AI response
2. **Interpret the colors**:
   - 🟢 Green (< 1.5s): Fast
   - 🟡 Yellow (1.5-3s): Medium
   - 🔴 Red (> 3s): Slow

### What's Measured

- **Total Time**: Complete request-to-response round-trip
- **Server Time**: Backend processing (RAG + Database)
- **Network Time**: Network latency
- **RAG Processing**: AI query and response generation
- **Database**: Data storage operations

### Example Output

```
⚡ 1234ms total  🔧 1100ms server  🌐 134ms network
RAG: 980ms | DB: 45ms
```

### Documentation

- **Quick Start**: See `LATENCY-QUICKSTART.md`
- **Full Guide**: See `LATENCY-MEASUREMENT.md`
- **Examples**: See `LATENCY-VISUAL-EXAMPLE.md`

### Testing

```bash
# Edit test_latency.py with your credentials, then:
python test_latency.py
```

---

## Alternative: Compact Version for README.md

If you prefer a more compact version:

---

## Performance Monitoring

Real-time latency measurement is built-in. Each chat response shows:
- Total response time (color-coded: 🟢 fast, 🟡 medium, 🔴 slow)
- Server processing time
- Network latency
- Detailed breakdown (RAG, Database)

See `LATENCY-QUICKSTART.md` for details.

---
