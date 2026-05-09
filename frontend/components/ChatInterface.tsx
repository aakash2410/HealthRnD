import React, { useState } from 'react';

const ChatInterface: React.FC = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');

    const handleSearch = async () => {
        // TODO: Connect to backend RAG API endpoint
        setResponse(`Mocked response for: ${query}`);
    };

    return (
        <div className="chat-interface">
            <input 
                type="text" 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="Ask the Biomedical Knowledge Graph..." 
            />
            <button onClick={handleSearch}>Search</button>
            <div className="response">{response}</div>
        </div>
    );
};

export default ChatInterface;
