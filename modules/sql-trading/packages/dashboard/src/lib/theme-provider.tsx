'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggle: () => void;
  senior: boolean;
  toggleSenior: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'dark',
  toggle: () => {},
  senior: false,
  toggleSenior: () => {},
});

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('dark');
  const [senior, setSenior] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('theme') as Theme;
    if (saved) setTheme(saved);
    const savedSenior = localStorage.getItem('senior') === 'true';
    setSenior(savedSenior);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute('data-senior', String(senior));
    localStorage.setItem('senior', String(senior));
  }, [senior]);

  const toggle = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  const toggleSenior = () => setSenior(prev => !prev);

  return (
    <ThemeContext.Provider value={{ theme, toggle, senior, toggleSenior }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
