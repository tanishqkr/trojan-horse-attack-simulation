import React from 'react';
import { AlertCircle, ShieldCheck, AlertTriangle } from 'lucide-react';

const AlertPanel = ({ alertLevel, summary }) => {
  // Determine styles strictly based on alert level
  let panelStyle = "bg-slate-800 border-slate-700";
  let icon = <ShieldCheck className="w-8 h-8 text-slate-400" />;
  let textColor = "text-slate-200";
  
  if (alertLevel === "LOW") {
    panelStyle = "bg-green-900/30 border-green-500/50 shadow-[0_0_15px_rgba(34,197,94,0.1)]";
    icon = <ShieldCheck className="w-8 h-8 text-green-400" />;
    textColor = "text-green-100";
  } else if (alertLevel === "MEDIUM") {
    panelStyle = "bg-yellow-900/30 border-yellow-500/50 shadow-[0_0_15px_rgba(234,179,8,0.2)]";
    icon = <AlertTriangle className="w-8 h-8 text-yellow-400" />;
    textColor = "text-yellow-100";
  } else if (alertLevel === "HIGH") {
    panelStyle = "bg-red-900/40 border-red-500 animate-intense-pulse";
    icon = <AlertCircle className="w-8 h-8 text-red-500" />;
    textColor = "text-red-100";
  }

  return (
    <div className={`p-6 rounded-xl border ${panelStyle} transition-all duration-300 flex items-center space-x-4`}>
      <div className="p-3 bg-black/20 rounded-full">
        {icon}
      </div>
      <div>
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-1">
          System Threat State: <span className={textColor}>{alertLevel}</span>
        </h3>
        <p className={`text-lg font-medium ${textColor}`}>
          {summary || "Awaiting Telemetry..."}
        </p>
      </div>
    </div>
  );
};

export default AlertPanel;
