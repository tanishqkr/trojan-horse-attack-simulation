import React from 'react';
import { format, parseISO } from 'date-fns';

const LogsViewer = ({ logs }) => {
  if (!logs || logs.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center bg-slate-900 border border-slate-800 rounded-xl mt-6">
        <p className="text-slate-500">System Logs Empty</p>
      </div>
    );
  }

  // Reverse to show newest at the top
  const sortedLogs = [...logs].reverse();

  return (
    <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[400px]">
      <div className="p-4 border-b border-slate-800 bg-slate-900/50">
        <h3 className="text-slate-400 text-sm font-medium uppercase tracking-wider">
          Real-Time Telemetry Stream
        </h3>
      </div>
      
      <div className="overflow-x-auto overflow-y-auto flex-1 p-0 custom-scrollbar">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-900/80 sticky top-0 bg-opacity-95 backdrop-blur-sm z-10 text-xs uppercase text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">Timestamp</th>
              <th className="px-4 py-3 font-medium">Event</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium w-full">Path/Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
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
                timeDisplay = format(parseISO(log.timestamp), 'HH:mm:ss.SSS');
              } catch(e) {}

              // Use file path or fallback to extracting err traces
              const details = log.file || log.error || `[${log.event} trigger]`;

              return (
                <tr key={index} className="hover:bg-slate-800/50 transition-colors">
                  <td className="px-4 py-3 whitespace-nowrap font-mono text-xs">{timeDisplay}</td>
                  <td className="px-4 py-3 whitespace-nowrap font-medium text-slate-300">{log.event}</td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={`px-2 py-1 rounded text-xs font-semibold tracking-wide ${statusColor} ${statusBg}`}>
                      {log.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-mono text-xs text-slate-500 truncate max-w-md" title={details}>
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
