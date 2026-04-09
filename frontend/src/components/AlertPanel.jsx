import React from 'react';
import { AlertCircle, ShieldCheck, AlertTriangle } from 'lucide-react';

const AlertPanel = ({ alertLevel, summary, compact = false }) => {

  let panelStyle = "bg-slate-800 border-slate-700";
  let icon = <ShieldCheck className={`${compact ? 'w-5 h-5' : 'w-8 h-8'} text-slate-400`} />;
  let textColor = "text-slate-200";
  
  if (alertLevel === "LOW") {
    panelStyle = "bg-green-900/10 border-green-500/20";
    icon = <ShieldCheck className={`${compact ? 'w-5 h-5' : 'w-8 h-8'} text-green-400`} />;
    textColor = "text-green-100";
  } else if (alertLevel === "MEDIUM") {
    panelStyle = "bg-yellow-900/20 border-yellow-500/30";
    icon = <AlertTriangle className={`${compact ? 'w-5 h-5' : 'w-8 h-8'} text-yellow-400`} />;
    textColor = "text-yellow-100";
  } else if (alertLevel === "HIGH") {
    panelStyle = "bg-red-900/30 border-red-500/50";
    icon = <AlertCircle className={`${compact ? 'w-5 h-5' : 'w-8 h-8'} text-red-500`} />;
    textColor = "text-red-100";
  }

  return (
    <div className={`${compact ? 'p-3 py-4' : 'p-6'} rounded-xl border ${panelStyle} transition-all duration-300 flex items-center space-x-4 h-full`}>
      <div className={`${compact ? 'p-2' : 'p-3'} bg-black/20 rounded-full`}>
        {icon}
      </div>
      <div className="flex-1 overflow-hidden">
        <h3 className={`${compact ? 'text-[9px]' : 'text-sm'} font-bold uppercase tracking-wider text-slate-400 mb-0.5`}>
          Threat State: <span className={textColor}>{alertLevel}</span>
        </h3>
        <p className={`${compact ? 'text-xs md:text-sm' : 'text-lg'} font-bold ${textColor} truncate`}>
          {summary || "Awaiting Telemetry..."}
        </p>
      </div>
    </div>
  );
};

export default AlertPanel;
