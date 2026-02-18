import React, { useEffect, useState } from 'react';

// AI001: Fixed - Safelist
const COLOR_MAP = {
  red: 'bg-red-500',
  blue: 'bg-blue-500',
};
const Button = ({ color }) => {
  return <button className={COLOR_MAP[color] + " text-white"}>Click me</button>;
};

// AI005: Fixed - Drop Shadow
const Header = () => <h1 className="drop-shadow-md">Hello</h1>;

// AI008: Fixed - Glassmorphism
const Hero = () => <div className="backdrop-blur-sm brightness-50 text-white">Cover</div>;

// AI010: Fixed - Underscores
const Layout = () => <div className="w-[calc(100%_-_20px)]">Content</div>;

// AI013: Fixed - Dynamic Viewport Height
const FullScreen = () => <div className="h-[100dvh]">Full</div>;

// AI015: Fixed - Rel Noopener
const Link = () => <a href="https://google.com" target="_blank" rel="noopener noreferrer">External</a>;
