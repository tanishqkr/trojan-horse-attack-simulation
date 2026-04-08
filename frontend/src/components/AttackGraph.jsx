import React, { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format, parseISO } from 'date-fns';

const AttackGraph = ({ logs }) => {
  // Transform log sequence into an accumulation array optimized for Recharts mapping X=time, Y=count
  const data = useMemo(() => {
    if (!logs || logs.length === 0) return [];
    
    let encryptedCount = 0;
    const series = [];

    // Filter only successful file encryptions to track the attack spread
    const attackLogs = logs.filter(l => l.event === "FILE_ENCRYPTED" && l.status === "SUCCESS");
    
    attackLogs.forEach((log) => {
      encryptedCount += 1;
      try {
        series.push({
          timeRaw: log.timestamp,
          timeFormatted: format(parseISO(log.timestamp), 'HH:mm:ss.SSS'),
          count: encryptedCount
        });
      } catch(e) {
        // Drop malformed timestamps gracefully
      }
    });

    return series;
  }, [logs]);

  if (data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center bg-slate-900 border border-slate-800 rounded-xl">
        <p className="text-slate-500">Awaiting payload telemetry...</p>
      </div>
    );
  }

  return (
    <div className="h-72 p-4 bg-slate-900 border border-slate-800 rounded-xl">
      <h3 className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-4">
        Attack Vector Propagation
      </h3>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis 
            dataKey="timeFormatted" 
            stroke="#475569" 
            tick={{ fontSize: 11 }}
            tickMargin={10}
            minTickGap={30}
          />
          <YAxis 
            stroke="#475569" 
            tick={{ fontSize: 11 }} 
            allowDecimals={false}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
            itemStyle={{ color: '#ecf0f1' }}
          />
          <Line 
            type="stepAfter" 
            dataKey="count" 
            name="Files Encrypted" 
            stroke="#ef4444" 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6, fill: '#ef4444', stroke: '#fff' }}
            animationDuration={500}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AttackGraph;
