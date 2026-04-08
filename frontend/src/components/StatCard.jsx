import React from 'react';

const StatCard = ({ title, value, subtext, highlight = false, alertLevel = "LOW" }) => {
  // Bonus: Progress Bar logic for risk score
  const isProgressBar = typeof value === 'number' && title.includes('Score');
  let barColor = "bg-green-500";
  if (alertLevel === "MEDIUM") barColor = "bg-yellow-500";
  if (alertLevel === "HIGH") barColor = "bg-red-500";

  return (
    <div className={`p-5 rounded-xl border bg-slate-900 shadow-sm flex flex-col justify-between ${highlight ? 'border-cyan-500/50 shadow-[0_0_10px_rgba(6,182,212,0.1)]' : 'border-slate-800'}`}>
      <h4 className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">{title}</h4>
      
      <div className="flex items-baseline space-x-2">
        <span className={`text-3xl font-bold ${highlight ? 'text-cyan-400' : 'text-slate-100'}`}>
          {value}
        </span>
        {subtext && <span className="text-slate-500 text-sm">{subtext}</span>}
      </div>

      {isProgressBar && (
        <div className="w-full bg-slate-800 rounded-full h-1.5 mt-4 overflow-hidden">
          <div 
            className={`${barColor} h-1.5 rounded-full transition-all duration-500 ease-out`} 
            style={{ width: `${Math.min(Math.max(value, 0), 100)}%` }}
          />
        </div>
      )}
    </div>
  );
};

export default StatCard;
