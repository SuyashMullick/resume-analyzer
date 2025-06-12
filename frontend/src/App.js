import React, { useState } from 'react';
import ResumeUpload from './ResumeUpload';
import JobMatches from './JobMatches';

function App() {
  const [matches, setMatches] = useState([]);

  return (
    <div>
      <h1>Smart Resume Analyzer</h1>
      <ResumeUpload onMatches={setMatches} />
      <JobMatches matches={matches} />
    </div>
  );
}

export default App;
