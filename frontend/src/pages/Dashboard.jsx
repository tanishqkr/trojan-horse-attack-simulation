import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity } from 'lucide-react';
import StatCard from '../components/StatCard';
import AlertPanel from '../components/AlertPanel';
import AttackGraph from '../components/AttackGraph';
import LogsViewer from '../components/LogsViewer';

const Dashboard = () => {
  const [analysis, setAnalysis] = useState({
    total_files: 0,
    time_taken: 0.0,
    alert_level: "LOW",
    risk_score: 0,
    summary: "Awaiting connection...",
    attack_detected: false
  });

  const [logs, setLogs] = useState([]);
  const [isLive, setIsLive] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [analysisRes, logsRes] = await Promise.all([
          axios.get('http://localhost:3600/analysis'),
          axios.get('http://localhost:3600/logs')
        ]);

        setAnalysis(analysisRes.data);
        setLogs(logsRes.data);
        setIsLive(true);
      } catch (error) {
        console.error("Backend connection failed", error);
        setIsLive(false);
      }
    };

    // Auto-refresh every 2.5 seconds
    fetchData();
    const interval = setInterval(fetchData, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-6 md:p-8">
      {/* Header section */}
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-100 flex items-center">
            <Activity className="w-8 h-8 mr-3 text-cyan-500" />
            Security Operations Center
          </h1>
          <p className="text-slate-400 mt-1">Real-time threat telemetry and endpoint monitoring</p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="relative flex h-3 w-3">
            {isLive && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>}
            <span className={`relative inline-flex rounded-full h-3 w-3 ${isLive ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
          </span>
          <span className="text-sm font-medium uppercase tracking-wider text-slate-400">
            {isLive ? 'System Online' : 'System Offline'}
          </span>
        </div>
      </div>

      {/* Main Alert Panel Full Width */}
      <div className="mb-6">
        <AlertPanel alertLevel={analysis.alert_level} summary={analysis.summary} />
      </div>

      {/* Top Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <StatCard
          title="Files Compromised"
          value={analysis.total_files}
          highlight={analysis.total_files > 0}
        />
        <StatCard
          title="Attack Duration"
          value={analysis.time_taken}
          subtext="sec"
        />
        <StatCard
          title="Overall Risk Score"
          value={analysis.risk_score}
          alertLevel={analysis.alert_level}
        />
      </div>

      {/* Graph Row */}
      <div className="w-full mb-6">
        <AttackGraph logs={logs} />
      </div>

      {/* Logs Row */}
      <div className="w-full">
        <LogsViewer logs={logs} />
      </div>
    </div>
  );
};

export default Dashboard;
