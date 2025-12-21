import Link from 'next/link';
import { FaServer, FaDatabase, FaBolt } from 'react-icons/fa';

export default function Home() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <header style={{ textAlign: 'center', padding: '3rem 0' }}>
        <h1 style={{ fontSize: '3rem', margin: 0 }} className="title-gradient">
          My-Brain에 오신 것을 환영합니다
        </h1>
        <p style={{ color: '#94a3b8', fontSize: '1.2rem', marginTop: '1rem' }}>
          업무와 지식 관리를 위한 나만의 AI 비서
        </p>
      </header>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0, color: '#f8fafc' }}>시스템 상태</h3>
            <FaServer color="#4ade80" />
          </div>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0, color: '#4ade80' }}>정상 작동 중</p>
          <span style={{ fontSize: '0.875rem', color: '#64748b' }}>백엔드 서버 가동 중</span>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0, color: '#f8fafc' }}>핵심 모델</h3>
            <FaBolt color="#facc15" />
          </div>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>Qwen 2.5</p>
          <span style={{ fontSize: '0.875rem', color: '#64748b' }}>Ollama (로컬) 실행 중</span>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0, color: '#f8fafc' }}>지식 베이스</h3>
            <FaDatabase color="#60a5fa" />
          </div>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: 0 }}>활성 상태</p>
          <span style={{ fontSize: '0.875rem', color: '#64748b' }}>/data 폴더 감시 중</span>
        </div>
      </div>

      {/* Recent Activity / Actions */}
      <div style={{ marginTop: '2rem' }}>
        <h2 style={{ marginBottom: '1.5rem' }}>빠른 작업</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          <Link href="/chat" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="glass-card" style={{ padding: '2rem', height: '100%', cursor: 'pointer' }}>
              <h3>💬 새 대화 시작하기</h3>
              <p style={{ color: '#94a3b8' }}>문서에 대해 질문하거나 업무 지원을 받아보세요.</p>
            </div>
          </Link>
          <Link href="/history" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="glass-card" style={{ padding: '2rem', height: '100%', cursor: 'pointer' }}>
              <h3>📜 업무 기록 보기</h3>
              <p style={{ color: '#94a3b8' }}>과거 대화 내용과 업무 요약을 확인하세요.</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
