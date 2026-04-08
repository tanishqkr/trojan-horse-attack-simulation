import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const AttackGraph = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center bg-slate-900 border border-slate-800 rounded-xl">
        <p className="text-slate-500 text-sm">Awaiting payload telemetry...</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col p-4 bg-slate-900 border border-slate-800 rounded-xl min-h-0">
      <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-[0.2em] mb-4">
        Threat Activity Intensity (pkts/sec)
      </h3>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis 
              dataKey="time" 
              stroke="#475569" 
              tick={{ fontSize: 9 }}
              tickMargin={10}
              minTickGap={40}
            />
            <YAxis 
              stroke="#475569" 
              tick={{ fontSize: 9 }} 
              allowDecimals={false}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }}
              itemStyle={{ color: '#ecf0f1' }}
              cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
            />
            <Bar 
              dataKey="count" 
              name="Events/sec" 
              radius={[2, 2, 0, 0]}
              animationDuration={500}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.count > 5 ? '#f43f5e' : entry.count > 2 ? '#fbbf24' : '#06b6d4'} 
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AttackGraph;
