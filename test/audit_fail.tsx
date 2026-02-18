import React, { useEffect, useState } from 'react';

// AI001: Dynamic Class Interpolation
const Button = ({ color }) => {
  return <button className={`bg-${color}-500 text-white`}>Click me</button>;
};

// AI005: Non-existent utility
const Header = () => <h1 className="text-shadow-md">Hello</h1>;

// AI008: Pseudo-transparency contrast
const Hero = () => <div className="bg-black/50 text-white">Cover</div>;

// AI010: Arbitrary calc spacing (missing underscores)
const Layout = () => <div className="w-[calc(100%-20px)]">Content</div>;

// AI013: VH mobile bug
const FullScreen = () => <div className="h-screen">Full</div>;

// AI015: Target blank vulnerability
const Link = () => <a href="https://google.com" target="_blank">External</a>;
