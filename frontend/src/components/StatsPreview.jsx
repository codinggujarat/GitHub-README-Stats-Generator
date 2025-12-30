import { useState, useEffect } from 'react';
import { Copy, Check, Loader2 } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export default function StatsPreview({ username, theme, showPrivate, showTrophies }) {
    const [copied, setCopied] = useState(false);
    const [loading, setLoading] = useState(true);
    const [loadedImages, setLoadedImages] = useState(0);

    // Reset loading when inputs change
    useEffect(() => {
        setLoading(true);
        setLoadedImages(0);
    }, [username, theme, showPrivate, showTrophies]);

    // Check if all images are loaded
    useEffect(() => {
        const expectedImages = showTrophies ? 4 : 3;
        if (loadedImages >= expectedImages) {
            setLoading(false);
        }
    }, [loadedImages, showTrophies]);

    const handleImageLoad = () => {
        setLoadedImages(prev => prev + 1);
    };

    if (!username) return null;

    // Construct URLs
    const queryParams = `?theme=${theme}&include_private=${showPrivate}`;
    const statsUrl = `${API_BASE_URL}/stats/${username}/svg${queryParams}`;
    const langUrl = `${API_BASE_URL}/languages/${username}/svg${queryParams}`;
    const streakUrl = `${API_BASE_URL}/streak/${username}/svg${queryParams}`;
    const trophiesUrl = `${API_BASE_URL}/trophies/${username}/svg${queryParams}`;

    let markdown = `![${username}'s Stats](${statsUrl})\n\n![Top Langs](${langUrl})\n\n![Streak](${streakUrl})`;
    if (showTrophies) {
        markdown += `\n\n![Trophies](${trophiesUrl})`;
    }

    const handleCopy = () => {
        navigator.clipboard.writeText(markdown);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="w-full max-w-2xl mx-auto mt-12 animate-in fade-in slide-in-from-bottom-4 duration-500 relative">
            {loading && (
                <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-white/80 dark:bg-[#0d1117]/80 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-[#30363d]">
                    <Loader2 className="w-10 h-10 text-brand-accent animate-spin mb-4" />
                    <p className="text-gray-600 dark:text-gray-400 font-medium animate-pulse">Generating Visualization...</p>
                </div>
            )}

            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">Preview</h2>
                <button
                    onClick={handleCopy}
                    disabled={loading}
                    className="flex items-center gap-2 text-sm text-brand-accent hover:text-brand-accent/80 dark:hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    {copied ? 'Copied!' : 'Copy Markdown'}
                </button>
            </div>

            <div className={`bg-white dark:bg-[#161b22] border border-gray-200 dark:border-[#30363d] rounded-xl p-6 flex flex-col items-center gap-6 overflow-hidden transition-all duration-500 shadow-xl ${loading ? 'opacity-0' : 'opacity-100'}`}>
                {/* Stats Card */}
                <div className="flex flex-col gap-6 w-full items-center">
                    <div className="transform hover:scale-[1.02] transition-transform duration-300">
                        <img
                            src={statsUrl}
                            alt="GitHub Stats"
                            onLoad={handleImageLoad}
                            onError={handleImageLoad} // Count errors as loaded to avoid stuck spinner
                            className="rounded-lg shadow-lg max-w-full"
                        />
                    </div>
                    <div className="transform hover:scale-[1.02] transition-transform duration-300">
                        <img
                            src={langUrl}
                            alt="Top Languages"
                            onLoad={handleImageLoad}
                            onError={handleImageLoad}
                            className="rounded-lg shadow-lg max-w-full"
                        />
                    </div>
                    <div className="transform hover:scale-[1.02] transition-transform duration-300">
                        <img
                            src={streakUrl}
                            alt="GitHub Streak"
                            onLoad={handleImageLoad}
                            onError={handleImageLoad}
                            className="rounded-lg shadow-lg max-w-full"
                        />
                    </div>
                    {showTrophies && (
                        <div className="transform hover:scale-[1.02] transition-transform duration-300">
                            <img
                                src={trophiesUrl}
                                alt="GitHub Trophies"
                                onLoad={handleImageLoad}
                                onError={handleImageLoad}
                                className="rounded-lg shadow-lg max-w-full"
                            />
                        </div>
                    )}
                </div>

                {/* Code Snippet */}
                <div className="w-full bg-gray-100 dark:bg-[#0d1117] p-4 rounded-lg font-mono text-xs text-gray-600 dark:text-gray-400 overflow-x-auto text-wrap break-all border border-gray-200 dark:border-transparent">
                    <code>{markdown}</code>
                </div>
            </div>
        </div>
    );
}
