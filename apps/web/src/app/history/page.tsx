'use client';

import { useState, useEffect } from 'react';
import { FaCalendarAlt, FaStar } from 'react-icons/fa';
import { workApi } from '@/api/client';

export default function HistoryPage() {
    const [dates, setDates] = useState<string[]>([]);
    const [selectedDate, setSelectedDate] = useState<string | null>(null);
    const [logContent, setLogContent] = useState<string>('');
    const [evaluation, setEvaluation] = useState<string>('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchDates();
    }, []);

    const fetchDates = async () => {
        try {
            const data = await workApi.getLogs();
            setDates(data);
            if (data.length > 0) {
                // setSelectedDate(data[0]);
                // fetchLog(data[0]);
            }
        } catch (error) {
            console.error(error);
        }
    };

    const fetchLog = async (date: string) => {
        setLoading(true);
        try {
            const data = await workApi.getLog(date);
            setLogContent(data.content);
            setSelectedDate(date);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchEvaluation = async () => {
        setLoading(true);
        try {
            const data = await workApi.getEvaluation('1 week');
            setEvaluation(data.evaluation);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '2rem 0' }}>
            <h1 className="title-gradient" style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>업무 기록 및 평가</h1>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
                {/* Sidebar: Date List */}
                <div className="glass-card" style={{ padding: '1.5rem', height: 'fit-content' }}>
                    <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <FaCalendarAlt className="text-blue-400" /> 날짜 선택
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        {dates.length === 0 && <p style={{ color: '#94a3b8' }}>기록이 없습니다.</p>}
                        {dates.map(date => (
                            <button
                                key={date}
                                onClick={() => fetchLog(date)}
                                style={{
                                    padding: '0.75rem',
                                    textAlign: 'left',
                                    borderRadius: '0.5rem',
                                    background: selectedDate === date ? 'rgba(99, 102, 241, 0.2)' : 'transparent',
                                    border: 'none',
                                    color: selectedDate === date ? '#818cf8' : '#cbd5e1',
                                    cursor: 'pointer',
                                    fontWeight: selectedDate === date ? 'bold' : 'normal'
                                }}
                            >
                                {date}
                            </button>
                        ))}
                    </div>

                    <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
                        <button
                            onClick={fetchEvaluation}
                            className="btn-primary"
                            style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                        >
                            <FaStar /> 주간 성과 평가하기
                        </button>
                    </div>
                </div>

                {/* Main: Content */}
                <div className="glass-card" style={{ padding: '2rem', minHeight: '500px' }}>
                    {loading ? (
                        <p style={{ color: '#94a3b8' }}>로딩 중...</p>
                    ) : evaluation ? (
                        <div>
                            <h2 style={{ marginBottom: '1rem', color: '#facc15' }}>AI 성과 평가 리포트</h2>
                            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', color: '#e2e8f0' }}>
                                {evaluation}
                            </div>
                            <button
                                onClick={() => setEvaluation('')}
                                style={{ marginTop: '2rem', background: 'transparent', border: '1px solid #64748b', color: '#94a3b8', padding: '0.5rem 1rem', borderRadius: '0.5rem', cursor: 'pointer' }}
                            >
                                닫기
                            </button>
                        </div>
                    ) : selectedDate ? (
                        <div>
                            <h2 style={{ marginBottom: '1rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }}>
                                {selectedDate} 업무 로그
                            </h2>
                            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', color: '#e2e8f0' }}>
                                {logContent}
                            </div>
                        </div>
                    ) : (
                        <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#64748b' }}>
                            <p>날짜를 선택하거나 성과 평가를 실행하세요.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
