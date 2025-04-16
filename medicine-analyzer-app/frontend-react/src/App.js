import React, { useState } from 'react';
import { analyzeImage, translateText } from './api';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [language, setLanguage] = useState('None');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert('Please upload a file');
    setLoading(true);
    setTranslatedText('');
    try {
      const res = await analyzeImage(file);
      setResponseText(res.data.reply);
    } catch (err) {
      console.error(err);
      alert('Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async () => {
    if (language === 'None') return;
    setLoading(true);
    try {
      const res = await translateText(responseText, language);
      setTranslatedText(res.data.translated);
    } catch (err) {
      console.error(err);
      alert('Failed to translate');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h2>💊 Medicine Image Analyzer</h2>
      <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Get Generic Name"}
      </button>

      {responseText && (
        <>
          <h3>🧾 Result (English)</h3>
          <p>{responseText}</p>

          <div>
            <label>🌐 Translate to: </label>
            <select value={language} onChange={e => setLanguage(e.target.value)}>
              <option value="None">None</option>
              <option value="Hindi">Hindi</option>
              <option value="Tamil">Tamil</option>
              <option value="Telugu">Telugu</option>
            </select>
            <button onClick={handleTranslate} disabled={language === 'None' || loading}>
              {loading ? "Translating..." : "Translate"}
            </button>
          </div>

          {translatedText && (
            <>
              <h3>🌐 Translated Response ({language})</h3>
              <p>{translatedText}</p>
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;