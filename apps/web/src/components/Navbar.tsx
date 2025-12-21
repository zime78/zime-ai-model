import Link from 'next/link';
import { FaBrain, FaSearch, FaHistory, FaCog } from 'react-icons/fa';

export default function Navbar() {
    return (
        <nav className="glass-card" style={{
            margin: '1rem 2rem',
            padding: '1rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            position: 'sticky',
            top: '1rem',
            zIndex: 50
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <FaBrain size={24} style={{ color: '#818cf8' }} />
                <span style={{ fontSize: '1.25rem', fontWeight: 'bold' }} className="title-gradient">
                    My-Brain
                </span>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
                <Link href="/" className="nav-link">대시보드</Link>
                <Link href="/chat" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FaSearch size={14} /> 대화하기
                </Link>
                <Link href="/history" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FaHistory size={14} /> 업무 기록
                </Link>
                <Link href="/settings" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FaCog size={14} /> 설정
                </Link>
            </div>
        </nav>
    );
}
