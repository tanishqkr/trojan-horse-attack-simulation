import React from 'react';

const StatCard = ({ title, value, subtext, highlight = false, alertLevel = "LOW", icon, compact = false }) => {
  const isProgressBar = typeof value === 'number' && title.includes('Score');
  let barColor = "bg-green-500";
  if (alertLevel === "MEDIUM") barColor = "bg-yellow-500";
  if (alertLevel === "HIGH") barColor = "bg-red-500";

  return (
    <div className={`${compact ? 'p-3' : 'p-5'} rounded-xl border bg-slate-900 shadow-sm flex flex-col justify-between ${highlight ? 'border-cyan-500/50 shadow-[0_0_10px_rgba(6,182,212,0.1)]' : 'border-slate-800'}`}>
      <div className="flex items-center justify-between mb-1">
        <h4 className={`text-slate-400 font-medium uppercase tracking-wider ${compact ? 'text-[10px]' : 'text-sm'}`}>{title}</h4>
        {icon && <div className="opacity-50">{icon}</div>}
      </div>
      
      <div className="flex items-baseline space-x-2">
        <span className={`${compact ? 'text-xl' : 'text-3xl'} font-bold ${highlight ? 'text-cyan-400' : 'text-slate-100'}`}>
          {value}
        </span>
        {subtext && <span className="text-slate-500 text-[10px] font-medium uppercase">{subtext}</span>}
      </div>

      {isProgressBar && (
        <div className="w-full bg-slate-800 rounded-full h-1 mt-2 overflow-hidden">
          <div 
            className={`${barColor} h-full rounded-full transition-all duration-500 ease-out`} 
            style={{ width: `${Math.min(Math.max(value, 0), 100)}%` }}
          />
        </div>
      )}
    </div>
  );
};

export default StatCard;
