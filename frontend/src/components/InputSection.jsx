import { Search } from 'lucide-react';

export default function InputSection({ username, setUsername, onGenerate, showPrivate, setShowPrivate, showTrophies, setShowTrophies }) {
    return (
        <div className="flex flex-col gap-3 w-full">
            <label className="text-xs uppercase tracking-wider font-bold text-gray-500 dark:text-gray-500">GitHub Username</label>
            <div className="flex flex-col gap-3">
                <div className="relative group">
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Type your username..."
                        className="glass-input w-full pl-10 pr-4 py-3 rounded-xl text-sm font-medium"
                    />
                    <Search className="absolute left-3 top-3.5 w-4 h-4 text-gray-400 dark:text-gray-500 group-focus-within:text-brand-accent transition-colors" />
                </div>
                <label className="flex items-center gap-2 cursor-pointer group">
                    <div className="relative">
                        <input
                            type="checkbox"
                            checked={showPrivate}
                            onChange={(e) => setShowPrivate(e.target.checked)}
                            className="sr-only peer"
                        />
                        <div className="w-10 h-6 bg-gray-300 dark:bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-accent"></div>
                    </div>
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400 group-hover:text-brand-accent dark:group-hover:text-white transition-colors">
                        Show Private Commits
                    </span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer group">
                    <div className="relative">
                        <input
                            type="checkbox"
                            checked={showTrophies}
                            onChange={(e) => setShowTrophies(e.target.checked)}
                            className="sr-only peer"
                        />
                        <div className="w-10 h-6 bg-gray-300 dark:bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-yellow-500"></div>
                    </div>
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400 group-hover:text-yellow-500 dark:group-hover:text-yellow-400 transition-colors">
                        Show Trophies (Beta)
                    </span>
                </label>
                <button
                    onClick={onGenerate}
                    className="glass-button w-full py-3 rounded-xl font-bold uppercase tracking-wide text-sm"
                >
                    Generate Stats
                </button>
            </div>
        </div>
    );
}
