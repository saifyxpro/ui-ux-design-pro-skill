# UI Design System Audit Report

**Date:** 2/18/2026, 6:07:55 AM
**Files Scanned:** 1
**Total Issues:** 5

## 📄 `test/audit_fail.tsx`
Summary: 🔴 1 Critical | 🟡 4 Warnings | 🔵 0 Info

| Line | Severity | Rule | Message | Fix |
| :--- | :--- | :--- | :--- | :--- |
| 5 | 🔴 CRITICAL | `AI001` | Tailwind interpolation detected — JIT compiler cannot extract these classes <br> _Code:_ `return <button className={`bg-${color}-500 text-white`}>Click me</button>;` | Use a safelist map object: className={colorMap[props.color]} |
| 9 | 🟡 WARNING | `AI005` | Hallucinated utility "text-shadow" — does not exist in Tailwind defaults <br> _Code:_ `const Header = () => <h1 className="text-shadow-md">Hello</h1>;` | Use drop-shadow-md or a custom plugin |
| 12 | 🟡 WARNING | `AI008` | Low contrast pseudo-transparency used on potential text background <br> _Code:_ `const Hero = () => <div className="bg-black/50 text-white">Cover</div>;` | Use glassmorphism: backdrop-filter: blur(4px) brightness(0.5) |
| 18 | 🟡 WARNING | `AI013` | h-screen causes layout shifts on mobile browsers (address bar resize) <br> _Code:_ `const FullScreen = () => <div className="h-screen">Full</div>;` | Use dynamic viewport height: h-[100dvh] |
| 21 | 🟡 WARNING | `AI015` | target="_blank" validation missing rel="noopener noreferrer" <br> _Code:_ `const Link = () => <a href="https://google.com" target="_blank">External</a>;` | Add rel="noopener noreferrer" to prevent tabnabbing |

