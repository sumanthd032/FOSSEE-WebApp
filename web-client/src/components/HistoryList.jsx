import React from 'react';
import { FileText, Calendar, Database } from 'lucide-react';

const HistoryList = ({ history }) => {
  if (!history || history.length === 0) return (
    <div className="text-center py-10 text-slate-500">No upload history found.</div>
  );

  return (
    <div className="grid grid-cols-1 gap-4">
      {history.map((item) => (
        <div key={item.id} className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow flex items-center justify-between">
            
            {/* File Info */}
            <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600">
                    <FileText size={24} />
                </div>
                <div>
                    <h4 className="font-semibold text-slate-800 text-lg">{item.file_name}</h4>
                    <div className="flex items-center gap-4 text-sm text-slate-500 mt-1">
                        <span className="flex items-center gap-1">
                            <Calendar size={14} />
                            {new Date(item.uploaded_at).toLocaleString()}
                        </span>
                        <span className="flex items-center gap-1">
                            <Database size={14} />
                            {item.total_records} Records
                        </span>
                    </div>
                </div>
            </div>

            {/* Quick Stats Summary */}
            <div className="hidden md:flex gap-8 text-right">
                <div>
                    <p className="text-xs text-slate-400 uppercase font-semibold">Avg Flow</p>
                    <p className="font-medium text-slate-700">{item.avg_flowrate?.toFixed(2)}</p>
                </div>
                <div>
                    <p className="text-xs text-slate-400 uppercase font-semibold">Avg Pressure</p>
                    <p className="font-medium text-slate-700">{item.avg_pressure?.toFixed(2)}</p>
                </div>
                <div>
                    <p className="text-xs text-slate-400 uppercase font-semibold">Avg Temp</p>
                    <p className="font-medium text-slate-700">{item.avg_temperature?.toFixed(2)}</p>
                </div>
            </div>
        </div>
      ))}
    </div>
  );
};

export default HistoryList;