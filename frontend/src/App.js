import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [analyses, setAnalyses] = useState([]);
  const [fullName, setFullName] = useState('');
  const [cloneUrl, setCloneUrl] = useState('');
  const [loading, setLoading] = useState(false);

  // rename your loader or keep loadAnalyses
  const loadAnalyses = () => {
    fetch('http://127.0.0.1:8000/analyses')
      .then(res => res.json())
      .then(data => setAnalyses(data))
      .catch(err => console.error(err));
  };

  // on mount, clear the list then fetch fresh
  useEffect(() => {
    fetch("http://127.0.0.1:8000/analyses", { method: "DELETE" })
      .then(() => loadAnalyses());
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!fullName || !cloneUrl) return;
    setLoading(true);
    try {
      await fetch('http://127.0.0.1:8000/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-GitHub-Event': 'push' },
        body: JSON.stringify({ repository: { full_name: fullName, clone_url: cloneUrl } }),
      });
      loadAnalyses();
      setFullName('');
      setCloneUrl('');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="wrapper">
      <div className="editor-container">
        <div className="editor-header">
          <span className="circle red" />
          <span className="circle yellow" />
          <span className="circle green" />
          <span className="editor-title">Code Complexity Dashboard</span>
        </div>
        <div className="editor-body">
          <form className="analyze-form" onSubmit={handleAnalyze}>
            <input
              type="text"
              placeholder="username/repo"
              value={fullName}
              onChange={e => setFullName(e.target.value)}
              disabled={loading}
            />
            <input
              type="text"
              placeholder="https://github.com/… .git"
              value={cloneUrl}
              onChange={e => setCloneUrl(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Analyzing…' : 'Analyze'}
            </button>
          </form>
          <pre>{`// Analyzed Repositories
const complexityResults = [
${analyses
    .filter(a => a.complexity_score > 0)
    .map(
      a => `  { repoId: ${JSON.stringify(a.repo_full_name)}, complexity: ${a.complexity_score.toFixed(2)} },`
    )
    .join('\n')}
];`}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
