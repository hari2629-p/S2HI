import React, { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import type { AssessmentResult, DashboardDataResponse } from "../types/types";
import { getDashboardData } from "../services/api";
import "../styles/dashboard.css";

interface LocationState {
    results?: AssessmentResult;
    userId?: number;
    sessionId?: string;
    ageGroup?: string;
}

const Dashboard: React.FC = () => {
    const location = useLocation();
    const state = location.state as LocationState | null;

    const [dashboardData, setDashboardData] = useState<DashboardDataResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Check if we have session info to fetch real data
    const hasSessionInfo = state?.userId && state?.sessionId;

    useEffect(() => {
        const fetchDashboardData = async () => {
            if (!hasSessionInfo) return;

            setIsLoading(true);
            setError(null);

            try {
                const data = await getDashboardData(state.userId!, state.sessionId!);
                setDashboardData(data);
            } catch (err) {
                console.error('Failed to fetch dashboard data:', err);
                setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
            } finally {
                setIsLoading(false);
            }
        };

        fetchDashboardData();
    }, [hasSessionInfo, state?.userId, state?.sessionId]);

    // Generate dashboard data from fetched data or use demo data
    const generateDashboardData = () => {
        if (dashboardData) {
            // Use real data from backend
            return {
                studentId: dashboardData.student_id,
                ageGroup: dashboardData.age_group,
                finalRisk: dashboardData.final_risk,
                confidence: dashboardData.confidence,
                riskLevel: dashboardData.risk_level,
                assessmentDate: dashboardData.assessment_date,
                summary: dashboardData.summary,
                keyInsights: dashboardData.key_insights,
                patterns: {
                    reading: {
                        accuracy: dashboardData.patterns.reading.accuracy,
                        avgTime: dashboardData.patterns.reading.avg_time,
                        commonMistake: dashboardData.patterns.reading.common_mistake,
                        recommendation: dashboardData.patterns.reading.recommendation,
                    },
                    math: {
                        accuracy: dashboardData.patterns.math.accuracy,
                        avgTime: dashboardData.patterns.math.avg_time,
                        commonMistake: dashboardData.patterns.math.common_mistake,
                        recommendation: dashboardData.patterns.math.recommendation,
                    },
                    focus: {
                        accuracy: dashboardData.patterns.focus.accuracy,
                        avgTime: dashboardData.patterns.focus.avg_time,
                        commonMistake: dashboardData.patterns.focus.common_mistake,
                        recommendation: dashboardData.patterns.focus.recommendation,
                    },
                }
            };
        }

        // Demo data when no real data available
        return {
            studentId: "STU-DEMO",
            ageGroup: "9–11",
            finalRisk: "Demo Mode - Complete an Assessment",
            confidence: "N/A",
            riskLevel: 0,
            assessmentDate: "No assessment completed",
            summary: "This is a demo view. Complete an assessment to see real results.",
            keyInsights: [],
            patterns: {
                reading: {
                    accuracy: 72,
                    avgTime: 1050,
                    commonMistake: "Letter Reversal (b/d, p/q)",
                    recommendation: "Use highlighted letters, phonics-based games, and short reading chunks.",
                },
                math: {
                    accuracy: 88,
                    avgTime: 720,
                    commonMistake: "None",
                    recommendation: "Math performance is strong. No immediate intervention needed.",
                },
                focus: {
                    accuracy: 75,
                    avgTime: 880,
                    commonMistake: "Impulsive clicks",
                    recommendation: "Short tasks with clear visual cues and structured breaks are helpful.",
                },
            }
        };
    };

    const hasResults = dashboardData !== null;

    const studentData = generateDashboardData();

    const getDomainIcon = (domain: string) => {
        switch (domain) {
            case 'reading': return '📚';
            case 'math': return '🔢';
            case 'focus': return '🎯';
            default: return '📊';
        }
    };

    const getAccuracyLevel = (accuracy: number) => {
        if (accuracy >= 85) return { label: 'Excellent', class: 'level-excellent' };
        if (accuracy >= 70) return { label: 'Good', class: 'level-good' };
        if (accuracy >= 50) return { label: 'Needs Work', class: 'level-warning' };
        return { label: 'Critical', class: 'level-critical' };
    };

    const getNextSteps = () => {
        if (!dashboardData) {
            return [
                { text: 'Take your first assessment to get personalized results' },
                { text: 'Results will appear here after completion' },
                { text: 'Each assessment takes about 5-10 minutes' },
            ];
        }

        return [
            { text: 'Schedule follow-up with learning specialist' },
            { text: 'Implement recommended intervention strategies' },
            { text: 'Re-assess in 4-6 weeks to track progress' },
        ];
    };

    // Show loading state
    if (isLoading) {
        return (
            <div className="dashboard-container">
                <div style={{ textAlign: 'center', padding: '4rem' }}>
                    <h2>Loading dashboard data...</h2>
                </div>
            </div>
        );
    }

    // Show error state
    if (error) {
        return (
            <div className="dashboard-container">
                <div style={{ textAlign: 'center', padding: '4rem' }}>
                    <h2>Error loading dashboard</h2>
                    <p>{error}</p>
                    <Link to="/" className="btn btn-primary" style={{ marginTop: '1rem' }}>
                        Return to Assessment
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            {/* Header Section */}
            <header className="dashboard-header">
                <div className="header-content">
                    <h1 className="dashboard-title">Learning Assessment Dashboard</h1>
                    <p className="dashboard-subtitle">
                        {dashboardData ? 'Your screening results & personalized recommendations' : 'Demo view - Complete an assessment for real results'}
                    </p>
                </div>
                <div className="header-actions">
                    <button className="btn btn-secondary">
                        <span>📥</span> Export Report
                    </button>
                    <Link to="/" className="btn btn-primary">
                        <span>🔄</span> New Assessment
                    </Link>
                </div>
            </header>

            {/* No Results Banner */}
            {!dashboardData && (
                <div className="demo-banner">
                    <span>👋</span>
                    <p>
                        <strong>Demo Mode:</strong> You're viewing sample data.
                        <Link to="/"> Take an assessment</Link> to see your real results!
                    </p>
                </div>
            )}

            {/* Stats Overview Row */}
            <section className="stats-row">
                <div className="stat-card">
                    <div className="stat-icon">📅</div>
                    <div className="stat-content">
                        <span className="stat-label">Assessment Date</span>
                        <span className="stat-value">{studentData.assessmentDate}</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">🎂</div>
                    <div className="stat-content">
                        <span className="stat-label">Age Group</span>
                        <span className="stat-value">{studentData.ageGroup} years</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">📊</div>
                    <div className="stat-content">
                        <span className="stat-label">Overall Score</span>
                        <span className="stat-value">
                            {Math.round(
                                (studentData.patterns.reading.accuracy +
                                    studentData.patterns.math.accuracy +
                                    studentData.patterns.focus.accuracy) / 3
                            )}%
                        </span>
                    </div>
                </div>
                <div className="stat-card highlight">
                    <div className="stat-icon">⚡</div>
                    <div className="stat-content">
                        <span className="stat-label">Risk Level</span>
                        <span className="stat-value risk-value">
                            {studentData.riskLevel > 0 ? `${studentData.riskLevel}%` : 'N/A'}
                        </span>
                    </div>
                </div>
            </section>

            {/* Main Content Grid */}
            <div className="main-grid">
                {/* Left Column - Student Info */}
                <aside className="sidebar">
                    {/* Student Profile Card */}
                    <div className="card profile-card">
                        <div className="profile-header">
                            <div className="avatar">
                                <span>👤</span>
                            </div>
                            <div className="profile-info">
                                <h3>Student Profile</h3>
                                <span className="student-id">{studentData.studentId}</span>
                            </div>
                        </div>

                        <div className="profile-details">
                            <div className="detail-row">
                                <span className="detail-label">Status</span>
                                <span className={`status-badge ${hasResults ? 'warning' : 'demo'}`}>
                                    {hasResults ? studentData.finalRisk : 'No Assessment'}
                                </span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Confidence</span>
                                <span className="confidence-badge">{studentData.confidence}</span>
                            </div>
                        </div>
                    </div>

                    {/* Summary Card */}
                    <div className="card summary-card">
                        <h4>💡 Assessment Insight</h4>
                        <p>{studentData.summary}</p>

                        {dashboardData && studentData.keyInsights && studentData.keyInsights.length > 0 && (
                            <ul className="insights-list">
                                {studentData.keyInsights.map((insight, index) => (
                                    <li key={index}>{insight}</li>
                                ))}
                            </ul>
                        )}
                    </div>

                    {/* Next Steps Card */}
                    <div className="card next-steps-card">
                        <h4>📋 Recommended Next Steps</h4>
                        <ul className="steps-list">
                            {getNextSteps().map((step, index) => (
                                <li key={index}>
                                    <span className="step-number">{index + 1}</span>
                                    <span>{step.text}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </aside>

                {/* Right Column - Domain Cards */}
                <main className="content-area">
                    <h2 className="section-title">
                        <span>📈</span> Domain Performance Analysis
                    </h2>

                    <div className="domain-grid">
                        {Object.entries(studentData.patterns).map(([domain, data]) => {
                            const level = getAccuracyLevel(data.accuracy);
                            return (
                                <div key={domain} className={`card domain-card domain-${domain}`}>
                                    <div className="domain-header">
                                        <div className="domain-title">
                                            <span className="domain-icon">{getDomainIcon(domain)}</span>
                                            <h3>{domain.charAt(0).toUpperCase() + domain.slice(1)}</h3>
                                        </div>
                                        <span className={`accuracy-badge ${level.class}`}>
                                            {level.label}
                                        </span>
                                    </div>

                                    {/* Accuracy Circle */}
                                    <div className="accuracy-display">
                                        <div className={`accuracy-circle ${domain}`}>
                                            <span className="accuracy-value">{data.accuracy}%</span>
                                            <span className="accuracy-label">Accuracy</span>
                                        </div>
                                    </div>

                                    {/* Metrics */}
                                    <div className="metrics-row">
                                        <div className="metric">
                                            <span className="metric-icon">⏱️</span>
                                            <div className="metric-content">
                                                <span className="metric-value">{(data.avgTime / 1000).toFixed(1)}s</span>
                                                <span className="metric-label">Avg. Time</span>
                                            </div>
                                        </div>
                                        <div className="metric">
                                            <span className="metric-icon">⚠️</span>
                                            <div className="metric-content">
                                                <span className="metric-value">{data.commonMistake === 'None' ? '—' : '1'}</span>
                                                <span className="metric-label">Issues</span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Common Mistake */}
                                    {data.commonMistake !== 'None' && (
                                        <div className="mistake-box">
                                            <strong>Common Pattern:</strong> {data.commonMistake}
                                        </div>
                                    )}

                                    {/* Recommendation */}
                                    <div className="recommendation">
                                        <div className="recommendation-header">
                                            <span>💡</span> Teacher Tip
                                        </div>
                                        <p>{data.recommendation}</p>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </main>
            </div>

            {/* Footer Disclaimer */}
            <footer className="disclaimer">
                <span className="disclaimer-icon">ℹ️</span>
                <p>
                    <strong>Important:</strong> This is not a medical diagnosis. It is an early screening tool
                    designed to guide educational support and professional follow-up. Please consult with
                    qualified specialists for comprehensive evaluation.
                </p>
            </footer>
        </div>
    );
};

export default Dashboard;
