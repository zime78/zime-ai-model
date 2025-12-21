'use client';

import { FaCog, FaSave } from 'react-icons/fa';

export default function SettingsPage() {
    return (
        <div style={{ padding: '2rem 0', maxWidth: '800px', margin: '0 auto' }}>
            <h1 className="title-gradient" style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>설정</h1>

            <div className="glass-card" style={{ padding: '2rem' }}>
                <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FaCog className="text-blue-400" /> 일반 설정
                </h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: '#cbd5e1' }}>AI 모델</label>
                        <select style={{
                            width: '100%',
                            padding: '0.75rem',
                            borderRadius: '0.5rem',
                            background: 'rgba(0,0,0,0.3)',
                            border: '1px solid var(--glass-border)',
                            color: 'white'
                        }}>
                            <option>Qwen 2.5 (Local)</option>
                            <option>Llama 3 (Local)</option>
                        </select>
                    </div>

                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: '#cbd5e1' }}>언어 (Language)</label>
                        <select style={{
                            width: '100%',
                            padding: '0.75rem',
                            borderRadius: '0.5rem',
                            background: 'rgba(0,0,0,0.3)',
                            border: '1px solid var(--glass-border)',
                            color: 'white'
                        }}>
                            <option>한국어</option>
                            <option>English</option>
                        </select>
                    </div>

                    <div style={{ paddingTop: '1rem' }}>
                        <button className="btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <FaSave /> 저장하기
                        </button>
                    </div>
                </div>
            </div>

            <div style={{ marginTop: '2rem', textAlign: 'center', color: '#64748b', fontSize: '0.875rem' }}>
                My-Brain v1.0.0
            </div>
        </div>
    );
}
