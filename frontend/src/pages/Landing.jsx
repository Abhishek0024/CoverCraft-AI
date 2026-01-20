import React from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Star, Zap, CheckCircle, FileText, Sparkles } from 'lucide-react';

const Landing = () => {
    const navigate = useNavigate();
    const { scrollY } = useScroll();
    const y1 = useTransform(scrollY, [0, 500], [0, 200]);
    const y2 = useTransform(scrollY, [0, 500], [0, -150]);

    return (
        <div className="landing-page">
            {/* Dynamic Background */}
            <div className="bg-noise"></div>
            <div className="bg-gradient-1"></div>
            <div className="bg-gradient-2"></div>

            {/* Navigation */}
            <nav className="nav-container">
                <div className="logo-section" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
                    <div className="logo-icon">
                        <Zap size={24} fill="currentColor" />
                    </div>
                    <span className="logo-text">CoverCraft AI</span>
                </div>
                <div className="nav-links">
                    <button onClick={() => navigate('/auth')} className="btn btn-secondary glass-btn">Sign In</button>
                    <button onClick={() => navigate('/auth')} className="btn btn-primary glow-effect">
                        Get Started <ArrowRight size={18} />
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                    >
                        <div className="badge-pill">
                            <Sparkles size={14} className="text-accent" />
                            <span>v2.0 Now Live</span>
                        </div>
                        <h1 className="hero-title">
                            Craft Your Career <br />
                            <span className="text-gradient-primary">Narrative with AI</span>
                        </h1>
                        <p className="hero-subtitle">
                            Stop writing generic cover letters. Our intelligent engine analyzes your resume and job description to craft a narrative that <em>demands</em> attention.
                        </p>

                        <div className="hero-cta-group">
                            <button onClick={() => navigate('/auth')} className="btn btn-primary btn-lg glow-effect">
                                Start Building Free
                            </button>
                            <div className="social-proof">
                                <div className="avatars">
                                    {[1, 2, 3].map(i => (
                                        <div key={i} className="avatar" style={{ backgroundImage: `url(https://i.pravatar.cc/100?img=${i + 10})` }} />
                                    ))}
                                </div>
                                <div className="text">
                                    <span className="stars">★★★★★</span>
                                    <span className="label">Loved by 10k+ job seekers</span>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* Visual/Art Section */}
                <div className="hero-visual">
                    <motion.div style={{ y: y1 }} className="floating-card card-main glass-panel">
                        <div className="card-header">
                            <div className="dot red"></div>
                            <div className="dot yellow"></div>
                            <div className="dot green"></div>
                        </div>
                        <div className="card-body">
                            <div className="skeleton-line w-75"></div>
                            <div className="skeleton-line w-50"></div>
                            <div className="skeleton-line w-100 mt-4"></div>
                            <div className="skeleton-line w-100"></div>
                            <div className="skeleton-line w-90"></div>

                            <motion.div
                                animate={{ opacity: [0.5, 1, 0.5] }}
                                transition={{ duration: 2, repeat: Infinity }}
                                className="ai-cursor"
                            />
                        </div>
                        <div className="card-badge">
                            <CheckCircle size={16} /> 98% Match
                        </div>
                    </motion.div>

                    {/* Decorative Elements */}
                    <motion.div style={{ y: y2 }} className="floating-element coin-1">
                        <FileText size={40} />
                    </motion.div>
                </div>
            </section>

            {/* Marquee / Clients */}
            <div className="ticker-wrap">
                <div className="ticker">
                    {['GOOGLE', 'AMAZON', 'MICROSOFT', 'NETFLIX', 'SPOTIFY', 'META'].map((company, i) => (
                        <span key={i} className="ticker-item">{company}</span>
                    ))}
                    {['GOOGLE', 'AMAZON', 'MICROSOFT', 'NETFLIX', 'SPOTIFY', 'META'].map((company, i) => (
                        <span key={i + 10} className="ticker-item">{company}</span>
                    ))}
                </div>
            </div>

            {/* Feature Section */}
            <section className="features-section container">
                <div className="section-header text-center">
                    <h2 className="section-title">Beyond Standard Templates</h2>
                    <p className="section-desc">We don't just fill in blanks. We analyze semantic meaning.</p>
                </div>

                <div className="feature-grid">
                    <FeatureCard
                        icon={<Zap />}
                        title="Instant Analysis"
                        desc="Our engine breaks down JD requirements into core competencies in milliseconds."
                    />
                    <FeatureCard
                        icon={<Star />}
                        title="Human-Like Tone"
                        desc="Choose from 5+ distinct tones. No more robotic 'I am writing to apply' intros."
                    />
                    <FeatureCard
                        icon={<CheckCircle />}
                        title="ATS Optimized"
                        desc="Keywords are naturally woven into the narrative to pass initial screeners."
                    />
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <div className="container footer-content">
                    <div className="footer-brand">
                        <h3>CoverCraft AI</h3>
                        <p>Elevating careers, one letter at a time.</p>
                    </div>
                    <div className="footer-links">
                        <span>Privacy</span>
                        <span>Terms</span>
                        <span>Contact</span>
                    </div>
                </div>
            </footer>
        </div>
    );
};

const FeatureCard = ({ icon, title, desc }) => (
    <motion.div
        whileHover={{ y: -10 }}
        className="feature-card glass-panel"
    >
        <div className="icon-box">{icon}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
    </motion.div>
);

export default Landing;
