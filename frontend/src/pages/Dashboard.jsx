import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { resume, job, generator } from '../api';
import {
    Upload, FileText, Zap, Settings, Check,
    Copy, Download, LogOut, ChevronRight, Briefcase, User, Home
} from 'lucide-react';

const Dashboard = () => {
    const navigate = useNavigate();
    const [step, setStep] = useState(1); // 1: Inputs, 2: Review/Generate
    const [showDropdown, setShowDropdown] = useState(false);

    // Data State
    const [resumeFile, setResumeFile] = useState(null);
    const [resumeId, setResumeId] = useState(null);
    const [jdText, setJdText] = useState('');
    const [jdId, setJdId] = useState(null);

    // Generation State
    const [tone, setTone] = useState('Professional');
    const [focus, setFocus] = useState('Skills Match');
    const [generatedResult, setGeneratedResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [statusMsg, setStatusMsg] = useState('');

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/');
    };

    const handleResumeUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setResumeFile(file);
        setStatusMsg('Uploading resume...');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await resume.upload(formData);
            setResumeId(res.data.resume_id);
            setStatusMsg('');
        } catch (err) {
            console.error(err);
            setStatusMsg('Error uploading resume');
        }
    };

    const handleJdSubmit = async () => {
        if (!jdText) return;
        setStatusMsg('Analyzing job description...');
        try {
            const res = await job.extract(jdText);
            setJdId(res.data.jd_id);
            setStatusMsg('');
            setStep(2); // Auto advance if resume is ready, or just user manual
        } catch (err) {
            console.error(err);
            setStatusMsg('Error analyzing JD');
        }
    };

    const handleGenerate = async () => {
        if (!resumeId || !jdId) {
            alert('Please upload a resume and provide a job description first.');
            return;
        }
        setLoading(true);
        setStatusMsg('Crafting your cover letter...');
        try {
            const payload = {
                resume_id: resumeId,
                jd_id: jdId,
                tone: tone.toLowerCase(),
                focus: focus.toLowerCase().split(' ')[0]
            };

            const res = await generator.create(payload);
            setGeneratedResult(res.data);
            setStatusMsg('');
        } catch (err) {
            // console.error(err);
            setStatusMsg('Generation failed');
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = () => {
        if (generatedResult?.cover_letter) {
            navigator.clipboard.writeText(generatedResult.cover_letter);
            alert('Copied to clipboard!');
        }
    };

    // UI Components
    return (
        <div style={{ minHeight: '100vh', padding: '40px 20px' }}>
            <div className="container">
                {/* Header */}
                <header style={{
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    marginBottom: '40px', paddingBottom: '20px', borderBottom: '1px solid var(--border-light)'
                }}>
                    <div
                        onClick={() => navigate('/')}
                        style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}
                    >
                        <div style={{
                            width: '36px', height: '36px', borderRadius: '8px',
                            background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center'
                        }}>
                            <Zap size={20} color="white" fill="currentColor" />
                        </div>
                        <h2 style={{ fontSize: '1.5rem', margin: 0 }}>CoverCraft AI</h2>
                    </div>
                    <div style={{ position: 'relative' }}>
                        <button
                            onClick={() => setShowDropdown(!showDropdown)}
                            style={{
                                width: '40px', height: '40px', borderRadius: '50%',
                                background: 'white', border: '1px solid var(--border-light)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                cursor: 'pointer', outline: 'none', boxShadow: 'var(--shadow-sm)'
                            }}
                        >
                            <User size={20} color="var(--text-primary)" />
                        </button>

                        <AnimatePresence>
                            {showDropdown && (
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.95, y: 10 }}
                                    animate={{ opacity: 1, scale: 1, y: 0 }}
                                    exit={{ opacity: 0, scale: 0.95, y: 10 }}
                                    transition={{ duration: 0.1 }}
                                    style={{
                                        position: 'absolute', top: '50px', right: 0,
                                        background: '#fff', border: '1px solid var(--border-light)',
                                        borderRadius: '12px', boxShadow: 'var(--shadow-lg)',
                                        width: '200px', zIndex: 50, overflow: 'hidden',
                                        transformOrigin: 'top right'
                                    }}
                                >
                                    <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border-light)' }}>
                                        <p style={{ margin: 0, fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)' }}>My Account</p>
                                    </div>

                                    <div
                                        onClick={() => { setShowDropdown(false); navigate('/profile'); }}
                                        className="dropdown-item"
                                    >
                                        <User size={16} /> Profile
                                    </div>

                                    <div
                                        onClick={() => { setShowDropdown(false); navigate('/'); }}
                                        className="dropdown-item"
                                    >
                                        <Home size={16} /> Home
                                    </div>

                                    <div
                                        onClick={handleLogout}
                                        className="dropdown-item danger"
                                        style={{ color: '#ef4444' }}
                                    >
                                        <LogOut size={16} /> Sign Out
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </header>

                <div className="dashboard-grid">

                    {/* Left Panel: Inputs */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

                        {/* Resume Section */}
                        <section className="glass-panel" style={{ padding: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                                <h3 style={{ fontSize: '1.1rem', fontFamily: 'var(--font-body)' }}>1. Resume</h3>
                                {resumeId && <Check size={20} color="#34d399" />}
                            </div>

                            <div style={{ position: 'relative' }}>
                                <input
                                    type="file"
                                    accept=".pdf,.docx,.txt"
                                    onChange={handleResumeUpload}
                                    style={{
                                        position: 'absolute', opacity: 0, width: '100%', height: '100%',
                                        cursor: 'pointer', zIndex: 2
                                    }}
                                />
                                <div style={{
                                    border: '2px dashed var(--border-light)', borderRadius: 'var(--radius-md)',
                                    padding: '30px', textAlign: 'center', transition: 'all 0.3s ease',
                                    background: 'var(--bg-input)'
                                }}
                                    className="upload-zone"
                                >
                                    {resumeFile ? (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', justifyContent: 'center' }}>
                                            <FileText size={24} color="var(--accent)" />
                                            <span style={{ color: 'var(--text-primary)' }}>{resumeFile.name}</span>
                                        </div>
                                    ) : (
                                        <>
                                            <Upload size={32} color="var(--text-secondary)" style={{ marginBottom: '12px' }} />
                                            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Click or Drag Resume Here</p>
                                            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>PDF, DOCX, TXT</p>
                                        </>
                                    )}
                                </div>
                            </div>
                        </section>

                        {/* JD Section */}
                        <section className="glass-panel" style={{ padding: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                                <h3 style={{ fontSize: '1.1rem', fontFamily: 'var(--font-body)' }}>2. Job Description</h3>
                                {jdId && <Check size={20} color="#34d399" />}
                            </div>
                            <textarea
                                className="input-field"
                                placeholder="Paste the job description here..."
                                rows={8}
                                value={jdText}
                                onChange={(e) => setJdText(e.target.value)}
                                style={{ resize: 'vertical', minHeight: '150px' }}
                            />
                            <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                                <button
                                    onClick={handleJdSubmit}
                                    className="btn btn-secondary"
                                    disabled={!jdText}
                                >
                                    Analyze JD <ChevronRight size={16} />
                                </button>
                            </div>
                        </section>

                        {/* Controls */}
                        <section className="glass-panel" style={{ padding: '24px' }}>
                            <h3 style={{ fontSize: '1.1rem', fontFamily: 'var(--font-body)', marginBottom: '16px' }}>3. Settings</h3>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                                <div className="input-group" style={{ margin: 0 }}>
                                    <label className="label">Tone</label>
                                    <select
                                        className="input-field"
                                        value={tone}
                                        onChange={(e) => setTone(e.target.value)}
                                    >
                                        <option>Formal</option>
                                        <option>Enthusiastic</option>
                                        <option>Professional</option>
                                        <option>Creative</option>
                                        <option>Direct</option>
                                    </select>
                                </div>
                                <div className="input-group" style={{ margin: 0 }}>
                                    <label className="label">Focus</label>
                                    <select
                                        className="input-field"
                                        value={focus}
                                        onChange={(e) => setFocus(e.target.value)}
                                    >
                                        <option>Skills Match</option>
                                        <option>Key Achievements</option>
                                        <option>Company Culture</option>
                                    </select>
                                </div>
                            </div>

                            <button
                                className="btn btn-primary"
                                style={{ width: '100%', marginTop: '24px', opacity: (resumeId && jdId) ? 1 : 0.5 }}
                                onClick={handleGenerate}
                                disabled={!resumeId || !jdId || loading}
                            >
                                {loading ? 'Crafting Magic...' : 'Generate Letter'}
                                {!loading && <Zap size={18} fill="currentColor" />}
                            </button>

                            {statusMsg && (
                                <p style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.9rem', color: 'var(--accent)' }}>
                                    {statusMsg}
                                </p>
                            )}
                        </section>

                    </div>

                    {/* Right Panel: Preview */}
                    <div style={{ height: '100%' }}>
                        <motion.div
                            className="glass-panel"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            style={{
                                height: '100%', minHeight: '600px', display: 'flex', flexDirection: 'column',
                                border: generatedResult ? '1px solid var(--accent)' : '1px solid var(--border-light)'
                            }}
                        >
                            {generatedResult ? (
                                <>
                                    <div style={{
                                        padding: '20px 30px', borderBottom: '1px solid var(--border-light)',
                                        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                                    }}>
                                        <div>
                                            <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Match Score</span>
                                            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--accent)' }}>
                                                {Math.round((generatedResult.match_score || 0) * 100)}%
                                            </div>
                                        </div>
                                        <div style={{ display: 'flex', gap: '10px' }}>
                                            <button onClick={copyToClipboard} className="btn btn-secondary" title="Copy">
                                                <Copy size={18} />
                                            </button>
                                            {/* Download logic would go here */}
                                        </div>
                                    </div>
                                    <div style={{ padding: '40px', flex: 1, overflowY: 'auto', background: '#ffffff', color: '#000000', margin: '20px', borderRadius: '4px' }}>
                                        <div style={{ whiteSpace: 'pre-wrap', fontFamily: 'Georgia, serif', lineHeight: '1.6' }}>
                                            {generatedResult.cover_letter}
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <div style={{
                                    flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                                    color: 'var(--text-muted)'
                                }}>
                                    <div style={{
                                        width: '80px', height: '80px', borderRadius: '50%', background: 'var(--bg-input)',
                                        display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px'
                                    }}>
                                        <Settings size={40} opacity={0.5} />
                                    </div>
                                    <p>Your tailored cover letter will appear here.</p>
                                </div>
                            )}
                        </motion.div>
                    </div>

                </div>
            </div>
        </div >
    );
};

export default Dashboard;
