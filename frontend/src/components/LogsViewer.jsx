import React from 'react';
import { format, parseISO } from 'date-fns';

const LogsViewer = ({ logs }) => {
  if (!logs || logs.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center bg-slate-900 border border-slate-800 rounded-xl">
        <p className="text-slate-500 text-sm font-medium uppercase tracking-widest">System Logs Empty</p>
      </div>
    );
  }


  const sortedLogs = [...logs].reverse();

  return (
    <div className="flex-1 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col min-h-0">
      <div className="px-4 py-2 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between">
        <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-[0.2em]">
          Real-Time System Telemetry
        </h3>
        <span className="text-[9px] text-slate-500 font-mono">{logs.length} Total Signals</span>
      </div>
      
      <div className="overflow-x-auto overflow-y-auto flex-1 p-0 custom-scrollbar">
        <table className="w-full text-left text-[11px] text-slate-400 border-collapse">
          <thead className="bg-slate-950 sticky top-0 z-10 text-[9px] uppercase text-slate-500 font-bold tracking-tighter">
            <tr>
              <th className="px-3 py-2 border-b border-slate-800">Timestamp</th>
              <th className="px-3 py-2 border-b border-slate-800">Operation</th>
              <th className="px-3 py-2 border-b border-slate-800">Status</th>
              <th className="px-3 py-2 border-b border-slate-800 w-full">Endpoint Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {sortedLogs.map((log, index) => {
              let statusColor = "text-slate-300";
              let statusBg = "bg-slate-800/50";
              
              if (log.status === "ERROR") {
                statusColor = "text-red-400";
                statusBg = "bg-red-900/20";
              } else if (log.status === "SUCCESS" && log.event === "FILE_ENCRYPTED") {
                statusColor = "text-yellow-400";
                statusBg = "bg-yellow-900/20";
              } else if (log.status === "SUCCESS") {
                statusColor = "text-green-400";
                statusBg = "bg-green-900/20";
              }

              let timeDisplay = log.timestamp;
              try {
                timeDisplay = format(parseISO(log.timestamp), 'HH:mm:ss.SS');
              } catch(e) {}

              const details = log.file || log.error || `[${log.event}]`;

              return (
                <tr key={index} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-3 py-1.5 whitespace-nowrap font-mono text-[10px] opacity-70">{timeDisplay}</td>
                  <td className="px-3 py-1.5 whitespace-nowrap font-bold text-slate-300 uppercase tracking-tighter">{log.event}</td>
                  <td className="px-3 py-1.5 whitespace-nowrap">
                    <span className={`px-1.5 py-0.5 rounded-sm text-[9px] font-black uppercase tracking-tighter ${statusColor} ${statusBg}`}>
                      {log.status}
                    </span>
                  </td>
                  <td className="px-3 py-1.5 font-mono text-[10px] text-slate-500 truncate max-w-xs xl:max-w-md" title={details}>
                    {details}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default LogsViewer;
