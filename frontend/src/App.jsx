import { useState, useEffect } from 'react';
import InputSection from './components/InputSection';
import ThemeSelector from './components/ThemeSelector';
import StatsPreview from './components/StatsPreview';
import { Github, Sparkles, Moon, Sun } from 'lucide-react';

function App() {
    const [username, setUsername] = useState('');
    const [activeUser, setActiveUser] = useState('');
    const [theme, setTheme] = useState('default');
    const [showPrivate, setShowPrivate] = useState(false);
    const [showTrophies, setShowTrophies] = useState(true);
    const [darkMode, setDarkMode] = useState(true);

    const handleGenerate = () => {
        if (username.trim()) {
            setActiveUser(username.trim());
        }
    };

    return (
        <div className={darkMode ? 'dark' : ''}>
            <div className="relative min-h-screen flex flex-col items-center justify-center py-12 px-4 overflow-hidden transition-colors duration-500 bg-brand-gray dark:bg-brand-dark">

                {/* Aurora Background Effects */}
                <div className="fixed inset-0 z-0 opacity-40 pointer-events-none">
                    <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
                    <div className="absolute top-0 -right-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
                    <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>
                </div>

                <div className="relative z-10 w-full max-w-5xl flex flex-col items-center gap-8">

                    {/* Header - Glass Card */}
                    <header className="glass-panel rounded-2xl p-8 text-center w-full max-w-2xl animate-in fade-in slide-in-from-top-4 duration-700 relative">
                        <button
                            onClick={() => setDarkMode(!darkMode)}
                            className="absolute top-4 right-4 p-2 rounded-full hover:bg-black/10 dark:hover:bg-white/10 transition-colors"
                        >
                            {darkMode ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-gray-600" />}
                        </button>

                        <div className="flex items-center justify-center gap-3 mb-2">
                            <div className="p-3 bg-brand-accent/20 rounded-full">
                                <Github className="w-8 h-8 text-brand-accent" />
                            </div>
                            <h1 className="text-4xl md:text-5xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400">
                                README <span className="text-brand-accent">S</span>TATS
                            </h1>
                        </div>
                        <p className="text-gray-600 dark:text-gray-400 text-lg font-light max-w-lg mx-auto flex items-center justify-center gap-2">
                            <Sparkles className="w-4 h-4 text-yellow-500 dark:text-yellow-400" />
                            Turn your GitHub profile into a work of art.
                        </p>
                    </header>

                    {/* Main Controls - Glass Card */}
                    <main className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6">

                        <div className="lg:col-span-4 glass-panel rounded-2xl p-6 flex flex-col gap-6 animate-in fade-in slide-in-from-left-4 duration-700 delay-100 h-fit">
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Configuration</h2>
                            <InputSection
                                username={username}
                                setUsername={setUsername}
                                onGenerate={handleGenerate}
                                showPrivate={showPrivate}
                                setShowPrivate={setShowPrivate}
                                showTrophies={showTrophies}
                                setShowTrophies={setShowTrophies}
                            />
                            <div className="my-2 h-px bg-gray-200 dark:bg-white/5"></div>
                            <ThemeSelector
                                currentTheme={theme}
                                setTheme={setTheme}
                            />
                        </div>

                        <div className="lg:col-span-8 min-h-[400px]">
                            {activeUser ? (
                                <StatsPreview
                                    username={activeUser}
                                    theme={theme}
                                    username={activeUser}
                                    theme={theme}
                                    showPrivate={showPrivate}
                                    showTrophies={showTrophies}
                                />
                            ) : (
                                <div className="glass-panel rounded-2xl p-12 h-full flex flex-col items-center justify-center text-center animate-in fade-in zoom-in duration-500">
                                    <div className="w-24 h-24 bg-gray-200 dark:bg-white/5 rounded-full flex items-center justify-center mb-4">
                                        <Github className="w-12 h-12 text-gray-500 dark:text-gray-600" />
                                    </div>
                                    <h3 className="text-2xl font-bold text-gray-700 dark:text-gray-500">Ready to Generate</h3>
                                    <p className="text-gray-600 dark:text-gray-600 mt-2">Enter your username on the left to visualize your stats.</p>
                                </div>
                            )}
                        </div>

                    </main>

                    <footer className="w-full text-center py-6 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-200">
                        <a
                            href="https://github.com/codinggujarat"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-gray-500 dark:text-gray-400 hover:text-brand-accent dark:hover:text-brand-accent transition-colors text-sm font-medium"
                        >
                            Made with ❤️ by codinggujarat
                        </a>
                    </footer>
                </div>
            </div>
        </div>
    );
}

export default App;
