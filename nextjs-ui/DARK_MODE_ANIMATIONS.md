# Dark Mode & Professional Animations Guide

## 🌙 Dark Mode Implementation

The application now supports **automatic dark mode** based on system preferences with beautiful gradients and smooth transitions.

### How It Works

- **Automatic Detection**: Dark mode is enabled based on user's system preference (`prefers-color-scheme: dark`)
- **CSS Variables**: The theme uses CSS custom properties for easy color management
- **Smooth Transitions**: All color changes animate smoothly (300ms duration)

### Color Scheme

**Light Mode:**
- Background: White/Light Gray
- Text: Dark Slate
- Borders: Light Slate
- Accents: Blue/Green

**Dark Mode:**
- Background: Dark Slate/Charcoal
- Text: Light Gray/White
- Borders: Medium Slate
- Accents: Bright Blue/Green (adjusted for contrast)

## ✨ Professional Animations

### Advanced Keyframe Animations

1. **slideInDown** - Element slides down from above with fade
2. **slideInUp** - Element slides up from below with fade
3. **slideInLeft** - Element slides in from left with fade
4. **slideInRight** - Element slides in from right with fade
5. **fadeIn** - Simple opacity fade
6. **scaleIn** - Element scales up while fading in
7. **pulse-glow** - Blue glowing pulse effect
8. **shimmer** - Gradient shimmer animation
9. **bounce-smooth** - Smooth bouncing motion
10. **float** - Floating/levitating animation
11. **rotate-slow** - Slow 360-degree rotation
12. **gradient-shift** - Animated gradient background
13. **blob-animate** - Organic blob motion
14. **flip** - 3D flip animation
15. **slide-and-fade** - Combined slide and fade
16. **wiggle** - Small rotation wiggle
17. **neon-glow** - Neon glow text effect
18. **skeleton-loading** - Skeleton placeholder animation
19. **success-bounce** - Success state bounce

### Utility Classes

**Animation Utilities:**
- `.animate-bounce-smooth` - Smooth bouncing
- `.animate-float` - Floating effect
- `.animate-rotate-slow` - Slow rotation
- `.animate-gradient` - Animated gradient
- `.animate-blob` - Blob animation
- `.animate-flip` - Flip effect
- `.animate-slide-fade` - Slide with fade
- `.animate-wiggle` - Wiggle effect
- `.animate-neon` - Neon glow
- `.animate-success` - Success bounce

**Stagger Delays:**
- `.stagger-1` through `.stagger-10` (0.1s to 1.0s delays)
- Used for cascading animations of multiple elements

**Transition Classes:**
- `.transition-smooth` - 300ms smooth transition
- `.transition-smooth-slow` - 500ms smooth transition
- `.transition-smooth-slower` - 700ms smooth transition
- `.hover-lift` - Lift on hover with shadow

### Component Enhancements

**Navigation:**
- Gradient text logo
- Animated underline on hover
- Smooth color transitions in dark mode
- Rotating emoji icon

**Main Page:**
- Gradient text heading with glow effect
- Staggered button animations
- Cascading content animations
- Floating empty state

**Company Search Form:**
- Field entrance animations
- Hover shadow effects
- Pulsing enrichment warning box
- Gradient submit button

**Analytics Dashboard:**
- Bouncing statistics cards
- Hover lift effects
- Animated table rows
- Gradient text stats
- Glowing download buttons

**Results Components:**
- Scale-in card animation
- Staggered metric cards
- Animated tabs with smooth switching
- Sliding content transitions

### Dark Mode Aware Components

**Glass Morphism:**
- `.glass` - Frosted glass effect (light)
- `.glass-dark` - Frosted glass effect (dark)

**Shadow Utilities:**
- `.shadow-dark` - Dark mode optimized shadow
- `.shadow-dark-lg` - Large dark mode shadow

**Glow Effects:**
- `.glow-blue` - Blue glow
- `.glow-green` - Green glow

**Interactive Elements:**
- `.btn-primary` - Primary button (dark mode aware)
- `.btn-secondary` - Secondary button (dark mode aware)
- `.input-animated` - Animated input fields
- `.card-dark` - Dark mode aware cards

## 🎨 Color Palette

### Gradients Used

1. **Blue to Purple** - Primary gradient for headers
2. **Blue to Green** - Secondary gradient for accents
3. **Customizable** - Based on CSS variables

### Typography

- **Headings**: Bold, gradient text
- **Labels**: Smaller, accent colored
- **Body**: Comfortable reading contrast

## 🚀 Performance

- **GPU Acceleration**: All animations use `transform` and `opacity` for smooth 60fps
- **CSS-based**: No JavaScript overhead for animations
- **Efficient Transitions**: Minimal repaints and reflows
- **Responsive**: All animations work on mobile devices

## 📱 Responsive Design

- **Mobile**: Animations optimized for smaller screens
- **Tablet**: Full animation support
- **Desktop**: Enhanced animations with hover effects

## 🔧 Usage Guide

### Adding Animations to New Elements

```html
<!-- Slide down on load -->
<div class="animate-slide-down">Content</div>

<!-- Slide up with delay -->
<div class="animate-slide-up" style={{ animationDelay: '0.2s' }}>Content</div>

<!-- Fade in -->
<div class="animate-fade-in">Content</div>

<!-- Scale in -->
<div class="animate-scale-in">Content</div>

<!-- Floating effect -->
<div class="animate-float">Content</div>

<!-- Bouncing smooth -->
<div class="animate-bounce-smooth">Content</div>
```

### Adding Stagger Effects

```html
<!-- Multiple items with staggered entrance -->
<div class="animate-slide-up stagger-1">Item 1</div>
<div class="animate-slide-up stagger-2">Item 2</div>
<div class="animate-slide-up stagger-3">Item 3</div>
```

### Dark Mode Transitions

```html
<!-- Automatically adapts to dark mode -->
<div class="bg-white dark:bg-slate-800 transition-colors duration-300">
  Content
</div>
```

## 🌐 Browser Support

- ✅ Chrome/Edge 88+
- ✅ Firefox 87+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 📈 Future Enhancements

- [ ] Custom animation speed controls
- [ ] Animation preference settings
- [ ] Advanced theme customization
- [ ] Animation event tracking
- [ ] Accessibility improvements for reduced motion

## 📚 Resources

- Tailwind CSS Documentation
- MDN Web Docs (CSS Animations)
- Web Animations Performance Best Practices
