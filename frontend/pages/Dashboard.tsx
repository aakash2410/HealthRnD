import React from 'react';
import ChatInterface from '../components/ChatInterface';
import Visualizations from '../components/Visualizations';

const Dashboard: React.FC = () => {
    return (
        <div className="dashboard-layout">
            <header>
                <h1>Healthcare Innovation Scouting Platform</h1>
                <p>Role-Based Customized Dashboard</p>
            </header>
            <main>
                <section className="search-section">
                    <ChatInterface />
                </section>
                <section className="visualization-section">
                    <Visualizations />
                </section>
            </main>
        </div>
    );
};

export default Dashboard;
