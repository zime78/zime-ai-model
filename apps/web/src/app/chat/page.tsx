'use client';

import { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';
import { chatApi } from '@/api/client';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: '안녕하세요! 무엇을 도와드릴까요? 업무나 문서에 대해 궁금한 점을 물어보세요.' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const data = await chatApi.sendMessage(userMessage);
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: '죄송합니다. 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
            <header style={{ marginBottom: '1rem' }}>
                <h1 className="title-gradient">AI 채팅</h1>
            </header>

            {/* Messages Area */}
            <div className="glass-card" style={{
                flex: 1,
                overflowY: 'auto',
                padding: '1.5rem',
                marginBottom: '1rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem'
            }}>
                {messages.map((msg, idx) => (
                    <div key={idx} style={{
                        display: 'flex',
                        justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        alignItems: 'flex-start',
                        gap: '0.75rem'
                    }}>
                        {msg.role === 'assistant' && (
                            <div style={{
                                background: 'rgba(255,255,255,0.1)',
                                padding: '0.5rem',
                                borderRadius: '50%'
                            }}>
                                <FaRobot />
                            </div>
                        )}

                        <div style={{
                            maxWidth: '80%',
                            padding: '1rem',
                            borderRadius: '1rem',
                            borderTopLeftRadius: msg.role === 'assistant' ? '0' : '1rem',
                            borderTopRightRadius: msg.role === 'user' ? '0' : '1rem',
                            background: msg.role === 'user'
                                ? 'linear-gradient(135deg, var(--primary), var(--secondary))'
                                : 'rgba(255,255,255,0.05)',
                            border: msg.role === 'assistant' ? '1px solid var(--glass-border)' : 'none',
                            lineHeight: '1.5'
                        }}>
                            {msg.content}
                        </div>

                        {msg.role === 'user' && (
                            <div style={{
                                background: 'rgba(255,255,255,0.1)',
                                padding: '0.5rem',
                                borderRadius: '50%'
                            }}>
                                <FaUser />
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div style={{ display: 'flex', gap: '0.5rem', color: '#94a3b8', fontStyle: 'italic' }}>
                        <FaRobot />
                        <span>생각 중...</span>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <form onSubmit={handleSubmit} style={{ position: 'relative' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="메시지를 입력하세요..."
                    style={{
                        width: '100%',
                        padding: '1rem',
                        paddingRight: '3rem',
                        borderRadius: '0.75rem',
                        background: 'var(--glass-bg)',
                        border: '1px solid var(--glass-border)',
                        color: 'white',
                        fontSize: '1rem',
                        outline: 'none'
                    }}
                    disabled={loading}
                />
                <button
                    type="submit"
                    disabled={loading || !input.trim()}
                    style={{
                        position: 'absolute',
                        right: '0.5rem',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        background: 'transparent',
                        border: 'none',
                        color: input.trim() ? '#818cf8' : '#475569',
                        cursor: input.trim() ? 'pointer' : 'default',
                        padding: '0.5rem'
                    }}
                >
                    <FaPaperPlane size={18} />
                </button>
            </form>
        </div>
    );
}
