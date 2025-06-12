import React, { useState } from 'react';
import axios from 'axios';

function ResumeUpload({ onMatches }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('resume', file);

    try {
      const response = await axios.post('http://localhost:8000/search_jobs/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onMatches(response.data.matches);
    } catch (err) {
      setError('Failed to upload or process resume.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Resume'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default ResumeUpload;
