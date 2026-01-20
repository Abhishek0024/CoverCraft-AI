import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { auth } from '../api';
import { useNavigate } from 'react-router-dom';
import { Rocket, ArrowRight, User, Mail, Lock } from 'lucide-react';
import '../index.css';

const Auth = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Form States
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (isLogin) {
                const res = await auth.login(email, password);
                localStorage.setItem('access_token', res.data.access_token);
                navigate('/dashboard');
            } else {
                await auth.register({
                    email,
                    password,
                    first_name: firstName,
                    last_name: lastName
                });
                // Auto switch to login or auto login (here just switch for simplicity)
                setIsLogin(true);
                setError('Registration successful! Please login.'); // Using error state for success msg temporarily or create success state
            }
        } catch (err) {
            console.error("Auth Error:", err);
            const detail = err.response?.data?.detail;
            if (detail && typeof detail === 'object') {
                // Handle Pydantic validation errors (array of objects)
                setError(JSON.stringify(detail));
            } else {
                setError(detail || 'An error occurred');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative',
            overflow: 'hidden'
        }}>
            {/* Background Decor */}
            {/* Background Decor */}
            <div style={{
                position: 'absolute',
                top: '-10%',
                left: '-10%',
                width: '600px',
                height: '600px',
                background: 'radial-gradient(circle, rgba(79, 70, 229, 0.1) 0%, rgba(0,0,0,0) 70%)',
                filter: 'blur(80px)',
                zIndex: -1
            }} />
            <div style={{
                position: 'absolute',
                bottom: '-10%',
                right: '-10%',
                width: '500px',
                height: '500px',
                background: 'radial-gradient(circle, rgba(14, 165, 233, 0.1) 0%, rgba(0,0,0,0) 70%)',
                filter: 'blur(80px)',
                zIndex: -1
            }} />

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-panel"
                style={{ width: '100%', maxWidth: '480px', padding: '40px', position: 'relative', overflow: 'hidden' }}
            >
                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: '32px' }}>
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
                        <div style={{
                            width: '40px', height: '40px',
                            background: 'var(--accent)',
                            borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center'
                        }}>
                            <Rocket size={24} color="white" />
                        </div>
                        <h1 style={{ fontSize: '2rem', margin: 0 }}>CoverCraft AI</h1>
                    </div>
                    <p style={{ color: 'var(--text-secondary)' }}>
                        Empower your career with valid AI-driven narratives.
                    </p>
                </div>

                {/* Tabs */}
                <div style={{ display: 'flex', background: 'var(--bg-input)', padding: '4px', borderRadius: '12px', marginBottom: '24px' }}>
                    <button
                        onClick={() => setIsLogin(true)}
                        style={{
                            flex: 1, padding: '10px', borderRadius: '8px',
                            background: isLogin ? 'var(--bg-card)' : 'transparent',
                            color: isLogin ? 'var(--text-primary)' : 'var(--text-secondary)',
                            transition: 'all 0.3s ease',
                            boxShadow: isLogin ? '0 2px 8px rgba(0,0,0,0.2)' : 'none'
                        }}
                    >
                        Log In
                    </button>
                    <button
                        onClick={() => setIsLogin(false)}
                        style={{
                            flex: 1, padding: '10px', borderRadius: '8px',
                            background: !isLogin ? 'var(--bg-card)' : 'transparent',
                            color: !isLogin ? 'var(--text-primary)' : 'var(--text-secondary)',
                            transition: 'all 0.3s ease',
                            boxShadow: !isLogin ? '0 2px 8px rgba(0,0,0,0.2)' : 'none'
                        }}
                    >
                        Sign Up
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit}>
                    <AnimatePresence mode="wait">
                        {!isLogin && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                style={{ overflow: 'hidden' }}
                            >
                                <div style={{ display: 'flex', gap: '16px' }}>
                                    <div className="input-group">
                                        <label className="label">First Name</label>
                                        <div style={{ position: 'relative' }}>
                                            <User size={18} style={{ position: 'absolute', top: '16px', left: '16px', color: 'var(--text-muted)' }} />
                                            <input
                                                className="input-field"
                                                style={{ paddingLeft: '44px' }}
                                                value={firstName}
                                                onChange={(e) => setFirstName(e.target.value)}
                                                placeholder="John"
                                                required={!isLogin}
                                            />
                                        </div>
                                    </div>
                                    <div className="input-group">
                                        <label className="label">Last Name</label>
                                        <div style={{ position: 'relative' }}>
                                            <User size={18} style={{ position: 'absolute', top: '16px', left: '16px', color: 'var(--text-muted)' }} />
                                            <input
                                                className="input-field"
                                                style={{ paddingLeft: '44px' }}
                                                value={lastName}
                                                onChange={(e) => setLastName(e.target.value)}
                                                placeholder="Doe"
                                                required={!isLogin}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <div className="input-group">
                        <label className="label">Email Address</label>
                        <div style={{ position: 'relative' }}>
                            <Mail size={18} style={{ position: 'absolute', top: '16px', left: '16px', color: 'var(--text-muted)' }} />
                            <input
                                type="email"
                                className="input-field"
                                style={{ paddingLeft: '44px' }}
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="name@example.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="input-group">
                        <label className="label">Password</label>
                        <div style={{ position: 'relative' }}>
                            <Lock size={18} style={{ position: 'absolute', top: '16px', left: '16px', color: 'var(--text-muted)' }} />
                            <input
                                type="password"
                                className="input-field"
                                style={{ paddingLeft: '44px' }}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    {error && (
                        <div style={{
                            marginBottom: '20px', padding: '12px', borderRadius: '8px',
                            background: error.includes('success') ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                            color: error.includes('success') ? '#34d399' : '#f87171',
                            fontSize: '0.9rem', textAlign: 'center'
                        }}>
                            {error}
                        </div>
                    )}

                    <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
                        {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Create Account')}
                        {!loading && <ArrowRight size={18} />}
                    </button>
                </form>

                <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    By continuing, you agree to our Terms of Service and Privacy Policy.
                </div>
            </motion.div>
        </div>
    );
};

export default Auth;
