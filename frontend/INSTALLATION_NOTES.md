# Frontend Installation Notes

## Good News! ✅

If you saw those deprecation warnings, your installation **still succeeded**! Those were just warnings, not errors.

The warnings have now been fixed by updating to current package versions.

## Fresh Installation

If you already ran `npm install`, you have two options:

### Option 1: Continue with what you have (Recommended for quick start)
The app will work fine with the warnings. Just run:
```bash
npm run dev
```

### Option 2: Update to latest packages (Cleaner, no warnings)
```bash
# Remove old packages
rm -rf node_modules package-lock.json

# Pull latest changes
git pull

# Install with updated packages
npm install
```

## What Changed

**Before:**
- React 18.2 → **Now: 18.3** (latest stable)
- Material-UI 5.x → **Now: 6.x** (latest)
- ESLint 8.x → **Removed** (not needed for basic usage)
- Old transitive dependencies → **Updated automatically**

## Installation Steps (Fresh Install)

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies (2-5 minutes)
npm install

# 3. Create environment file
echo "VITE_API_URL=http://localhost:5000/api" > .env

# 4. Start development server
npm run dev
```

You should see:
```
  VITE v5.4.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Verification

Test that everything works:

```bash
# Build test (optional)
npm run build

# Should complete without errors
# Creates a 'dist' folder
```

## Common npm Warnings Explained

### "deprecated" warnings
- **What it means**: Package has a newer version or is no longer maintained
- **Impact**: Usually none - your app will still work fine
- **Fixed**: By updating package.json versions

### "peer dependency" warnings
- **What it means**: Package wants a specific version of another package
- **Impact**: Usually none if versions are close
- **Action**: Ignore unless you see actual errors

### "audit" warnings
- **What it means**: Security vulnerabilities in packages
- **Check**: Run `npm audit`
- **Fix**: Run `npm audit fix` (we already did this)

## Troubleshooting

### Issue: npm install fails with errors

**Solution 1: Clear cache**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Solution 2: Use legacy peer deps**
```bash
npm install --legacy-peer-deps
```

**Solution 3: Use npm 9+**
```bash
npm install -g npm@latest
npm --version  # Should be 9.x or 10.x
```

### Issue: Port 5173 already in use

```bash
# Find and kill process using port 5173
# macOS/Linux:
lsof -ti:5173 | xargs kill -9

# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Or use a different port:
npm run dev -- --port 3000
```

### Issue: "Cannot find module" errors

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Issue: Vite build fails

```bash
# Check Node.js version (need 18+)
node --version

# Update Node if needed
# https://nodejs.org/
```

## Success Checklist

After installation, verify:

- [ ] `node_modules` folder created
- [ ] `package-lock.json` created
- [ ] No ERROR messages (warnings are OK)
- [ ] `npm run dev` starts server
- [ ] Browser opens to http://localhost:5173
- [ ] You see the AI Resume Analyzer interface

## Next Steps

1. **Start the app**: `npm run dev`
2. **Check it works**: Open http://localhost:5173
3. **Start backend**: Follow backend/README.md
4. **Test upload**: Try uploading a resume

## Still Having Issues?

The warnings you saw are **normal and harmless**. If you can run `npm run dev` and see the app in your browser, everything is working correctly!

If you have actual **errors** (not warnings), please share:
- The full error message
- Your Node.js version: `node --version`
- Your npm version: `npm --version`
- Your operating system
