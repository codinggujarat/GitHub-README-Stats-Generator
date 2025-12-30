import { Search } from 'lucide-react';

export default function InputSection({ username, setUsername, onGenerate }) {
    return (
        <div className="flex flex-col gap-3 w-full">
            <label className="text-xs uppercase tracking-wider font-bold text-gray-500">GitHub Username</label>
            <div className="flex flex-col gap-3">
                <div className="relative group">
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Type your username..."
                        className="glass-input w-full pl-10 pr-4 py-3 rounded-xl text-white placeholder-gray-500 text-sm font-medium"
                    />
                    <Search className="absolute left-3 top-3.5 w-4 h-4 text-gray-500 group-focus-within:text-brand-accent transition-colors" />
                </div>
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
