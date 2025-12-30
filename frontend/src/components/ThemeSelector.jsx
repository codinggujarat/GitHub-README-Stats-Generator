import { Palette } from 'lucide-react';

export const themes = [
    { id: 'default', name: 'Dark', color: '#1a1b27' },
    { id: 'light', name: 'Light', color: '#ffffff' },
    { id: 'neon', name: 'Neon', color: '#00ffff' },
    { id: 'glass', name: 'Glass', color: '#888888' },
    { id: 'cyberpunk', name: 'Cyber', color: '#fcee0a' },
    { id: 'dracula', name: 'Dracula', color: '#bd93f9' },
    { id: 'monokai', name: 'Monokai', color: '#a6e22e' },
    { id: 'nord', name: 'Nord', color: '#88c0d0' },
    { id: 'solarized_light', name: 'Solarized Light', color: '#fdf6e3' },
    { id: 'solarized_dark', name: 'Solarized Dark', color: '#002b36' },
    { id: 'cobalt', name: 'Cobalt', color: '#002240' },
    { id: 'synthwave', name: 'Synthwave', color: '#ff71ce' },
    { id: 'high_contrast', name: 'High Contrast', color: '#000000' },
    { id: 'gruvbox', name: 'Gruvbox', color: '#fe8019' },
    { id: 'tokyonight', name: 'Tokyo Night', color: '#7aa2f7' },
];

export default function ThemeSelector({ currentTheme, setTheme }) {
    return (
        <div className="flex flex-col gap-3 w-full">
            <div className="flex items-center gap-2">
                <Palette className="w-4 h-4 text-gray-500" />
                <label className="text-xs uppercase tracking-wider font-bold text-gray-500">Visual Theme</label>
            </div>

            <div className="grid grid-cols-2 gap-2">
                {themes.map((theme) => (
                    <button
                        key={theme.id}
                        onClick={() => setTheme(theme.id)}
                        className={`
              relative p-3 rounded-xl text-xs font-semibold text-left transition-all duration-300
              ${currentTheme === theme.id
                                ? 'bg-brand-accent text-white shadow-lg shadow-brand-accent/25 scale-[1.02] ring-2 ring-brand-accent/50 ring-offset-2 ring-offset-gray-100 dark:ring-offset-[#0d1117]'
                                : 'bg-black/5 dark:bg-white/5 text-gray-600 dark:text-gray-400 hover:bg-black/10 dark:hover:bg-white/10 hover:text-gray-900 dark:hover:text-gray-200'}
            `}
                    >
                        <div className="flex items-center gap-2">
                            <div
                                className="w-2 h-2 rounded-full shadow-[0_0_8px_rgba(0,0,0,0.5)]"
                                style={{ backgroundColor: theme.color }}
                            ></div>
                            {theme.name}
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
}
