import { useState } from 'react';
import { Copy, Check } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export default function StatsPreview({ username, theme }) {
    const [copied, setCopied] = useState(false);

    if (!username) return null;

    // Construct URLs
    const statsUrl = `${API_BASE_URL}/stats/${username}/svg?theme=${theme}`;
    const langUrl = `${API_BASE_URL}/languages/${username}/svg?theme=${theme}`;
    const streakUrl = `${API_BASE_URL}/streak/${username}/svg?theme=${theme}`;

    const markdown = `![${username}'s Stats](${statsUrl})\n\n![Top Langs](${langUrl})\n\n![Streak](${streakUrl})`;

    const handleCopy = () => {
        navigator.clipboard.writeText(markdown);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="w-full max-w-2xl mx-auto mt-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white">Preview</h2>
                <button
                    onClick={handleCopy}
                    className="flex items-center gap-2 text-sm text-brand-accent hover:text-white transition-colors"
                >
                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    {copied ? 'Copied!' : 'Copy Markdown'}
                </button>
            </div>

            <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-6 flex flex-col items-center gap-6 overflow-hidden">
                {/* Stats Card */}
                <div className="flex flex-col gap-6 w-full items-center">
                    <div className="transform hover:scale-[1.02] transition-transform duration-300">
                        <img
                            src={statsUrl}
                            alt="GitHub Stats"
                            className="rounded-lg shadow-lg max-w-full"
                            onError={(e) => { e.target.src = ''; e.target.alt = 'User not found or API Error'; }}
                        />
                    </div>
                    <div className="transform hover:scale-[1.02] transition-transform duration-300">
                        <img
                            src={langUrl}
                            alt="Top Languages"
                            className="rounded-lg shadow-lg max-w-full"
                        />
                    </div>
                    <div className="transform hover:scale-[1.02] transition-transform duration-300">
                        <img
                            src={streakUrl}
                            alt="GitHub Streak"
                            className="rounded-lg shadow-lg max-w-full"
                        />
                    </div>
                </div>

                {/* Code Snippet */}
                <div className="w-full bg-[#0d1117] p-4 rounded-lg font-mono text-xs text-gray-400 overflow-x-auto">
                    <code>{markdown}</code>
                </div>
            </div>
        </div>
    );
}
