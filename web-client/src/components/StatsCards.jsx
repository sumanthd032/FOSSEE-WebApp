import React from 'react';
import { Activity, Thermometer, Gauge, Database } from 'lucide-react';

const StatsCard = ({ title, value, unit, icon: Icon, color }) => (
  <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4 hover:shadow-md transition-shadow">
    <div className={`p-3 rounded-lg ${color} bg-opacity-10`}>
      <Icon className={`w-6 h-6 ${color.replace('bg-', 'text-')}`} />
    </div>
    <div>
      <p className="text-sm font-medium text-gray-500">{title}</p>
      <p className="text-2xl font-bold text-gray-900">
        {typeof value === 'number' ? value.toFixed(2) : value}
        <span className="text-sm text-gray-400 font-normal ml-1">{unit}</span>
      </p>
    </div>
  </div>
);

const StatsCards = ({ data }) => {
  if (!data) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard 
        title="Total Records" 
        value={data.total_records} 
        unit="entries" 
        icon={Database} 
        color="bg-blue-600" 
      />
      <StatsCard 
        title="Avg Flowrate" 
        value={data.avg_flowrate} 
        unit="m³/h" 
        icon={Activity} 
        color="bg-emerald-500" 
      />
      <StatsCard 
        title="Avg Pressure" 
        value={data.avg_pressure} 
        unit="bar" 
        icon={Gauge} 
        color="bg-amber-500" 
      />
      <StatsCard 
        title="Avg Temp" 
        value={data.avg_temperature} 
        unit="°C" 
        icon={Thermometer} 
        color="bg-rose-500" 
      />
    </div>
  );
};

export default StatsCards;