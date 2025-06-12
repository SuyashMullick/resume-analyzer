function JobMatches({ matches }) {
  if (!matches || matches.length === 0) {
    return <p>No job matches found.</p>;
  }

  return (
    <ul>
      {matches.map((job, idx) => (
        <li key={idx}>
          <h3>{job["Job Title"]}</h3>
          <p><strong>Company:</strong> {job.Company}</p>
          <p><strong>Relevance:</strong> {job.relevance_score}%</p>
          <p>{job.Job_Description?.substring(0, 150)}...</p>
        </li>
      ))}
    </ul>
  );
}

export default JobMatches;