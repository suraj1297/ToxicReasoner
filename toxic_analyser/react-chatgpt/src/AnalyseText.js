import React, { useState } from 'react';

function AnalyseText() {
    const [text, setText] = useState('');
    const [responseText, setResponseText] = useState('');
    const [isLoading, setIsLoading] = useState(false); 

    const handleInputChange = (e) => {
        setText(e.target.value);
    };

    const handleAnalyzeClick = async () => {
        setIsLoading(true); 
        try {
            const response = await fetch('http://127.0.0.1:5000/api/reason', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ input_data: text.trim() }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log(data.reason[0].generated_text);
            setResponseText(data.reason[0].generated_text);
        } catch (error) {
            console.error('Error in fetching:', error);
            setResponseText('Error fetching response');
        } finally {
            setIsLoading(false); // End loading
        }
    };

    return (
        <div className="input-container">
            <textarea
                className="textarea-input"
                value={text}
                onChange={handleInputChange}
                rows="1"
                style={{ height: text ? `${text.split('\n').length * 20}px` : 'auto' }}
            />
            <button className="analyze-button" onClick={handleAnalyzeClick}>Analyze</button>
            {isLoading ? (
                <div className="loading-container">
                    <h3>Loading...</h3>
                </div>
            ) : (
                <div className="display-area">
                    <div>{responseText}</div>
                </div>
            )}
        </div>
    );
}

export default AnalyseText;
