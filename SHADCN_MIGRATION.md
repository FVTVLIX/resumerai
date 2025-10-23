# shadcn/ui Migration Guide

## Progress Status

### ✅ Completed
- [x] Updated package.json (removed MUI, added Tailwind + shadcn dependencies)
- [x] Added Tailwind CSS configuration
- [x] Added PostCSS configuration
- [x] Updated index.css with Tailwind directives
- [x] Created utility functions (lib/utils.js)
- [x] Added base shadcn/ui components:
  - button.jsx
  - card.jsx
  - progress.jsx
  - accordion.jsx
  - alert.jsx
  - badge.jsx
- [x] Rewrote Header component

### 🚧 In Progress
The remaining components need to be updated. I'll complete this shortly.

## What Changed

### Dependencies
**Removed:**
- @mui/material
- @mui/icons-material
- @emotion/react
- @emotion/styled

**Added:**
- tailwindcss
- @radix-ui/react-progress
- @radix-ui/react-accordion
- @radix-ui/react-slot
- lucide-react (for icons)
- class-variance-authority
- clsx
- tailwind-merge

### File Structure
```
frontend/src/
├── components/
│   ├── ui/              # NEW: shadcn/ui base components
│   │   ├── button.jsx
│   │   ├── card.jsx
│   │   ├── progress.jsx
│   │   ├── accordion.jsx
│   │   ├── alert.jsx
│   │   └── badge.jsx
│   ├── Header.jsx       # ✅ Updated
│   ├── UploadSection.jsx    # ⏳ To be updated
│   ├── AnalysisProgress.jsx # ⏳ To be updated
│   ├── ResultsDashboard.jsx # ⏳ To be updated
│   └── ErrorMessage.jsx     # ⏳ To be updated
├── lib/
│   └── utils.js         # NEW: Tailwind utility functions
├── index.css            # ✅ Updated with Tailwind
└── App.jsx              # ⏳ To be updated

frontend/
├── tailwind.config.js   # NEW
└── postcss.config.js    # NEW
```

## Installation

After pulling these changes:

```bash
cd frontend

# Remove old node_modules
rm -rf node_modules package-lock.json

# Install new dependencies
npm install

# Start dev server
npm run dev
```

## Design Comparison

### Before (Material-UI)
```jsx
<Button variant="contained" color="primary">
  Click Me
</Button>
```

### After (shadcn/ui)
```jsx
<Button variant="default">
  Click Me
</Button>
```

### Key Differences

| Feature | Material-UI | shadcn/ui |
|---------|-------------|-----------|
| **Styling** | sx prop, styled components | Tailwind CSS classes |
| **Icons** | @mui/icons-material | lucide-react |
| **Theme** | ThemeProvider | CSS variables |
| **Components** | Imported from library | Copy/paste into project |
| **Customization** | Theme override | Edit component files directly |

## Component Mapping

| MUI Component | shadcn/ui Equivalent |
|---------------|---------------------|
| `<Button>` | `<Button>` |
| `<Card>`, `<CardContent>` | `<Card>`, `<CardContent>` |
| `<LinearProgress>` | `<Progress>` |
| `<Accordion>` | `<Accordion>` |
| `<Alert>` | `<Alert>` |
| `<Chip>` | `<Badge>` |
| `<Box>` | `<div>` with Tailwind classes |
| `<Typography>` | HTML elements with Tailwind |

## Styling Guide

### Layout
```jsx
// MUI
<Box sx={{ display: 'flex', gap: 2, p: 3 }}>

// shadcn/ui (Tailwind)
<div className="flex gap-2 p-3">
```

### Spacing
- `sx={{ p: 2 }}` → `className="p-2"`
- `sx={{ mt: 4 }}` → `className="mt-4"`
- `sx={{ mx: 'auto' }}` → `className="mx-auto"`

### Colors
- `color="primary"` → `className="text-primary"`
- `bgcolor="error.main"` → `className="bg-destructive"`

### Typography
- `<Typography variant="h1">` → `<h1 className="text-4xl font-bold">`
- `<Typography variant="body1">` → `<p className="text-base">`

## Remaining Work

I'll complete the following components next:

1. **UploadSection** - File upload with drag-and-drop
2. **AnalysisProgress** - Progress tracking
3. **ResultsDashboard** - Main results display
4. **ErrorMessage** - Error states
5. **App.jsx** - Remove MUI ThemeProvider

## Benefits of shadcn/ui

1. **No Runtime Overhead** - Components are copied into your project
2. **Full Control** - Edit components directly
3. **Tailwind Integration** - Utility-first CSS
4. **Modern Design** - Clean, professional look
5. **Smaller Bundle** - Only include what you use
6. **Better DX** - Auto-completion with Tailwind

## Next Steps

Pull this commit and run `npm install`. The foundation is ready.

I'll complete the remaining components in the next commit.
