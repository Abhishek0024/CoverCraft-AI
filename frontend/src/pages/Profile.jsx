import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { user, auth } from '../api';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, Copy, FileText, Star, Zap } from 'lucide-react';

const Profile = () => {
    const navigate = useNavigate();
    const [history, setHistory] = useState([]);
    const [userInfo, setUserInfo] = useState({ name: '', email: '' });
    const [loading, setLoading] = useState(true);
    const [expandedId, setExpandedId] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            await Promise.all([fetchHistory(), fetchUserInfo()]);
            setLoading(false);
        };
        loadData();
    }, []);

    const fetchUserInfo = async () => {
        try {
            const res = await auth.me(); // Fetching directly from auth api wrapper we just made
            setUserInfo({
                name: `${res.data.first_name} ${res.data.last_name}`,
                email: res.data.email
            });
        } catch (err) {
            console.error(err);
        }
    };

    const fetchHistory = async () => {
        try {
            const res = await user.getHistory();
            setHistory(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            // setLoading(false); // Handled in Promise.all
        }
    };

    const copycontent = (text) => {
        navigator.clipboard.writeText(text);
        alert("Copied!");
    };

    return (
        <div style={{ minHeight: '100vh', padding: '40px 20px' }}>
            <div className="container">
                {/* Header */}
                <div style={{ marginBottom: '40px', display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <button onClick={() => navigate('/dashboard')} className="btn btn-secondary">
                        <ArrowLeft size={18} /> Back
                    </button>
                    <h1 style={{ fontSize: '2rem', margin: 0, color: 'var(--text-primary)' }}>My Profile</h1>
                </div>

                <div style={{ marginBottom: '40px' }}>
                    <div className="profile-user-info" style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                        <div style={{
                            width: '80px', height: '80px', borderRadius: '50%', background: 'var(--accent)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '2.5rem', fontWeight: 600, color: 'white'
                        }}>
                            {userInfo.name.charAt(0)}
                        </div>
                        <div>
                            <h2 style={{ fontSize: '2.5rem', fontWeight: 700, margin: 0, lineHeight: 1.2 }}>{userInfo.name}</h2>
                            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', margin: 0 }}>{userInfo.email}</p>
                        </div>
                    </div>
                </div>

                <div className="profile-grid" style={{}}>

                    {/* History List */}
                    <div>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '20px' }}>Saved Letters</h2>

                        {loading ? (
                            <p>Loading history...</p>
                        ) : history.length === 0 ? (
                            <div className="glass-panel" style={{ padding: '40px', textAlign: 'center' }}>
                                <FileText size={48} color="var(--text-muted)" style={{ margin: '0 auto 20px' }} />
                                <p style={{ color: 'var(--text-secondary)' }}>You haven't generated any cover letters yet.</p>
                                <button onClick={() => navigate('/dashboard')} className="btn btn-primary" style={{ marginTop: '20px' }}>
                                    Create One Now
                                </button>
                            </div>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                {history.map((item) => (
                                    <motion.div
                                        key={item.id}
                                        className="glass-panel"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        style={{ overflow: 'hidden' }}
                                    >
                                        <div
                                            onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}
                                            style={{
                                                padding: '20px', cursor: 'pointer',
                                                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                                            }}
                                        >
                                            <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                                                <div style={{
                                                    width: '40px', height: '40px', borderRadius: '8px',
                                                    background: 'var(--bg-input)', display: 'flex', alignItems: 'center', justifyContent: 'center'
                                                }}>
                                                    <FileText size={20} color="var(--accent)" />
                                                </div>
                                                <div>
                                                    <h3 style={{ fontSize: '1.1rem', margin: 0 }}>{item.title}</h3>
                                                    <div style={{ display: 'flex', gap: '12px', fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                                            <Clock size={14} /> {new Date(item.created_at).toLocaleDateString()}
                                                        </span>
                                                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--accent)' }}>
                                                            <Zap size={14} fill="currentColor" /> {Math.round((item.match_score || 0) * 100)}% Match
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <AnimatePresence>
                                            {expandedId === item.id && (
                                                <motion.div
                                                    initial={{ height: 0 }}
                                                    animate={{ height: 'auto' }}
                                                    exit={{ height: 0 }}
                                                    style={{ overflow: 'hidden', borderTop: '1px solid var(--border-light)' }}
                                                >
                                                    <div style={{ padding: '20px', background: 'var(--bg-secondary)' }}>
                                                        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '10px' }}>
                                                            <button
                                                                onClick={() => copycontent(item.content)}
                                                                className="btn btn-secondary"
                                                                style={{ fontSize: '0.8rem', padding: '6px 12px' }}
                                                            >
                                                                <Copy size={14} /> Copy
                                                            </button>
                                                        </div>
                                                        <div style={{ whiteSpace: 'pre-wrap', fontFamily: 'serif', lineHeight: 1.6, color: 'var(--text-primary)' }}>
                                                            {item.content}
                                                        </div>
                                                    </div>
                                                </motion.div>
                                            )}
                                        </AnimatePresence>
                                    </motion.div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Sidebar Stats */}
                    <div>
                        <div className="glass-panel" style={{ padding: '24px' }}>
                            <h3 style={{ fontSize: '1.1rem', marginBottom: '16px' }}>Stats</h3>
                            <div style={{ marginBottom: '20px' }}>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Total Letters</p>
                                <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent)' }}>{history.length}</p>
                            </div>
                            <div>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Avg Match Score</p>
                                <p style={{ fontSize: '2rem', fontWeight: 700 }}>
                                    {history.length > 0
                                        ? Math.round((history.reduce((acc, curr) => acc + (curr.match_score || 0), 0) / history.length) * 100)
                                        : 0}%
                                </p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default Profile;
