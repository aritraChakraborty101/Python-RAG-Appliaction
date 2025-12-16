# Latency Measurement - Verification Checklist

Use this checklist to verify the latency measurement feature is working correctly.

## ✅ Pre-Flight Checks

- [ ] Django server is running (`python manage.py runserver`)
- [ ] Virtual environment is activated
- [ ] You can access the chat page (http://localhost:8000/chat-page)
- [ ] You are logged in

## ✅ Visual Verification

### 1. Basic Display
- [ ] Send a message in the chat
- [ ] Latency information appears below AI response
- [ ] You can see three badges: Total, Server, Network
- [ ] You can see the detailed breakdown (RAG and DB times)

### 2. Color Coding
- [ ] Fast responses (< 1500ms) show GREEN badge
- [ ] Medium responses (1500-3000ms) show YELLOW badge  
- [ ] Slow responses (> 3000ms) show RED badge

### 3. Metrics Accuracy
- [ ] Total time ≈ Server time + Network time (±50ms tolerance)
- [ ] Server time = RAG time + DB time (approximately)
- [ ] All times are in milliseconds
- [ ] Numbers are reasonable (not negative, not extremely large)

## ✅ Functional Testing

### Test 1: Simple Query
```
Send: "Hi"
Expected: Fast response, low RAG time
- [ ] Response received
- [ ] Latency displayed
- [ ] Numbers seem reasonable
```

### Test 2: Complex Query
```
Send: "Explain machine learning in detail with examples"
Expected: Longer RAG time
- [ ] Response received
- [ ] RAG time > simple query
- [ ] Still shows latency correctly
```

### Test 3: Multiple Messages
```
Send 3-5 messages in succession
Expected: Each shows its own latency
- [ ] Each message has latency info
- [ ] Latencies vary slightly
- [ ] No errors in console
```

## ✅ Browser Console Checks

### Chrome/Firefox DevTools
1. Open DevTools (F12)
2. Go to Console tab
3. Send a message

- [ ] No JavaScript errors
- [ ] No 404 errors
- [ ] No CORS errors

### Network Tab
1. Go to Network tab in DevTools
2. Send a message
3. Click on the `/api/chat` request

- [ ] Status: 201 Created
- [ ] Response contains `latency` field
- [ ] Response time matches displayed time (roughly)

## ✅ API Response Verification

### Using Browser DevTools
```javascript
// In console, send a test request
fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    },
    body: JSON.stringify({ message: 'test' })
})
.then(r => r.json())
.then(d => console.log('Latency:', d.latency))
```

- [ ] Response includes `latency` object
- [ ] `latency.total_ms` is present
- [ ] `latency.rag_processing_ms` is present
- [ ] `latency.database_ms` is present
- [ ] `latency.breakdown` is present

### Using curl
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' | jq '.latency'
```

- [ ] Command returns latency data
- [ ] JSON is well-formed
- [ ] All expected fields present

## ✅ Test Script Verification

### Run the test script
```bash
# 1. Edit test_latency.py with credentials
# 2. Run:
python test_latency.py
```

- [ ] Script runs without errors
- [ ] Login successful
- [ ] Message sent successfully
- [ ] Latency metrics displayed
- [ ] Performance rating shown

## ✅ Cross-Browser Testing

### Chrome
- [ ] Latency displays correctly
- [ ] Colors show properly
- [ ] No console errors

### Firefox
- [ ] Latency displays correctly
- [ ] Colors show properly
- [ ] No console errors

### Safari (if available)
- [ ] Latency displays correctly
- [ ] Colors show properly
- [ ] No console errors

## ✅ Mobile Testing (Optional)

If you have mobile device or responsive mode:

- [ ] Open chat in mobile view
- [ ] Send message
- [ ] Latency displays properly (may wrap)
- [ ] Still readable on small screen

## ✅ Edge Cases

### Slow Network Simulation
1. Open DevTools → Network tab
2. Set throttling to "Slow 3G"
3. Send message

- [ ] Latency still measured correctly
- [ ] Network time increases significantly
- [ ] No timeouts or errors

### Multiple Tabs
1. Open chat in two browser tabs
2. Send messages from both

- [ ] Each tab shows its own latency
- [ ] No conflicts between tabs
- [ ] Both work independently

### Page Reload
1. Send a message (see latency)
2. Reload page
3. Check conversation history

- [ ] Old messages still visible
- [ ] Old latency info NOT stored (expected)
- [ ] New messages show new latency

## ✅ Performance Checks

### Server Impact
- [ ] Server response time didn't increase significantly
- [ ] CPU usage normal
- [ ] Memory usage normal

### Client Impact
- [ ] Page loads normally
- [ ] Chat remains responsive
- [ ] No noticeable slowdown

## ✅ Documentation Checks

- [ ] `LATENCY-QUICKSTART.md` exists and is readable
- [ ] `LATENCY-MEASUREMENT.md` exists and is complete
- [ ] `LATENCY-VISUAL-EXAMPLE.md` exists with examples
- [ ] `test_latency.py` exists and is executable

## ✅ Code Quality

### Backend (chat/views.py)
- [ ] `import time` at top of file
- [ ] `chat()` function includes timing code
- [ ] Latency data added to response
- [ ] No syntax errors

### Frontend (chat/templates/chat/chat_multi.html)
- [ ] CSS styles for latency added
- [ ] JavaScript measures client time
- [ ] `addMessageToUI()` accepts latency parameter
- [ ] No JavaScript syntax errors

## 🎯 Final Verification

### Quick Test Sequence
1. [ ] Open chat page
2. [ ] Send message: "What is Python?"
3. [ ] Verify latency appears
4. [ ] Check that total ≈ server + network
5. [ ] Check color badge matches speed
6. [ ] Open browser console - no errors
7. [ ] Check Network tab - latency in response
8. [ ] Send another message - works again

### If ALL checked:
✅ **Implementation is working correctly!**

### If ANY unchecked:
See troubleshooting section in `LATENCY-MEASUREMENT.md`

## 📊 Expected Values (Approximate)

Good performance:
- Total: 500-1500ms
- Server: 400-1200ms
- Network: 50-300ms
- RAG: 300-1000ms
- DB: 20-100ms

Acceptable performance:
- Total: 1500-3000ms
- Server: 1200-2500ms
- Network: 100-500ms
- RAG: 1000-2000ms
- DB: 50-200ms

Needs optimization:
- Total: > 3000ms
- Server: > 2500ms
- RAG: > 2000ms
- DB: > 200ms

## 🐛 Common Issues

### No latency shown
- Hard refresh (Ctrl+Shift+R)
- Check browser console
- Verify backend is updated

### Wrong numbers
- Check timezone/locale settings
- Verify performance.now() available
- Check for browser extensions interfering

### Errors in console
- Check authentication token
- Verify API endpoint accessible
- Check CORS settings if needed

---

**Last Updated**: December 16, 2025  
**Version**: 1.0
